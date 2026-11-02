from src.app import app

def test_index_returns_200():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_add_task_redirects():
    client = app.test_client()
    response = client.post('/add', data={'task_text': 'test task'})
    assert response.status_code == 302
