from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
import string
import names  # You'll need to pip install names

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    grade_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assessments = db.relationship('RiskAssessment', backref='student', lazy=True)

class RiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    academic_performance = db.Column(db.Float)
    attendance_rate = db.Column(db.Float)
    behavioral_incidents = db.Column(db.Integer)
    social_emotional_score = db.Column(db.Float)
    risk_patterns = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/student/<student_id>')
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    latest_assessment = RiskAssessment.query.filter_by(student_id=student_id).order_by(RiskAssessment.created_at.desc()).first()
    
    student_data = {
        'id': student.id,
        'name': student.name,
        'grade_level': student.grade_level
    }
    
    if latest_assessment:
        student_data['latest_assessment'] = {
            'academic_performance': latest_assessment.academic_performance,
            'attendance_rate': latest_assessment.attendance_rate,
            'behavioral_incidents': latest_assessment.behavioral_incidents,
            'social_emotional_score': latest_assessment.social_emotional_score,
            'patterns': eval(latest_assessment.risk_patterns) if latest_assessment.risk_patterns else {}
        }
    
    return jsonify(student_data)

@app.route('/api/assess', methods=['POST'])
def assess_risk():
    data = request.get_json()
    student_id = data.get('studentId')
    risk_factors = data.get('patterns', [])
    
    # Calculate metrics based on risk factors
    academic_performance = random.uniform(0.6, 1.0) if 'low_grades' not in risk_factors else random.uniform(0.3, 0.6)
    attendance_rate = random.uniform(0.8, 1.0) if 'frequent_absences' not in risk_factors else random.uniform(0.5, 0.8)
    behavioral_incidents = random.randint(0, 2) if 'disruptive_behavior' not in risk_factors else random.randint(3, 8)
    social_emotional_score = random.uniform(0.7, 1.0) if 'social_isolation' not in risk_factors else random.uniform(0.4, 0.7)
    
    # Determine risk patterns
    patterns = {
        'circle': 'red' if academic_performance < 0.6 else 'yellow' if academic_performance < 0.8 else 'green',
        'triangle': 'red' if attendance_rate < 0.7 else 'yellow' if attendance_rate < 0.9 else 'green',
        'square': 'red' if behavioral_incidents > 5 else 'yellow' if behavioral_incidents > 2 else 'green'
    }
    
    # Create new assessment
    assessment = RiskAssessment(
        student_id=student_id,
        academic_performance=academic_performance,
        attendance_rate=attendance_rate,
        behavioral_incidents=behavioral_incidents,
        social_emotional_score=social_emotional_score,
        risk_patterns=str(patterns)
    )
    
    db.session.add(assessment)
    db.session.commit()
    
    return jsonify({
        'metrics': {
            'academic_performance': academic_performance,
            'attendance_rate': attendance_rate,
            'behavioral_incidents': behavioral_incidents,
            'social_emotional_score': social_emotional_score
        },
        'patterns': patterns
    })

@app.route('/api/generate-student', methods=['GET'])
def generate_student():
    # Generate a random 8-digit student ID
    while True:
        student_id = ''.join(random.choices(string.digits, k=8))
        if not Student.query.get(student_id):
            break
    
    # Create new student with random data
    student = Student(
        id=student_id,
        name=names.get_full_name(),
        grade_level=random.randint(9, 12)
    )
    
    # Generate initial assessment with random metrics
    assessment = RiskAssessment(
        student_id=student_id,
        academic_performance=random.uniform(0.6, 1.0),
        attendance_rate=random.uniform(0.7, 1.0),
        behavioral_incidents=random.randint(0, 5),
        social_emotional_score=random.uniform(0.5, 1.0)
    )
    
    # Calculate initial patterns
    patterns = {
        'circle': 'red' if assessment.academic_performance < 0.6 else 'yellow' if assessment.academic_performance < 0.8 else 'green',
        'triangle': 'red' if assessment.attendance_rate < 0.7 else 'yellow' if assessment.attendance_rate < 0.9 else 'green',
        'square': 'red' if assessment.behavioral_incidents > 5 else 'yellow' if assessment.behavioral_incidents > 2 else 'green'
    }
    assessment.risk_patterns = str(patterns)
    
    try:
        db.session.add(student)
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'id': student.id,
            'name': student.name,
            'grade_level': student.grade_level,
            'metrics': {
                'academic_performance': assessment.academic_performance,
                'attendance_rate': assessment.attendance_rate,
                'behavioral_incidents': assessment.behavioral_incidents,
                'social_emotional_score': assessment.social_emotional_score
            },
            'patterns': patterns
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 