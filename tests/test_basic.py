
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code in (200, 302)  # Pode redirecionar para login

def test_auth_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_admin_route(client):
    response = client.get('/admin')
    assert response.status_code in (200, 302)

def test_main_route(client):
    response = client.get('/main')
    assert response.status_code in (200, 302)

def test_list_route(client):
    response = client.get('/list')
    assert response.status_code in (200, 302)
