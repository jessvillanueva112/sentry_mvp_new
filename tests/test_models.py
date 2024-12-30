import pytest
from app import db, Student, RiskAssessment

def test_create_student(app):
    student = Student(
        id="87654321",
        name="New Student",
        grade=11,
        email="new@school.edu"
    )
    db.session.add(student)
    db.session.commit()
    
    assert student.id == "87654321"
    assert student.name == "New Student"
    assert student.grade == 11
    assert student.email == "new@school.edu"

def test_create_assessment(app, sample_student):
    assessment = RiskAssessment(
        student_id=sample_student.id,
        risk_score="Low",
        circle_pattern="green",
        triangle_pattern="blue",
        square_pattern="green"
    )
    assessment.set_patterns(["academic_engagement", "motivation_loss"])
    db.session.add(assessment)
    db.session.commit()
    
    assert assessment.student_id == sample_student.id
    assert assessment.risk_score == "Low"
    assert assessment.circle_pattern == "green"
    assert assessment.get_patterns() == ["academic_engagement", "motivation_loss"]

def test_student_assessment_relationship(app, sample_student, sample_assessment):
    assert len(sample_student.assessments) == 1
    assert sample_student.assessments[0].id == sample_assessment.id
    assert sample_assessment.student.id == sample_student.id