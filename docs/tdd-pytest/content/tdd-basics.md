# TDD Basics

Here we will build a simple todo app following roughly the same steps as in the
Part I of [TDD with Python][book:TDDPy] book.

[book:TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754

## Project setup

Fist of all we need to create the project's directory structure and install
minimal requirements into a "virtualenv". Then we write the first test which
should obviously "fail" since there is no actual application code written at
this point. And then we write a minimal Flask app, just to get the test to pass.

```bash
$ cd ~/Projects
$ mkdir tdd-todoapp
$ cd tdd-todoapp
$ pyvenv venv
$ . venv/bin/activate
$ python -V
Python 3.5.

$ pip install Flask
$ pip install pytest pytest-splinter
```

Create the `app` and `tests` dirs:

```bash
$ mkdir todoapp tests
```

Edit `tests/functional_tests.py`:

```python
# tests/functional_tests.py
from splinter import Browser

BASE_URL = 'http://localhost:5000'

with Browser() as browser:
    browser.visit(BASE_URL)
    assert browser.is_text_present('hello world')
```

Run the test:

```
$ python tests/functional_test.py
Traceback (most recent call last):
  File "tests/functional_test.py", line 8, in <module>
      assert browser.is_text_present('hello world')
      AssertionError
```

`AssertionError` indicates test failure. Note that we haven't actually used
`pytest` yet. The file containing our first test is just a regular python
script[^1].


[^1]: Non-trivial apps will have many tests organized in multiple functions or
classes. That's when we need to use a "test runner" -- a command that discovers
and runs all the tests, and then reports which ones have passed or failed.

Now, create a basic flask app:

```python
# todoapp/__init__.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'

if __name__ == "__main__":
    app.run()
```

Open another terminal, activate `venv`, and run the app:

```bash
$ python todoapp/__init__.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Rerun the test and see it pass.
At this point you should have the following files in your project directory:

```
├── tests
│   └── functional_test.py
├── todoapp
│   └── __init__.py
└── venv
    ├── bin
    ├── include
	...
```

## Starting the actual app

We can use `functional_test.py` to guide the development of the todo app.  This
can be as simple as using comments to write a walk-through the app's features by
an imaginary user. This is a variation on the
"[Readme driven development][blog:RDD]" theme.

[blog:RDD]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

```python
# tests/functional_test.py
from splinter import Browser

BASE_URL = 'http://localhost:5000'

with Browser() as browser:
    browser.visit(BASE_URL)
    assert browser.is_text_present('hello world')


# Edith has heard about a cool new online to-do app.
# She goes to check out its homepage

# She notices the page title and header mention to-do lists

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep
```

`Unittest` is the standard Python module for creating and running tests.
`Pytest` is an alternative testing framework. It requires less boilerplate code
and is somewhat easier to use. We can adapt `functional_test.py` to test the
"check homepage" feature as follows:

```python
# tests/functional_test.py
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
# She goes to check out its homepage
def test_can_check_homepage(browser):
    browser.visit(url('/'))
    assert browser.is_text_present('hello world')

# She notices the page title and header mention to-do lists
# ...
```

Note how the `browser` instance has been converted into a function decorated
with `yield_fixture`[^2]. It does the job of both `setUp()` and `tearDown()`
methods of a `unittest.TestCase`. It is possible to organize tests into classes,
but it is not required.

[^2]: Pytest fixtures must be callable objects passed to test functions as
arguments. Inside a test function we get an instance of the return or yield
object.


Before running `pytest`, create a `setup.cfg` file to exclude `venv` (and other
dirs if needed) from being in the tests auto-discovery path.

```config
[pytest]
norecursedirs = .git venv
```

Now run the test (note that `pytest`'s runner is `py.test`):

```bash
$ py.test -v
=================================== test session starts ====================================
platform darwin -- Python 3.5.0, pytest-2.8.3, py-1.4.31, pluggy-0.3.1 -- /Users/ivan/Projects/tdd-todoapp/venv/bin/python3.5
cachedir: .cache
rootdir: /Users/ivan/Projects/tdd-todoapp, inifile: setup.cfg
plugins: splinter-1.7.0, xdist-1.13.1
collected 1 items

tests/functional_test.py::test_can_check_homepage PASSED

======================= 1 passed, 1 pytest-warnings in 2.34 seconds ========================
```

Use `py.test -ra` if you want to see what is causing `pytest-warnings`.

Back to the app. "hello world" is nice, but it has little to do with a todo app.
The test should look more like:

```python
# Edith has heard about a cool new online to-do app.
def test_can_check_homepage(browser):
    # She goes to check out its homepage
    browser.visit(url('/'))
    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title
```

```bash
$ py.test
<... skipped lines ...>
========================================= FAILURES =========================================
_________________________________ test_can_check_homepage __________________________________

browser = <splinter.driver.webdriver.firefox.WebDriver object at 0x106a3d7b8>

    def test_can_check_homepage(browser):
        # She goes to check out its homepage
        browser.visit(url('/'))
        # She notices the page title and header mention to-do lists
>       assert 'To-Do' in browser.title
E       assert 'To-Do' in ''
<... skipped lines ...>
```

Note the last line. It shows the actual value of `browser.title` during the
test run. Time to update the app:

```bash
$ mkdir todoapp/templates
$ touch todoapp/templates/home.html
```

```html
<!-- todoapp/templates/home.html -->
<html>
<head>
  <title>To-Do</title>
</head>

<body>
  <h1>My todos list</h1>
</body>

</html>
```

```python
# todoapp/__init__.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
```

`py.test` should now pass.


## Unit tests vs functional tests

The tests so far are called "functional" because they test an application from
the perspective of a user; open a browser, visit a url, etc. These tests work
without any knowledge about the app's implementation details. Almost any kind of
web application, written in Python or another language, can be tested with
`pytest` and `splinter`. On the other hand, unit tests (the concept and not the
`unittest` module) are supposed to test an application from the developer's
point of view. Unit tests should cover very specific and usually very small
parts of code. Therefore, there should be many more unit tests than functional
tests.  Because of that unit tests must be fast. Opening and closing browsers is
not very useful in this context. As described in the TDDPy book, the development
process goes as follows:

1. Start by writing a functional test, describing the new functionality from
    the user's point of view.
2. Once we have a functional test that fails, we start to think about how to
	write code that can get it to pass (or at least to get past its current
	failure). We now use one or more unit tests to define how we want our code to
	behave -- the idea is that each line of production code we write should be
    tested by (at least) one of our unit tests.
3. Once we have a failing unit test, we write the smallest amount of
	application code we can, just enough to get the unit test to pass. We may
	iterate between steps 2 and 3 a few times, until we think the functional test
	will get a little further.
4. Now we can rerun our functional tests and see if they pass, or get a little
	further. That may prompt us to write some new unit tests, and some new code,
	and so on.

Let's create a unit test for the todo app using flask's test client[^3] which
does the same thing as the `test_can_check_homepage()` inside
`functional_test.py`:

[^3]: "client" is a generic way to refer to code or application running on the
user's side (like web browsers) in the client-server software design model.

```python
# tests/unit_test.py

import pytest
from todoapp import app

@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_home_page_returns_correct_html(client):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    assert '<title>To-Do</title>' in rsp.get_data(as_text=True)
```

and run it

```bash
$ py.test tests/unit_test.py
========================================== ERRORS ==========================================
___________________________ ERROR collecting tests/unit_test.py ____________________________
tests/unit_test.py:2: in <module>
    import todoapp
E   ImportError: No module named 'todoapp'
```

The app's module is not in the Python's path, so `pytest` can't import it. The
simplest way to fix this is to set the `PYTHONPATH` shell variable to the
current dir:

```bash
$ export PYTHONPATH='.'

$ py.test -v tests/unit_test.py
=================================== test session starts ====================================

tests/unit_test.py::test_home_page_returns_correct_html PASSED

======================= 1 passed, 1 pytest-warnings in 0.02 seconds
```

0.02 seconds is much better compared to 2.5 seconds needed to start a browser.

Since we know that the `home` view should return `home.html` template,
we can check the returned html as follows:

```python
def test_home_page_returns_correct_html(client):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    tpl = app.jinja_env.get_template('home.html')
    assert tpl.render() == rsp.get_data(as_text=True)
```

At this point your project dir should look like (excluding `*.pyc` and
`__pycache__` dir):

```
├── setup.cfg
├── tests
│   ├── functional_test.py
│   └── unit_test.py
├── todoapp
│   ├── __init__.py
│   └── templates
│       └── home.html
└── venv
    └── bin
...
```


## Testing user interactions

Time to get back to functional tests. The next step is to add user input
functionality. This means adding `<form>` and `<input>` elements in the app's
html template. Let's do an explicit test for this inside `tests/unit_test.py`
instead of testing full template:

```python
def test_home_page_returns_correct_html(client):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<form' in html
    assert '<input' in html
```

Think about why we didn't "close" the elements.

Update the html template to make the test pass.

```html
<!-- todoapp/templates/home.html -->

<body>
  <h1>My todos list</h1>
  <form>
    <input id="new_todo_item" name="todo_text"/>
  </form>
  </table>
</body>
```

We can now update our functional test:

```python
# tests/function_test.html

# ...

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

    # She types "Buy peacock feathers" into a text box
    inputbox.type('Buy peacock feathers')

    # When she hits enter...
    inputbox.type('\n')

    # ...the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
```

What-you-type-is-what-you-get...

At this point we need to decide what to do when the user hits "Enter" preferably
without resorting to [css tricks][SO:form-wo-submit] and javascript. Turns out
that an html form containing a single `<input>` is implicitly submitted on
"Enter"[^4]. All we need to do is to specify that submit method is "POST" and to
add a list or table to the template which will display submitted todo items. But
write the tests first!

[SO:form-wo-submit]: http://stackoverflow.com/questions/477691/submitting-a-form-by-pressing-enter-without-a-submit-button

[^4]: Introduced in HTML 2.0, and currently described under
      [implicit submission](http://www.w3.org/TR/html5/forms.html#form-submission-0)
      section of HTML 5 specification.

```python
# tests/unit_test.py

def test_home_page_returns_correct_html(client):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<form' in html
    assert '<input' in html
    assert '<table' in html

def test_home_page_accepts_post_request(client):
    rsp = client.post('/', data={"todo_text": "do something useful"})
    assert rsp.status == '200 OK'
    assert 'do something useful' in rsp.get_data(as_text=True)
```

Now update the template.

```html
<!-- todoapp/templates/home.html -->
<body>
  <h1>My todos list</h1>
  <form method="POST">
    <input id="new_todo_item" name="todo_text"/>
  </form>

  <table id="todo_list_table"></table>
</body>
```

Run unit tests.

```bash
$ py.test tests/unit_test.py
================================ test session starts =================================

    def test_home_page_accepts_post_request(client):
        rsp = client.post('/')
>       assert rsp.status == '200 OK'
E       assert '405 METHOD NOT ALLOWED' == '200 OK'
E         - 405 METHOD NOT ALLOWED
E         + 200 OK

tests/unit_test.py:21: AssertionError
=============== 1 failed, 1 passed, 1 pytest-warnings in 0.03 seconds ================

```

Flask routes accept only "GET" requests by default, but this is easily changed
using `methods` keyword. We will also need to import flask's `request` object.


```python
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_item = request.form.get('todo_text')
        return 'got new item: %s' % new_item
    return render_template('home.html')
```





If you want a more explicit error message, change the assertion line like this:

```python

    assert any(row.text == '1: Buy peacock feathers' for row in rows), \
           'New to-do item did not appear in the table'

```
