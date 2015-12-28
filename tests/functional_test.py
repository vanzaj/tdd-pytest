import pytest
from splinter import Browser


@pytest.yield_fixture(scope='session')
def browser():
    b = Browser()
    yield b
    b.quit()


BASE_URL = 'http://localhost:5000'


def url(route):
    return '{}/{}'.format(BASE_URL, route)


# Edith has heard about a cool new online to-do app.
def test_can_check_homepage(browser):
    # She goes to check out its homepage
    browser.visit(url('/'))

    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title
    header = browser.find_by_tag('h1').first
    assert 'todos' in header.text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_by_id('new_todo_item').first
    assert inputbox['placeholder'] == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.type('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.type('\n')
    table = browser.find_by_id('id_list_table').first
    rows = table.find_by_tag('tr')
    assert any(row.text == '1: Buy peacock feathers' for row in rows), \
           'New to-do item did not appear in the table'

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    assert False, 'Finish all tests'

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep
