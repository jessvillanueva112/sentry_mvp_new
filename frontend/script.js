document.getElementById('start-assessment').addEventListener('click', function() {
    const studentId = document.getElementById('student-id').value;
    const riskFactor = document.getElementById('risk-factors').value;

    fetch('/api/assess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ studentId, riskFactor }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('risk-score').textContent = data.riskScore;
        // Update chart with data.riskFactors
    })
    .catch(error => console.error('Error:', error));
}); 