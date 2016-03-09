# Test driven development with pytest

[Test Driven Development with Python][book:HP-TDDPy] book by  Harry Percival is
a nice practical introduction to TDD with Python in the web development context.
It starts with the development of a simple [Django][web:django] based web app
using [unittest][pydoc:unittest] and [Selenium][web:selenium] for testing. Very
common setup.  Here we will develop the same app using [Flask][web:flask] and
test it with [pytest][web:pytest] + [pytest-splinter][web:pytest-splinter] and
[pytest-bdd][web:pytest-bdd] extensions.

This guide is aimed at developers with some experience in Python and web
programming. This means some familiarity with things like "url routing", "http
requests", "html templating" and the general MVC pattern. Basic knowledge about
how to use the command line interface (we'll use `bash`) is also assumed.

This is a very basic how-to-get-started-with-testing guide. Hopefully enough to
overcome the initial learning barrier. I'm not a "testing expert", and I don't
want to get into why anybody should be doing TDD or get into the depths of
what's a "unit", "functional", "acceptance" or "integration" test. You can read
more about testing in Harry's book, [wikipedia][wiki:TDD] and other
authoritative sources like [this one][c2:TDD] or [that one][book:KB-TDD].
<http://gojko.net/> is another useful resource.

Both this guide and the source of the app are on [GitHub](https://github.com/vanzaj/tdd-pytest).

[book:HP-TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754
[pydoc:unittest]: https://docs.python.org/3.5/library/unittest.html
[web:django]: https://www.djangoproject.com/
[web:flask]: http://flask.pocoo.org/
[web:selenium]: http://www.seleniumhq.org/
[web:pytest]: http://pytest.org/
[web:pytest-splinter]: https://pypi.python.org/pypi/pytest-splinter
[web:pytest-bdd]: https://pypi.python.org/pypi/pytest-bdd
[wiki:TDD]: https://en.wikipedia.org/wiki/Test-driven_development
[c2:TDD]: http://c2.com/cgi/wiki?TestDrivenDevelopment
[book:KB-TDD]: http://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530

## Conventions

There are two types of code blocks:

command line -- what you need to type in a terminal (`$` indicates standard
[bash][web:bash] shell prompt),

```bash
$ whoami
ivan
$ python -V
Python 3.5.0
```

and Python code -- what you need to type inside a text editor (the first line
starting with `#` indicates the path to file relative to project's root
directory.

```python
# path/to/tests/test_file.py
import pytest

def test_sanity():
    assert 2 + 2 == 4
```

[web:bash]: https://www.gnu.org/software/bash/
