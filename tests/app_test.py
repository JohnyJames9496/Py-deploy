import pytest
from src.app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task_redirects(client):
    response = client.post('/add', data={'task_text': 'test task'})
    assert response.status_code == 302
