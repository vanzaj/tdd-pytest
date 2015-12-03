# Test driven development with pytest

[Test Driven Development with Python][book:TDDPy] book by  Harry Percival is a
nice practical introduction to TDD with Python in the web development context.
It shows the development of a simple [Django][web:django] based web app with
testing based on [unittest][pydoc:unittest] and [Selenium][web:selenium]. Very
common setup.  Here we will develop the same app using [Flask][web:flask] and
test it with [pytest][web:pytest] + [pytest-splinter][web:pytest-splinter]
and [pytest-bdd][web:pytest-bdd] extensions.

This guide is aimed at intermediate level developers with some experience in web
programming. "Intermediate" means familiarity with things like "url routing",
"http requests", "html templating" and the general MVC pattern.  There is little
explanation and comments about the code.  It is not a "translation" of Harry's
book.  Get and read the book or at least checkout the preface and some beginning
chapters to get more context.

[book:TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754
[pydoc:unittest]: https://docs.python.org/3.5/library/unittest.html
[web:django]: https://www.djangoproject.com/
[web:flask]: http://flask.pocoo.org/
[web:selenium]: http://www.seleniumhq.org/
[web:pytest]: http://pytest.org/
[web:pytest-splinter]: https://pypi.python.org/pypi/pytest-splinter
[web:pytest-bdd]: https://pypi.python.org/pypi/pytest-bdd


## Conventions

There are two types of code blocks:

command line -- what you need to type in a terminal (`$` indicates standard
[bash][web:bash] shell prompt)

```bash
$ whoami
ivan
$ python -V
Python 3.5.0
```

python code -- what you need to type inside a text editor (the first line
starting with `#` indicates the path to file relative to project's root directory.

```python
# path/to/tests/test_file.py
import pytest

def test_sanity():
    assert 2 + 2 == 4
```

[web:bash]: https://www.gnu.org/software/bash/
