from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from models import db, Student, RiskAssessment
from risk_assessment import RiskAssessment as RiskCalculator

app = Flask(__name__)
CORS(app)

# Database configuration
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    STATIC_FOLDER='../frontend',
    STATIC_URL_PATH=''
)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/assess', methods=['POST'])
def assess_risk():
    data = request.json
    student_id = data.get('studentId')
    risk_factors = data.get('riskFactors', [])
    
    # Calculate risk score
    calculator = RiskCalculator()
    risk_score = calculator.calculate_risk_score(risk_factors)
    
    return jsonify({
        'studentId': student_id,
        'riskScore': risk_score,
        'riskFactors': risk_factors
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    total_students = Student.query.count()
    risk_distribution = {
        'low': Student.query.filter_by(risk_level='Low').count(),
        'medium': Student.query.filter_by(risk_level='Medium').count(),
        'high': Student.query.filter_by(risk_level='High').count()
    }
    
    return jsonify({
        'totalStudents': total_students,
        'riskDistribution': risk_distribution
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True) 