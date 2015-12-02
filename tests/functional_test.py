from splinter import Browser


BASE_URL = 'http://localhost:5000'

with Browser() as browser:
    browser.visit(BASE_URL)
    assert browser.is_text_present('hello world')
