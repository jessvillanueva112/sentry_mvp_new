from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    violence_incidents = db.Column(db.PickleType, nullable=True)
    counselor_notes = db.Column(db.PickleType, nullable=True)
    risk_level = db.Column(db.String(50), default='Low')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'risk_level': self.risk_level,
            'violence_incidents': self.violence_incidents or [],
            'counselor_notes': self.counselor_notes or []
        }

class Counselor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(255), nullable=False)
    assigned_students = db.relationship('Student', backref='counselor', lazy=True)

class SupportPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    interventions = db.Column(db.PickleType, nullable=True)
    stakeholders = db.Column(db.PickleType, nullable=True)

class RiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    poverty_level = db.Column(db.String(50), nullable=True)
    mental_health_issues = db.Column(db.PickleType, nullable=True)
    behavioral_patterns = db.Column(db.PickleType, nullable=True)
    risk_score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    external_health_score = db.Column(db.Float, nullable=True)
    incident_count = db.Column(db.Integer, default=0)
    family_risk_factors = db.Column(db.PickleType, nullable=True)
    safety_plan_status = db.Column(db.String(50), default='none')
    
    def calculate_risk_score(self):
        score = 0
        weights = {
            'poverty_level': 0.2,
            'mental_health': 0.25,
            'behavioral': 0.25,
            'external_health': 0.15,
            'incidents': 0.15
        }
        
        if self.poverty_level == 'High':
            score += weights['poverty_level']
        
        if self.mental_health_issues:
            score += min(len(self.mental_health_issues) * 0.1, weights['mental_health'])
            
        if self.behavioral_patterns:
            score += min(len(self.behavioral_patterns) * 0.1, weights['behavioral'])
            
        if self.external_health_score:
            score += (100 - self.external_health_score) / 100 * weights['external_health']
            
        if self.incident_count:
            score += min(self.incident_count * 0.05, weights['incidents'])
            
        return min(score * 100, 100) 