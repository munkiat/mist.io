"""mist.io.socket

Here we define the socketio Connection and handlers.

When a user loads mist.io or comes back online, their browser will request a
new socket and the initialize function will be triggered on the server within a
greenlet.

"""

import uuid
import json
import socket
import random
from time import time

from sockjs.tornado import SockJSConnection, SockJSRouter
from mist.io.sockjs_mux import MultiplexConnection
import tornado.iostream

import requests

try:
    from mist.core.helpers import user_from_session_id
    from mist.core import config
    from mist.core.methods import get_stats
    multi_user = True
except ImportError:
    from mist.io.helpers import user_from_session_id
    from mist.io import config
    from mist.io.methods import get_stats
    multi_user = False

from mist.io.helpers import amqp_subscribe_user
from mist.io.methods import notify_user
from mist.io.exceptions import MachineUnauthorizedError
from mist.io.exceptions import BadRequestError
from mist.io.amqp_tornado import Consumer

from mist.io import methods
from mist.io import tasks
from mist.io.shell import Shell
from mist.io.hub.tornado_shell_client import ShellHubClient

import logging
logging.basicConfig(level=config.PY_LOG_LEVEL,
                    format=config.PY_LOG_FORMAT,
                    datefmt=config.PY_LOG_FORMAT_DATE)
log = logging.getLogger(__name__)


# hold all open connections to properly clean them up in case of SIGTERM
CONNECTIONS = set()


def get_conn_info(conn_info):
    real_ip = forwarded_for = user_agent = ''
    for header in conn_info.headers:
        if header.lower() == 'x-real-ip':
            real_ip = conn_info.headers[header]
        elif header.lower() == 'x-forwarded-for':
            forwarded_for = conn_info.headers[header]
        elif header.lower() == 'user-agent':
            user_agent = conn_info.headers[header]
    ip = real_ip or forwarded_for or conn_info.ip
    session_id = ''
    if 'beaker.session.id' in conn_info.cookies.keys():
        session_id = conn_info.cookies['beaker.session.id'].value
    return ip, user_agent, session_id


class MistConnection(SockJSConnection):
    def on_open(self, conn_info):
        log.info("%s: Initializing", self.__class__.__name__)
        self.ip, self.user_agent, session_id = get_conn_info(conn_info)
        self.user = user_from_session_id(session_id)
        self.session_id = uuid.uuid4().hex
        CONNECTIONS.add(self)

    def send(self, msg, data=None):
        super(MistConnection, self).send(json.dumps({msg: data}))

    def on_close(self):
        log.info("%s: on_close event handler", self.__class__.__name__)
        CONNECTIONS.remove(self)


class ShellConnection(MistConnection):
    def on_open(self, conn_info):
        super(ShellConnection, self).on_open(conn_info)
        self.hub_client = None
        self.ssh_info = {}

    def on_shell_open(self, data):
        if self.ssh_info:
            self.close()
        self.ssh_info = {
            'backend_id': data['backend_id'],
            'machine_id': data['machine_id'],
            'host': data['host'],
            'columns': data['cols'],
            'rows': data['rows'],
            'ip': self.ip,
            'user_agent': self.user_agent,
            'email': self.user.email,
            'provider': data.get('provider', '')
        }
        self.hub_client = ShellHubClient(worker_kwargs=self.ssh_info)
        self.hub_client.on_data = self.emit_shell_data
        self.hub_client.start()
        log.info('on_shell_open finished')

    def on_shell_data(self, data):
        self.hub_client.send_data(data)

    def on_shell_resize(self, columns, rows):
        self.hub_client.resize(columns, rows)

    def emit_shell_data(self, data):
        self.send('shell_data', data)

    def on_close(self):
        if self.hub_client:
            self.hub_client.stop()
        super(ShellConnection, self).on_close()


class UserUpdatesConsumer(Consumer):
    def __init__(self, main_sockjs_conn,
                 amqp_url='amqp://guest:guest@127.0.0.1/'):
        self.sockjs_conn = m