import pytest
import todoapp


@pytest.fixture(scope='session')
def client():
    todoapp.app.config['TESTING'] = True
    return todoapp.app.test_client()


def test_home_page_returns_correct_html(client):
    response = client.get('/')
    assert response.status == '200 OK'
    assert '<title>To-Do</title>' in str(response.data)
