from behave import *
from time import time, sleep

try:
    from mist.io.tests.settings import LOCAL
except ImportError:
    LOCAL = True
    pass

@when(u'I visit mist.io')
def visit(context):
    visit_route(context, '/')


@when(u'I visit "{route}"')
def visit_route(context, route):
    # Navigate the browser to the requested route
    context.browser.get('%s/#%s' % (context.mist_url, route))
    # Wait for the splash screen to disappear
    splash_loadout(context)


@when(u'I wait for {seconds} seconds')
def wait(context, seconds):
    sleep(int(seconds))


@when(u'I click the "{text}" button')
def click_button(context, text):
    sleep(0.5)
    buttons = context.browser.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if button.text == text:
            button.click()
            sleep(1)
            return

    assert False, u'Could not find %s button' % text


@when(u'I click the button that contains "{text}"')
def click_button(context, text):
    buttons = context.browser.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if text in button.text:
            button.click()
            return

    assert False, u'Could not find button that contains %s' % text


@when(u'I check the button that contains "{text}"')
def check_button(context, text):
    buttons = context.browser.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if text in button.text:
            # Get parent
            parent = button.find_element_by_xpath('..')
            # Get checkbox
            checkbox = parent.find_elements_by_tag_name('label')[0]
            checkbox.click()
            return

    assert False, u'Could not find button that contains %s' % text


@when(u'I click the "{text}" button inside the "{popup}" popup')
def click_button_within_popup(context, text, popup):
    popups = context.browser.find_elements_by_class_name("ui-popup-active")
    for pop in popups:
        if popup in pop.text:
            buttons = pop.find_elements_by_class_name("ui-btn")
            for button in buttons:
                if text in button.text:
                    button.click()
                    return

    assert False, u'Could not find %s button in %s popup' % (text, popup)


@when(u'I click the "{text}" button inside the "{panel_title}" panel')
def click_button_within_panel(context, text, panel_title):
    panels = context.browser.find_elements_by_class_name("ui-panel-open")
    if not panels:
        assert False, u'No open panels found. Maybe the driver got refocused or the panel failed to open'

    found_panel = None
    for panel in panels:
        header = panel.find_element_by_tag_name("h1")
        if panel_title in header.text:
            found_panel = panel
            break

    if not found_panel:
        assert False, u'Panel with Title %s could not be found. Maybe the driver got refocused or the panel ' \
                      u'failed to open or there is no panel with that title' % panel_title

    buttons = found_panel.find_elements_by_class_name("ui-btn")
    for button in buttons:
        if text in button.text:
            button.click()
            return

    assert False, u'Could not find %s button inside %s panel' % (text, panel_title)


@then(u'the header should be "{text}" within {timeout} seconds')
def assert_header_is_within_timeout(context, text, timeout):

    for i in range(int(timeout) * 2):
        header = context.browser.find_elements_by_class_name('ui-header')[0]
        title = header.find_elements_by_class_name('ui-title')[0]
        if text == title.text:
            return
        sleep(0.5)

    assert False, u'Page header is not %s' % text


@then(u'the title should be "{text}" within {timeout} seconds')
def assert_title_is_within_timeout(context, text, timeout):

    for i in range(int(timeout) * 2):
        if text == context.browser.title:
            return
        sleep(0.5)

    assert False, u'Page title is not %s' % text


@then(u'the title should be "{text}"')
def assert_title_is(context, text):
    assert text == context.browser.title


@then(u'the title should contain "{text}"')
def assert_title_contains(context, text):
    assert text in context.browser.title


def splash_loadout(context, timeout=20):

    for i in range(timeout):
        splash_screen = context.browser.find_element_by_id('splash')
        display = splash_screen.value_of_css_property('display')
        if 'none' in display:
            return
        sleep(1)

    assert False, u'Page took longer than %s seconds to load' % str(timeout)


def erase_text(element, timeout=10):

    for i in range(timeout * 2):

        # Send backspaces to delete any existing text
        for i in range(len(get_text(element))):
            element.send_keys(u'\ue003')

        # Check if textfield is empty
        if not get_text(element):
            return

        sleep(0.5)

    assert False, u"Failed to erase element's text"


def fill_text(element, text, timeout=10):

    for i in range(timeout * 2):

        # Erase any pre-existing text
        erase_text(element)

        # Fill the chars of the text one by one
        for char in text:
            element.send_keys(char)

        # Check if the text field contains the wanted text
        if get_text(element) == text:
            return

        sleep(0.5)

    assert False, u"Failed to fill element with text"


def get_text(element):
    return element.text or element.get_attribute('value')
