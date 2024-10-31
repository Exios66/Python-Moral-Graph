import pytest
from src.app import app
import json
from http import HTTPStatus
from typing import Dict, Any

@pytest.fixture
def client():
    """Test client fixture for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def validate_simulation_response(data: Dict[str, Any]) -> None:
    """Helper function to validate simulation response data"""
    required_fields = {
        'totalParticipants': int,
        'averageScore': float,
        'dimensionScores': dict,
        'completionRate': float,
        'totalInteractions': int,
        'averageInteractionsPerParticipant': int,
        'timestamp': str
    }
    
    for field, field_type in required_fields.items():
        assert field in data, f"Missing required field: {field}"
        assert isinstance(data[field], field_type), f"Invalid type for {field}"

def test_simulate_endpoint_valid_data(client):
    """Test simulation endpoint with valid participant count"""
    response = client.post(
        '/api/simulate',
        data=json.dumps({'participantCount': 100}),
        content_type='application/json'
    )
    
    assert response.status_code == HTTPStatus.OK
    data = json.loads(response.data)
    validate_simulation_response(data)
    
    # Additional validation
    assert 10 <= data['totalParticipants'] <= 10000
    assert 1.0 <= data['averageScore'] <= 5.0
    assert 0 <= data['completionRate'] <= 100
    assert data['totalInteractions'] > 0

def test_simulate_endpoint_invalid_data(client):
    """Test simulation endpoint with invalid inputs"""
    test_cases = [
        ({'participantCount': -1}, "Participant count must be between 10 and 10000"),
        ({'participantCount': 0}, "Participant count must be between 10 and 10000"),
        ({'participantCount': 10001}, "Participant count must be between 10 and 10000"),
        ({}, "Missing required parameter: participantCount"),
        ({'participantCount': "invalid"}, "Invalid participant count format")
    ]
    
    for test_input, expected_error in test_cases:
        response = client.post(
            '/api/simulate',
            data=json.dumps(test_input),
            content_type='application/json'
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.data)
        assert 'error' in data
        assert expected_error in data['error']

def test_simulate_endpoint_invalid_content_type(client):
    """Test simulation endpoint with invalid content type"""
    response = client.post(
        '/api/simulate',
        data='not-json-data',
        content_type='text/plain'
    )
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = json.loads(response.data)
    assert 'error' in data
    assert "Invalid content type" in data['error']