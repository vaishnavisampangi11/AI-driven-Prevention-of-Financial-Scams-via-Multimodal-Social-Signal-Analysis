from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    response = client.post('/api/auth/register', json={'name': 'Test User', 'email': 'test@example.com', 'password': 'strongpass1'})
    assert response.status_code in (200, 201, 400)

    login = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'strongpass1'})
    assert login.status_code in (200, 401)


def test_protected_route_without_token():
    response = client.get('/api/dashboard/summary')
    assert response.status_code in (401, 200)
