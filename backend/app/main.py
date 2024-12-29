from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/assess', methods=['POST'])
def assess_risk():
    data = request.json
    student_id = data.get('studentId')
    risk_factor = data.get('riskFactor')
    
    # Example logic to calculate risk score
    risk_score = "Medium"  # Replace with actual logic
    risk_factors = [10, 20, 30, 40]  # Replace with actual data

    return jsonify({'riskScore': risk_score, 'riskFactors': risk_factors})

if __name__ == '__main__':
    app.run(debug=True) 