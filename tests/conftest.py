import pytest
from app import app as flask_app, db, Student, RiskAssessment

@pytest.fixture
def app():
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["TESTING"] = True
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_student(app):
    student = Student(
        id="12345678",
        name="Test Student",
        grade=10,
        email="test@school.edu"
    )
    db.session.add(student)
    db.session.commit()
    return student

@pytest.fixture
def sample_assessment(app, sample_student):
    assessment = RiskAssessment(
        student_id=sample_student.id,
        risk_score="Medium",
        circle_pattern="yellow",
        triangle_pattern="green",
        square_pattern="blue"
    )
    assessment.set_patterns(["academic_engagement", "attendance_poor"])
    db.session.add(assessment)
    db.session.commit()
    return assessment