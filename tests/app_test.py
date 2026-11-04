import os
os.environ.setdefault("DB_URL", "sqlite:///test.db")

from src.app import app, db

def test_index_page_loads():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_add_task():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.post('/add', data={'task_text': 'Test task'})
    assert response.status_code == 302
