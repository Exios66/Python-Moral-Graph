import pytest
from src.app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_simulate_endpoint(client):
    # Test with valid data
    response = client.post('/api/simulate',
                          data=json.dumps({'participantCount': 10}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'totalParticipants' in data
    assert 'averageScore' in data
    assert 'dimensionScores' in data

    # Test with invalid data
    response = client.post('/api/simulate',
                          data=json.dumps({'participantCount': -1}),
                          content_type='application/json')
    assert response.status_code == 500 