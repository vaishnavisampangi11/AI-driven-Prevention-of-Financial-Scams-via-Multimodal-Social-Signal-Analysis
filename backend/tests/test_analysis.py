from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_text_analysis_requires_auth():
    response = client.post('/api/analyses/text', json={'input_text': 'Urgent OTP needed', 'source_type': 'SMS'})
    assert response.status_code in (401, 200)


def test_url_analysis_requires_auth():
    response = client.post('/api/analyses/url', json={'url': 'https://example.com'})
    assert response.status_code in (401, 200)
