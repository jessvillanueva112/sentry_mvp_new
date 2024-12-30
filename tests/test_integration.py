import pytest
import json
import threading
from datetime import datetime, timedelta
from app import app, db, Student, Assessment

@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown the database for each test."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_complete_assessment_workflow(test_client):
    """Test complete workflow from student generation to assessment"""
    try:
        # Step 1: Generate new student
        response = test_client.get('/api/generate-student')
        assert response.status_code == 200, "Failed to generate student"
        student_data = json.loads(response.data)
        student_id = student_data['id']
        
        # Step 2: Verify student creation in database
        with app.app_context():
            student = Student.query.get(student_id)
            assert student is not None, "Student not found in database"
            assert student.name == student_data['name'], "Student name mismatch"
            
        # Step 3: Submit assessment
        assessment_data = {
            'studentId': student_id,
            'patterns': ['connection', 'engagement', 'learning']
        }
        response = test_client.post('/api/assess',
                                   data=json.dumps(assessment_data),
                                   content_type='application/json')
        assert response.status_code == 200, "Assessment submission failed"
        assessment_result = json.loads(response.data)
        
        # Step 4: Verify assessment in database
        with app.app_context():
            student = Student.query.get(student_id)
            assert len(student.assessments) == 2, "Incorrect number of assessments"
            latest_assessment = student.assessments[0]
            assert latest_assessment.get_patterns() == assessment_result['patterns'], "Pattern mismatch"
    except Exception as e:
        pytest.fail(f"Complete workflow test failed: {str(e)}")

def test_multiple_assessments_tracking(test_client):
    """Test tracking multiple assessments for a student"""
    try:
        # Generate student
        response = test_client.get('/api/generate-student')
        assert response.status_code == 200, "Failed to generate student"
        student_data = json.loads(response.data)
        student_id = student_data['id']
        
        # Submit multiple assessments
        patterns = [
            ['connection', 'engagement'],
            ['learning', 'connection'],
            ['engagement', 'learning']
        ]
        
        for pattern_set in patterns:
            assessment_data = {
                'studentId': student_id,
                'patterns': pattern_set
            }
            response = test_client.post('/api/assess',
                                       data=json.dumps(assessment_data),
                                       content_type='application/json')
            assert response.status_code == 200, f"Failed to submit assessment with patterns {pattern_set}"
        
        # Verify all assessments are recorded
        with app.app_context():
            student = Student.query.get(student_id)
            assert len(student.assessments) == 4, "Incorrect number of assessments"
            
            # Verify chronological order and timestamps are within expected range
            timestamps = [a.timestamp for a in student.assessments]
            assert timestamps == sorted(timestamps, reverse=True), "Assessments not in chronological order"
            
            time_range = datetime.utcnow() - timedelta(minutes=5)
            assert all(ts >= time_range for ts in timestamps), "Assessment timestamps outside expected range"
    except Exception as e:
        pytest.fail(f"Multiple assessments test failed: {str(e)}")

def test_risk_calculation_consistency(test_client):
    """Test consistency of risk calculations across assessments"""
    try:
        # Generate two students
        response1 = test_client.get('/api/generate-student')
        response2 = test_client.get('/api/generate-student')
        assert response1.status_code == 200 and response2.status_code == 200, "Failed to generate students"
        
        student1_data = json.loads(response1.data)
        student2_data = json.loads(response2.data)
        
        # Submit identical assessments
        assessment_data = {
            'patterns': ['connection', 'engagement', 'learning']
        }
        
        # Assess both students
        for student_data in [student1_data, student2_data]:
            assessment_data['studentId'] = student_data['id']
            response = test_client.post('/api/assess',
                                       data=json.dumps(assessment_data),
                                       content_type='application/json')
            assert response.status_code == 200, f"Failed to assess student {student_data['id']}"
        
        # Compare results
        result1 = json.loads(test_client.get(f"/api/student/{student1_data['id']}").data)
        result2 = json.loads(test_client.get(f"/api/student/{student2_data['id']}").data)
        
        # Verify metric consistency
        metrics = ['academic_performance', 'attendance_rate', 'social_emotional_score']
        for metric in metrics:
            diff = abs(result1['latest_assessment'][metric] - result2['latest_assessment'][metric])
            assert diff < 0.1, f"Inconsistent {metric} calculations"
    except Exception as e:
        pytest.fail(f"Risk calculation consistency test failed: {str(e)}")

def test_data_persistence_across_sessions(test_client):
    """Test data persistence across multiple sessions"""
    try:
        # First session: Create student and assessment
        response = test_client.get('/api/generate-student')
        assert response.status_code == 200, "Failed to generate student"
        student_data = json.loads(response.data)
        student_id = student_data['id']
        
        assessment_data = {
            'studentId': student_id,
            'patterns': ['connection', 'engagement']
        }
        response = test_client.post('/api/assess',
                                   data=json.dumps(assessment_data),
                                   content_type='application/json')
        assert response.status_code == 200, "Failed to submit initial assessment"
        
        # Simulate new session
        with app.test_client() as new_client:
            response = new_client.get(f'/api/student/{student_id}')
            assert response.status_code == 200, "Failed to retrieve student in new session"
            
            retrieved_data = json.loads(response.data)
            assert retrieved_data['id'] == student_id, "Student ID mismatch"
            assert retrieved_data['name'] == student_data['name'], "Student name mismatch"
            assert retrieved_data['latest_assessment'] is not None, "Missing assessment data"
            assert len(retrieved_data['latest_assessment']['patterns']) > 0, "Missing pattern data"
    except Exception as e:
        pytest.fail(f"Data persistence test failed: {str(e)}")

def test_concurrent_assessments(test_client):
    """Test handling of concurrent assessments"""
    try:
        # Generate student
        response = test_client.get('/api/generate-student')
        assert response.status_code == 200, "Failed to generate student"
        student_data = json.loads(response.data)
        student_id = student_data['id']
        
        # Prepare assessment data
        assessment_data = {
            'studentId': student_id,
            'patterns': ['connection', 'engagement']
        }
        
        # Simulate concurrent requests
        responses = []
        threads = []
        
        def make_request():
            try:
                with app.test_client() as client:
                    response = client.post('/api/assess',
                                         data=json.dumps(assessment_data),
                                         content_type='application/json')
                    responses.append(response)
            except Exception as e:
                pytest.fail(f"Concurrent request failed: {str(e)}")
        
        # Create and start threads
        for _ in range(3):
            thread = threading.Thread(target=make_request)
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10)
            assert not thread.is_alive(), "Thread timeout occurred"
        
        # Verify responses
        assert all(r.status_code == 200 for r in responses), "Some concurrent requests failed"
        
        # Verify database consistency
        with app.app_context():
            student = Student.query.get(student_id)
            assert student is not None, "Student not found after concurrent requests"
            assert len(student.assessments) == 4, "Incorrect number of assessments after concurrent requests"
            
            # Verify assessment integrity
            patterns = [assessment.get_patterns() for assessment in student.assessments]
            assert all(isinstance(p, dict) for p in patterns), "Invalid pattern data in assessments"
    except Exception as e:
        pytest.fail(f"Concurrent assessments test failed: {str(e)}") 