# Test Driven Development with pytest

Gentle introduction to testing in the web programming context.
Somewhat inspired by [Test Driven Development with Python][book:TDDPy],
but using [Flask][web:flask], [pytest][web:pytest],
[pytest-splinter][web:pytest-splinter]
and eventually [pytest-bdd][web:pytest-bdd].

## How to contribute to the guide

```
git clone https://github.com/vanzaj/tdd-pytest
pip install -r requirements.txt
cd docs/tdd-pytest/
# edit or add inside content
make docs
# open http://localhost:8000
```


[book:TDDPy]: http://chimera.labs.oreilly.com/books/1234000000754
[web:flask]: http://flask.pocoo.org/
[web:pytest]: http://pytest.org/
[web:pytest-splinter]: https://pypi.python.org/pypi/pytest-splinter
[web:pytest-bdd]: https://pypi.python.org/pypi/pytest-bdd
