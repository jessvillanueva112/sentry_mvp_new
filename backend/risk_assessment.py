import numpy as np
from sklearn.linear_model import LogisticRegression

# Example function to calculate risk score
class RiskAssessment:
    def __init__(self):
        self.risk_factors = {
            'behavioral': 0,
            'attendance': 1,
            'academic': 2,
            'social': 3
        }
        
        # Initialize the model with more realistic training data
        self.model = LogisticRegression()
        
        # Example training data based on risk factors
        X_train = np.array([
            [1, 0, 0, 0],  # Only behavioral
            [0, 1, 0, 0],  # Only attendance
            [0, 0, 1, 0],  # Only academic
            [0, 0, 0, 1],  # Only social
            [1, 1, 0, 0],  # behavioral + attendance
            [1, 1, 1, 0],  # behavioral + attendance + academic
            [1, 1, 1, 1],  # All factors
        ])
        
        # Corresponding risk levels (0: low, 1: high)
        y_train = np.array([0, 0, 0, 0, 1, 1, 1])
        
        # Train the model
        self.model.fit(X_train, y_train)

    def calculate_risk_score(self, risk_factors):
        # Convert string risk factors to numeric array
        input_vector = np.zeros(len(self.risk_factors))
        
        for factor in risk_factors:
            factor_key = factor.lower().split()[0]  # Get first word of factor
            if factor_key in self.risk_factors:
                input_vector[self.risk_factors[factor_key]] = 1
        
        # Get probability of high risk
        risk_prob = self.model.predict_proba(input_vector.reshape(1, -1))[0][1]
        
        # Convert probability to risk level
        if risk_prob < 0.3:
            return "Low"
        elif risk_prob < 0.7:
            return "Medium"
        else:
            return "High"

# Example usage
if __name__ == "__main__":
    ra = RiskAssessment()
    example_data = [1, 0]  # Example input data
    score = ra.calculate_risk_score(example_data)
    print(f"Calculated Risk Score: {score}") 