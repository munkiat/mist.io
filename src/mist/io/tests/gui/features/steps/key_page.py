from behave import *
from time import time, sleep
from general import get_text


@then(u'I should see the public key')
def is_public_key_visible(context, timeout=10):

    textfield = context.browser.find_element_by_id("public-key")

    for i in range(timeout * 2):
        if get_text(textfield)[:7] == "ssh-rsa":
            return
        sleep(0.5)

    assert False, u"Public key is not visible"


@then(u'I should see the private key')
def is_public_key_visible(context, timeout=10):

    textfield = context.browser.find_element_by_id("private-key")

    for i in range(timeout * 2):
        if get_text(textfield)[:14] == "-----BEGIN RSA":
            return
        sleep(0.5)

    assert False, u"Private key is not visible"
