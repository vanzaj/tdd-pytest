import pytest
from todoapp import app


@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_home_page_returns_correct_html(client):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<form' in html
    assert '<input' in html


def test_home_page_accepts_post_request(client):
    rsp = client.post('/', data={"todo_text": "do something useful"})
    assert rsp.status == '200 OK'
    assert 'do something useful' in rsp.get_data(as_text=True)
