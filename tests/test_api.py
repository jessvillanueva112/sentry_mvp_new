import json
import pytest
from app import app, db, Student, Assessment

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.session.remove()
        db.drop_all()

def test_index_route(client):
    """Test the index route returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_generate_student_api(client):
    """Test student generation endpoint"""
    response = client.get('/api/generate-student')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert 'name' in data
    assert 'grade' in data
    assert 'initial_assessment' in data

def test_get_student_api(client):
    """Test getting student details"""
    # First create a student
    gen_response = client.get('/api/generate-student')
    student_data = json.loads(gen_response.data)
    student_id = student_data['id']

    # Then retrieve the student
    response = client.get(f'/api/student/{student_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == student_id
    assert data['name'] == student_data['name']

def test_get_nonexistent_student(client):
    """Test getting a student that doesn't exist"""
    response = client.get('/api/student/999999')
    assert response.status_code == 404

def test_assess_patterns_api(client):
    """Test pattern assessment endpoint"""
    # First create a student
    gen_response = client.get('/api/generate-student')
    student_data = json.loads(gen_response.data)
    student_id = student_data['id']

    # Submit an assessment
    assessment_data = {
        'studentId': student_id,
        'patterns': ['connection', 'engagement', 'learning']
    }
    response = client.post('/api/assess',
                          data=json.dumps(assessment_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'patterns' in data
    assert 'metrics' in data
    assert 'descriptions' in data

def test_assess_invalid_student(client):
    """Test assessment with invalid student ID"""
    assessment_data = {
        'studentId': '999999',
        'patterns': ['connection', 'engagement', 'learning']
    }
    response = client.post('/api/assess',
                          data=json.dumps(assessment_data),
                          content_type='application/json')
    assert response.status_code == 404

def test_assess_missing_data(client):
    """Test assessment with missing data"""
    response = client.post('/api/assess',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400 