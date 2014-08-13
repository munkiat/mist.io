from behave import *
from time import time, sleep
from general import fill_text, get_text


@given(u'a key named "{name}"')
def given_key(context, name):
    context.execute_steps(u"""
    When I visit "/keys"
    And I click the "Add" button
    And I type "%s" in key name input
    And I click the "Generate" button inside the "Add key" popup
    And I wait until private key is filled
    And I click the "Add" button inside the "Add key" popup
    Then "%s" key should be added within 15 seconds
    """ % (name, name))


@when(u'I type "{text}" in key name input')
def fill_key_name(context, text):
    """Type the given text into the "Name" input field of Add key popup"""

    if "randomly_created" in text:
        text = context.random_name

    textfield = context.browser.find_element_by_id("key-add-id")
    fill_text(textfield, text)


@when(u'I wait until private key is filled')
def wait_private_key_fill(context, timeout=20):
    """Wait until the "Private Key" input field of Add key popup
    is filled with a private key
    """

    key_start = "-----BEGIN RSA"
    textfield = context.browser.find_element_by_id("key-add-private")

    for i in range(timeout):
        if key_start in get_text(textfield):
            return
        sleep(1)

    assert False, u"Private key was not filled"


@when(u'I type "{text}" in new key name input')
def fill_key_new_name(context, text):
    """Type the given text into the "New name" input field of Rename key popup"""

    if "randomly_created" in text:
        text = context.random_name
    sleep(0.5)
    textfield = context.browser.find_element_by_id("new-key-name")
    fill_text(textfield, text)


@when(u'I type "{text}" into the keys filter')
def fill_keys_filter(context, text):
    """Fill the filter in the key list view with the given text"""

    search_parent = context.browser.find_elements_by_css_selector(".ui-input-search")
    search_field = search_parent[0].find_elements_by_tag_name("input")[0]
    fill_text(search_field, text)


@when(u'I delete all keys')
def delete_all_keys(context):

    keys_length = len(context.browser.find_elements_by_css_selector(".ui-listview li.ember-view"))

    for i in range(keys_length):
        key = context.browser.find_elements_by_css_selector(".ui-listview li.ember-view")[0]
        name = key.text.replace("default", "").strip()
        context.execute_steps(u"""
        When I visit "/keys"
        And I check the button that contains "%s"
        And I click the "Delete" button
        And I click the "Yes" button
        Then "%s" key should be removed
        """ % (name, name))


@then(u'"{text}" key should be added within {timeout} seconds')
def is_key_added_within_timeout(context, text, timeout):
    """Check if a key was added to the keys list within a specific timeout"""

    if "randomly_created" in text:
        text = context.random_name

    for i in range(int(timeout)):
        keys = context.browser.find_elements_by_css_selector(".ui-listview li")
        for key in keys:
            if text in key.text:
                return
        sleep(1)

    assert False, u"%s Key was not added within %s seconds" % (text, timeout)


@then(u'"{text}" should be the default key')
def is_key_default(context, text, timeout=10):
    """Check if the key is the default one. This is determined by the "default"
    tag that is added to the list item
    """

    if "randomly_created" in text:
        text = context.random_name

    for i in range(timeout * 2):
        keys = context.browser.find_elements_by_css_selector(".ui-listview li")
        for key in keys:
            if text in key.text and "default" in key.text:
                return
        sleep(0.5)

    assert False, u"%s Key is not the default one" % text


@then(u'"{text}" key should be removed')
def is_key_removed(context, text, timeout=10):
    """Check if a key does not exist in the keys list"""

    if "randomly_created" in text:
        text = context.random_name

    for i in range(timeout * 2):
        keys = context.browser.find_elements_by_css_selector(".ui-listview li")
        found = False
        for key in keys:
            if text in key.text:
                found = True
        if not found:
            return
        sleep(0.5)

    assert False, u"%s Key is not removed" % text
