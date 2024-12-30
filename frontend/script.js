// Initialize Chart.js
let riskChart;

// Function to initialize the risk distribution chart
function initializeChart() {
    const ctx = document.getElementById('risk-chart').getContext('2d');
    riskChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: ['#4caf50', '#ffc107', '#dc3545'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                            return `${label}: ${percentage}% (${value} students)`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

// Function to fetch student information
function fetchStudentInfo(studentId) {
    fetch(`/api/student/${studentId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('student-name').textContent = data.name || '-';
            document.getElementById('student-grade').textContent = data.grade || '-';
            document.getElementById('last-assessment-date').textContent = 
                data.latest_assessment ? new Date(data.latest_assessment.timestamp).toLocaleDateString() : 'No previous assessment';
            
            document.getElementById('student-info').classList.remove('hidden');
            
            if (data.latest_assessment) {
                updateMetrics(data.latest_assessment);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching student information');
        });
}

// Function to update metrics display
function updateMetrics(assessment) {
    // Update metric values
    document.getElementById('academic-score').textContent = `${Math.round(assessment.academic_performance * 100)}%`;
    document.getElementById('attendance-score').textContent = `${Math.round(assessment.attendance_rate * 100)}%`;
    document.getElementById('behavioral-score').textContent = `${10 - assessment.behavioral_incidents}/10`;
    document.getElementById('social-score').textContent = `${Math.round(assessment.social_emotional_score * 100)}%`;
    
    // Update gauge fills
    document.getElementById('academic-gauge').style.width = `${assessment.academic_performance * 100}%`;
    document.getElementById('attendance-gauge').style.width = `${assessment.attendance_rate * 100}%`;
    document.getElementById('behavioral-gauge').style.width = `${((10 - assessment.behavioral_incidents) / 10) * 100}%`;
    document.getElementById('social-gauge').style.width = `${assessment.social_emotional_score * 100}%`;
    
    // Update gauge colors based on values
    updateGaugeColors(assessment);
}

// Function to update gauge colors
function updateGaugeColors(assessment) {
    const gauges = {
        'academic-gauge': assessment.academic_performance,
        'attendance-gauge': assessment.attendance_rate,
        'behavioral-gauge': (10 - assessment.behavioral_incidents) / 10,
        'social-gauge': assessment.social_emotional_score
    };
    
    Object.entries(gauges).forEach(([id, value]) => {
        const gauge = document.getElementById(id);
        if (value >= 0.8) {
            gauge.style.backgroundColor = '#4caf50';
        } else if (value >= 0.6) {
            gauge.style.backgroundColor = '#ffc107';
        } else {
            gauge.style.backgroundColor = '#dc3545';
        }
    });
}

// Function to update statistics from localStorage
function updateStatistics() {
    const localData = getFromLocalStorage();
    const distribution = {
        low: 0,
        medium: 0,
        high: 0
    };
    
    localData.forEach(item => {
        if (item.riskScore === "Low") distribution.low++;
        else if (item.riskScore === "Medium") distribution.medium++;
        else if (item.riskScore === "High") distribution.high++;
    });

    // Update chart with new data
    riskChart.data.datasets[0].data = [
        distribution.low,
        distribution.medium,
        distribution.high
    ];
    riskChart.update();

    // Update risk factors display
    if (localData.length > 0) {
        updateRiskFactorsDisplay(localData[localData.length - 1].riskIndicators);
    }
}

// Function to update risk factors display
function updateRiskFactorsDisplay(factors) {
    const riskFactorsDiv = document.querySelector('.risk-factors');
    if (!riskFactorsDiv) return;
    
    const riskFactorLabels = {
        'grades_declining': 'Declining Grades',
        'assignment_completion': 'Low Assignment Completion',
        'academic_engagement': 'Low Academic Engagement',
        'attendance_poor': 'Poor Attendance',
        'tardiness': 'Frequent Tardiness',
        'class_skipping': 'Class Skipping',
        'disruptive_behavior': 'Disruptive Behavior',
        'disciplinary_incidents': 'Disciplinary Incidents',
        'peer_conflicts': 'Peer Conflicts',
        'social_isolation': 'Social Isolation',
        'emotional_distress': 'Emotional Distress',
        'motivation_loss': 'Loss of Motivation'
    };
    
    riskFactorsDiv.innerHTML = factors.map(factor => 
        `<div class="risk-factor-chip">${riskFactorLabels[factor] || factor}</div>`
    ).join('');
}

// Initialize localStorage structure
const LOCAL_STORAGE_KEY = 'studentRiskData';

// Function to save data to localStorage
function saveToLocalStorage(data) {
    const existingData = getFromLocalStorage();
    existingData.push(data);
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(existingData));
}

// Function to get data from localStorage
function getFromLocalStorage() {
    return JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || '[]');
}

// Function to clear localStorage
function clearLocalStorage() {
    localStorage.removeItem(LOCAL_STORAGE_KEY);
    updateStatistics();
    document.getElementById('student-info').classList.add('hidden');
    resetMetrics();
}

// Function to reset metrics display
function resetMetrics() {
    const metricIds = ['academic-score', 'attendance-score', 'behavioral-score', 'social-score'];
    metricIds.forEach(id => document.getElementById(id).textContent = '-');
    
    const gaugeIds = ['academic-gauge', 'attendance-gauge', 'behavioral-gauge', 'social-gauge'];
    gaugeIds.forEach(id => {
        const gauge = document.getElementById(id);
        gauge.style.width = '0%';
        gauge.style.backgroundColor = '#e9ecef';
    });
}

// Initialize the chart when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    updateStatistics();
    
    // Add fetch student info button handler
    document.getElementById('fetch-student').addEventListener('click', function() {
        const studentId = document.getElementById('student-id').value;
        if (studentId) {
            fetchStudentInfo(studentId);
        } else {
            alert('Please enter a student ID');
        }
    });
});

// Handle risk assessment form submission
document.getElementById('start-assessment').addEventListener('click', function() {
    const studentId = document.getElementById('student-id').value;
    const riskFactors = Array.from(document.getElementById('risk-factors').selectedOptions)
        .map(option => option.value);

    if (!studentId || riskFactors.length === 0) {
        alert('Please fill in all required fields');
        return;
    }

    fetch('/api/assess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            studentId,
            riskFactors
        }),
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('risk-score').textContent = result.riskScore;
        const data = {
            studentId,
            riskIndicators: riskFactors,
            riskScore: result.riskScore,
            timestamp: new Date().toISOString()
        };
        saveToLocalStorage(data);
        updateStatistics();
        
        // Update metrics with the new assessment data
        updateMetrics(result.metrics);
    })
    .catch(error => console.error('Error:', error));
});

// Add clear data button functionality
document.getElementById('clear-data').addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
        clearLocalStorage();
        document.getElementById('risk-score').textContent = 'N/A';
    }
}); 