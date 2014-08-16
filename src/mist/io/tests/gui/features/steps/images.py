from behave import *
from time import time, sleep
from general import fill_text

@when(u'I wait until images are loaded')
def wait_images_load(context, timeout=60):
    """Wait until images are loaded in image list view. Count image list items
    to determine that.
    """

    images_list = context.browser.find_element_by_id("image-list")

    for i in range(timeout):
        images = images_list.find_elements_by_tag_name("li")
        if len(images):
            return
        sleep(1)

    assert False, u'Images failed to load'


@when(u'I type "{text}" into the images filter')
def fill_keys_filter(context, text):
    """Fill the filter in the images list view with the given text"""

    search_input = context.browser.find_element_by_id("search-term-input")
    fill_text(search_input, text)


@then(u'there should be starred images')
def starred_images_exist(context):
    starred = context.browser.find_elements_by_class_name("ui-checkbox-on")
    assert len(starred), u'No starred images found'


@then(u'the first image should contain "{text}"')
def first_image_contains_text(context, text, timeout=30):

    images_list = context.browser.find_element_by_id("image-list")

    for i in range(timeout):
        first_image = images_list.find_elements_by_tag_name("li")[0]
        if text in first_image.text:
            return
        sleep(1)

    assert False, u'First image does not contain %s' % text


@then(u'an Image that contains "{text}" should be starred')
def assert_starred_image(context, text):
    images_list = context.browser.find_element_by_id("image-list")
    images = images_list.find_elements_by_tag_name("li")

    starred_images = []
    for image in images:
        try:
            image.find_element_by_class_name("ui-checkbox-on")
            starred_images.append(image)
        except:
            pass

    for image in starred_images:
        if text in image.text:
            return

    assert False, u'No starred image found containing: %s ' % text


@when(u'I star an Image that contains "{text}"')
def star_image(context, text):
    images_list = context.browser.find_element_by_id("image-list")
    images = images_list.find_elements_by_tag_name("li")

    for image in images:
        if text in image.text:
            star_button = image.find_element_by_class_name("ui-checkbox")
            star_button.click()
            return


@when(u'I clear the Images search bar')
def clear_image_search_bar(context):
    search_bar = context.browser.find_element_by_id("search-term-input")
    for i in range(20):
        search_bar.send_keys(u'\ue003')