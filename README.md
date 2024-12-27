# Student Risk Data Collection Dashboard V0.1

## One-Liner
A simple, focused dashboard to collect and visualize basic student risk data for early intervention.

## Success Criteria

### Minimum Viable Product (MVP)
- Create a single-page form to collect basic student risk indicators
- Store data locally
- Display basic visualization of collected data
- Ensure data privacy and basic input validation

### Stretch Goals
- Add data filtering capabilities
- Implement basic data export functionality
- Create simple risk score calculation

## Key Tasks

### 1. HTML Form Design
- Create input fields for:
  - Student ID/Name
  - Age
  - Basic risk indicators (dropdown/checkboxes)
  - Optional notes section

### 2. Data Storage
- Use localStorage for initial data persistence
- Create simple data structure to store student risk information

### 3. Basic Visualization
- Create a simple chart showing:
  - Number of students
  - Risk level distribution
  - Basic statistical overview

## Technical Requirements
- HTML5
- CSS3
- Vanilla JavaScript
- Chart.js for visualization
- Flask for backend API
- Flask-Cors for handling CORS

## Data Collection Fields
```javascript
const studentRiskData = {
  studentId: String,
  age: Number,
  riskIndicators: [
    'behavioral_issues',
    'attendance_problems',
    'academic_struggles',
    'social_isolation'
  ],
  riskScore: Number,
  additionalNotes: String
};
```

## Privacy Considerations
- No personally identifiable information stored
- Data stored client-side only
- Clear data reset/delete functionality

## Learning Objectives
1. Form design and validation
2. Basic data storage techniques
3. Simple data visualization
4. JavaScript event handling

## Setting Up the Flask Application

### Project Structure

```
project-root/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── models.py
│   ├── __init__.py
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

### Installation and Setup

1. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies:**

   Create a `requirements.txt` file with the following content:

   ```
   Flask
   Flask-Cors
   python-dotenv
   ```

   Then, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**

   Create a `.env` file in the root directory with the following content:

   ```
   FLASK_APP=backend/main.py
   FLASK_ENV=development
   ```

4. **Running the Application:**

   Start the Flask application with:

   ```bash
   flask run --host=0.0.0.0
   ```

   Access the API at `http://<your-public-ip>:5000/api/students`.

## Git Setup

1. **Initialize Git:**

   ```bash
   git init
   ```

2. **Create a `.gitignore` File:**

   Add the following to `.gitignore`:

   ```
   venv/
   __pycache__/
   .env
   ```

3. **Commit Your Changes:**

   ```bash
   git add .
   git commit -m "Initial commit"
   ```

## Deployment

To deploy your Flask app, you can use a cloud service like AWS, Google Cloud, or DigitalOcean. Ensure your server is secure and only accessible through necessary ports. Consider using a production server like Gunicorn or uWSGI with a reverse proxy like Nginx for better performance and security.

Would you like me to elaborate on any specific section?