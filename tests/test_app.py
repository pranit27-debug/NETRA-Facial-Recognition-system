import os
import pytest
import json
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert 'NETRA' in data['status']

def test_detect_faces_no_image(client):
    """Test face detection with no image provided"""
    response = client.post('/detect')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_detect_faces_invalid_file(client):
    """Test face detection with invalid file type"""
    response = client.post('/detect', data={
        'image': (b'Test file content', 'test.txt')
    }, content_type='multipart/form-data')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

# Note: Add more tests for actual face detection once we have test images
