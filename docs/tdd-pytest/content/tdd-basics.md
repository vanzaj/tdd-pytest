# TDD Basics

Here we will build a simple todo app following roughly the same steps as in the
Part I of [TDD with Python][book:TDDPy] book.

[book:TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754

## Project setup

Fist of all we need to create the project's directory structure and install
minimal requirements into a "virtualenv". Then we write the first test which
should obviously "fail" since there is no actual application code written at
this point. And then we write a minimal Flask app, to get the test to pass.

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

Manual testing of a web application usually involves the following steps:

1. open a web browser
2. navigate to some url
3. check some page rendering detail
4. close the browser

Here is how to do this with [splinter](https://splinter.readthedocs.org/):

```python
# tests/functional_test.py

from splinter import Browser

browser = Browser()
url = 'http://localhost'
browser.visit(url)
assert browser.is_text_present('hello world')
browser.quit()
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

Now, let's create a basic flask app:

```python
# todoapp/__init__.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()
```

Open another terminal, activate `venv`, and run the app:

```bash
$ python todoapp/__init__.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Rerun the test and see it... fail. By default flask apps are running on port
5000. Fix the `url` in `functional_test.py` to take that into account, rerun
the test, and now it should pass.

At this point you should have the following files in your project's directory:

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

We can use `functional_test.py` to guide the development of our todo app. This
can be as simple as using comments to write a walk-through the app's features by
an imaginary user. This is a variation on the
"[Readme driven development][blog:RDD]" theme.

[blog:RDD]: http://tom.preston-werner.com/2010/08/23/readme-driven-development.html

```python
# tests/functional_test.py

from splinter import Browser

browser = Browser()
url = 'http://localhost:5000'

# Edith has heard about a cool new online to-do app.
# She goes to check out its homepage
browser.visit(url)

# She notices the page title and header mention to-do lists
assert 'Todo' in browser.title
header = browser.find_by_tag('h1').first
assert 'Todo list' in header.text

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# ...
browser.quit()
```

We don't need to figure out how to test all the features at once.
Thinking about 2 or 3 "next" features provides enough context to start
implementing the app. But before doing that, we need to discuss about the
difference between "functional" and "unit" tests.


### Functional vs unit tests

Considering an application from a user's perspective helps to stay focused on
building what's actually needed. Writing tests from the same perspective allows
verification that those needed parts of the app behave or function as intended.
Hence they are called **functional** tests. Note that there is no reference to
`flask` anywhere in `funcational_test.py`. The user is not expected to know
anything about the app's implementation details. He or she is only interested in
functionality. The developer, on the other hand, must make all the technical
implementation decisions, which framework to use, how to organize the code...
Actual application code also need to be tested, and done so from the
developper's perspective. Such tests are called **unit** tests. "Unit" refers to
a "unit of software code". Usually it means a function (`def foo():...`) or a on
object's method, but there isn't really a more precise or agreed upon definition
of "unit of code".


### Unittest vs pytest

`Unittest` is the standard Python module for creating and running tests. The
name is confusing because this module is used to write both "unit" and
"functional" tests. `Pytest` is an alternative testing package. It can also be
used to write both "unit" and "functional" tests. The syntax for writing tests
using `pytest` requires less boilerplate code compared to `unittest`, and it
feels more in line with "Simple is better than complex" (see
[pep20](https://www.python.org/dev/peps/pep-0020/)). `Pytest` also performs test
discovery, execution, and reporting. In that sense, it is an alternative to
`unittest` + [`nose`](https://nose.readthedocs.org/) combination.

Enough "theory", back to the app. We need to change our "hello world" app into
a "todo" app. According to our first couple of functional requirments, the app
should return an html page with a title and a header containing "Todo" text.
It is very simple to do this in `flask`, but let's write a unit test for it
first. Test-driven means test code first, actual code later.

```python
# tests/unit_test.py

from todoapp import app

def test_home_page_header():
    client = app.test_client()
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    assert '<title>Todo</title>' in rsp.get_data(as_text=True)
    assert '<h1>Todo list</h1>' in rsp.get_data(as_text=True)
```

This looks quite similar to our function test except that we are using `flask`'s
built-in test client[^2] and checking explicitly for a valid HTTP response code.
Also, the test is written as a function. This is how tests (both unit and
functional) are usually created when using `pytest`.  `Pytest` comes with a
`py.test` command which discovers and runs the tests. Without arguments, it
looks recursively for `tests/` directories and `*_test.py` files , and executes
any function or method with a `test` inside it's name. For now we want to run
only the unit tests.

[^2]: "client" is a generic way to refer to code or application running on the
user's side (like web browsers) in the client-server software design model.

```bash
$ py.test tests/unit_test.py
============================= test session starts ==============================
... skip lines ...
_____________________ ERROR collecting tests/unit_test.py ______________________
tests/unit_test.py:2: in <module>
    from todoapp import app
E   ImportError: No module named 'todoapp'
================== 1 pytest-warnings, 1 error in 0.01 seconds ==================
```

The app's module is not in the Python's path. The simplest way to fix this is
to set the `PYTHONPATH` shell variable to the current dir:

```bash
$ export PYTHONPATH='.'
$ py.test tests/unit_test.py
=================================== FAILURES ===================================
____________________________ test_home_page_header _____________________________

    def test_home_page_header():
        client = app.test_client()
        rsp = client.get('/')
        assert rsp.status == '200 OK'
>       assert '<title>Todo</title>' in rsp.get_data(as_text=True)
E       assert '<title>Todo</title>' in 'hello world'

tests/unit_test.py:8: AssertionError
================= 1 failed, 1 pytest-warnings in 0.02 seconds ==================
```

So, the app responds to a GET request, but of course it is not returning any
html. Note that we don't need to have the app running while executing unit
tests. Let's fix the app:

```python
# todoapp/__init__.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
```

And create a page template.

```bash
$ mkdir todoapp/templates
```

```html
<!-- todoapp/templates/home.html -->

<html>
<head>
  <title>Todo</title>
</head>
<body>
  <h1>Todo list</h1>
</body>
</html>
```

Rerun the test with a verbose flag on.

```bash
$ py.test -v tests/unit_test.py
============================= test session starts ==============================
... skip lines ...
collected 1 items

tests/unit_test.py::test_home_page_header PASSED

================= 1 passed, 1 pytest-warnings in 0.03 seconds ==================
```

Use `py.test -ra` if you want to see what is causing `pytest-warnings`.  If you
start the app and run `$py.test tests/function_test.py` it should also pass
without failing. It's time to add more functional tests.


-----

*Big reorg: half-backed bits and pieces below*


One "small" problem with the above approach is that `browser` is a global object
whose state could be modifed by different test functions. Global variables are
particularly bad in the testing context where we must be sure that the same test
functions are always executed under identical conditions. To ensure this, each
test function should create and destroy it's context. To avoid code repetition,
we can use pytest's [fixtures](https://pytest.org/latest/fixture.html)[^2]:

[^2]: yield fixtures allow very simple setup/teardown syntax

```python
# tests/functional_tests.py
import pytest
from splinter import Browser

@pytest.yield_fixture(scope='session')
def browser():
    b = Browser()
    yield b
    b.quit()

url = 'http://localhost:5000'

# Edith has heard about a cool new online to-do app.
# She goes to check out its homepage
def test_check_homepage(browser):
    browser.visit(url)
    assert browser.is_text_present('???')

# She notices the page title and header mention to-do lists
def test_todo_in_page_title(browser):
    browser.visit(url)
    assert 'Todo' in browser.title
```

We can run these two tests using `$ py.test tests/functional_tests.py`.  Of
course both assertions will fail. We also notice that opening and closing a
browser takes a couple of seconds.



----

On the other hand, unit tests (the concept and not the
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



----

If you want a more explicit error message, change the assertion line like this:

```python

    assert any(row.text == '1: Buy peacock feathers' for row in rows), \
           'New to-do item did not appear in the table'

```
