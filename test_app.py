import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_records(client):
    response = client.get('/api/v1/records')
    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] == 2

def test_get_single_record(client):
    response = client.get('/api/v1/records/1')
    assert response.status_code == 200

def test_record_not_found(client):
    response = client.get('/api/v1/records/99')
    assert response.status_code == 404