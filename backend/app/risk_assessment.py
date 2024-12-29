import numpy as np
from sklearn.linear_model import LogisticRegression

# Example function to calculate risk score
class RiskAssessment:
    def __init__(self):
        # Initialize the model
        self.model = LogisticRegression()
        # Example training data
        self.X_train = np.array([[0, 1], [1, 0], [1, 1], [0, 0]])
        self.y_train = np.array([0, 1, 1, 0])
        self.model.fit(self.X_train, self.y_train)

    def calculate_risk_score(self, data):
        # Convert input data to numpy array
        input_data = np.array(data).reshape(1, -1)
        # Predict risk score
        risk_score = self.model.predict_proba(input_data)[0][1]
        return risk_score

# Example usage
if __name__ == "__main__":
    ra = RiskAssessment()
    example_data = [1, 0]  # Example input data
    score = ra.calculate_risk_score(example_data)
    print(f"Calculated Risk Score: {score}") 