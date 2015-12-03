# TDD Basics

Here we will build a simple todo app following roughly the same steps as in the
Part I of [TDD with Python][book:TDDPy] book.

[book:TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754

## Project setup

Before anything else, we need to create the project's directory structure and
install minimal requirments into a `virtualenv`. Then create a "failing"
test, write a minimal Flask app, and get the test to pass.

```bash
$ cd ~/Projects
$ mkdir tdd-todoapp
$ cd tdd-todoapp
$ pyvenv venv
$ . venv/bin/activate
$ python -V
Python 3.5.0

$ pip install Flask
$ pip install pytest pytest-xdist pytest-splinter
```

Create the `app` and `tests` dirs:

```bash
$ mkdir todoapp && mkdir tests
$ touch tests/functional_tests.py
```

```python
# tests/functional_tests.py
from splinter import Browser

BASE_URL = 'http://localhost:5000'

with Browser() as browser:
    browser.visit(BASE_URL)
    assert browser.is_text_present('hello world')
```

Run the test and see it fail.

```
$ python tests/functional_test.py
Traceback (most recent call last):
  File "tests/functional_test.py", line 8, in <module>
      assert browser.is_text_present('hello world')
      AssertionError
```

Create a basic flask app:

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

At this point you should have the following files in your project dir:

```
├── setup.cfg
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
can be as simple as using comments to write a walkthrough the app's features by
an imaginary user. This is a variation on
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
`Pytest` is an alternative testing framework. It is arguably more "pythonic"
(requires less boilerplate code) and simpler to use. We can adapt
`functional_test.py` to test the "check homepage" feature as follows:

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

def _r(route):
    """ routing helper """
    if not route.startswith('/'):
        route = '/' + route
    return '%s%s' % (BASE_URL, route)


# Edith has heard about a cool new online to-do app.
# She goes to check out its homepage
def test_can_check_homepage(browser):
    browser.visit(_r('/'))
    assert browser.is_text_present('hello world')

# She notices the page title and header mention to-do lists
# ...
```

Note how the `browser` instance has been converted into a function decorated with
`yield_fixture`. This is the equivalent of `setUp()` and `tearDown()` methods
of a `unittest.TestCase`. Pytest fixtures are then passed to test functions as
arguments. It is possible to organize tests into classes, but it is not
required.

Before running `pytest`, create a `setup.cfg` to exclude `venv` (and other dirs
if needed) from being in the tests auto-discovery path.

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
