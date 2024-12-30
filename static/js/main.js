document.addEventListener('DOMContentLoaded', function() {
    const studentIdInput = document.getElementById('studentId');
    const generateStudentBtn = document.getElementById('generateStudent');
    const fetchInfoBtn = document.getElementById('fetchInfo');
    const assessRiskBtn = document.getElementById('assessRisk');
    const clearDataBtn = document.getElementById('clearData');
    const riskLevelSpan = document.getElementById('riskLevel');
    const currentRiskFactors = document.getElementById('currentRiskFactors');
    const studentInfo = document.getElementById('studentInfo');
    const studentName = document.getElementById('studentName');
    const studentGrade = document.getElementById('studentGrade');

    // Shape indicators
    const indicators = {
        academic: document.getElementById('academicIndicator'),
        attendance: document.getElementById('attendanceIndicator'),
        behavioral: document.getElementById('behavioralIndicator'),
        socialEmotional: document.getElementById('socialEmotionalIndicator')
    };

    // Metric values
    const values = {
        academic: document.getElementById('academicValue'),
        attendance: document.getElementById('attendanceValue'),
        behavioral: document.getElementById('behavioralValue'),
        socialEmotional: document.getElementById('socialEmotionalValue')
    };

    // Gauge elements
    const gauges = {
        academic: document.getElementById('academicGauge'),
        attendance: document.getElementById('attendanceGauge'),
        behavioral: document.getElementById('behavioralGauge'),
        socialEmotional: document.getElementById('socialEmotionalGauge')
    };

    // Risk factor checkboxes
    const checkboxes = document.querySelectorAll('.form-check-input');
    let currentStudent = null;
    let riskChart = null;

    // Initialize chart
    function initializeChart() {
        const ctx = document.getElementById('riskChart').getContext('2d');
        riskChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        'var(--risk-green)',
                        'var(--risk-yellow)',
                        'var(--risk-red)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    generateStudentBtn.addEventListener('click', generateStudent);
    fetchInfoBtn.addEventListener('click', fetchStudentInfo);
    assessRiskBtn.addEventListener('click', assessRisk);
    clearDataBtn.addEventListener('click', clearData);

    // Initialize chart on load
    initializeChart();

    function generateStudent() {
        fetch('/api/generate-student')
            .then(response => {
                if (!response.ok) throw new Error('Failed to generate student');
                return response.json();
            })
            .then(data => {
                currentStudent = data;
                studentIdInput.value = data.id;
                studentName.textContent = data.name;
                studentGrade.textContent = `Grade ${data.grade_level}`;
                studentInfo.classList.remove('hidden');
                updateUI(data);
                updateChart(data.metrics);
                alert(`Generated student: ${data.name} (ID: ${data.id})`);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to generate student');
            });
    }

    function fetchStudentInfo() {
        const studentId = studentIdInput.value.trim();
        if (!studentId) {
            alert('Please enter a student ID');
            return;
        }

        fetch(`/api/student/${studentId}`)
            .then(response => {
                if (!response.ok) throw new Error('Student not found');
                return response.json();
            })
            .then(data => {
                currentStudent = data;
                studentName.textContent = data.name;
                studentGrade.textContent = `Grade ${data.grade_level}`;
                studentInfo.classList.remove('hidden');
                updateUI(data);
                if (data.latest_assessment) {
                    updateChart(data.latest_assessment);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to fetch student information');
            });
    }

    function assessRisk() {
        if (!currentStudent) {
            alert('Please fetch student information first');
            return;
        }

        const selectedFactors = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        const data = {
            studentId: currentStudent.id,
            patterns: selectedFactors
        };

        fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (!response.ok) throw new Error('Assessment failed');
                return response.json();
            })
            .then(data => {
                updateRiskIndicators(data.patterns);
                updateMetrics(data.metrics);
                updateGauges(data.metrics);
                updateRiskLevel(data.patterns);
                updateRiskFactors(selectedFactors);
                updateChart(data.metrics);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to assess risk');
            });
    }

    function updateUI(student) {
        if (student.latest_assessment) {
            updateRiskIndicators(student.latest_assessment.patterns);
            updateMetrics({
                academic_performance: student.latest_assessment.academic_performance,
                attendance_rate: student.latest_assessment.attendance_rate,
                behavioral_incidents: student.latest_assessment.behavioral_incidents,
                social_emotional_score: student.latest_assessment.social_emotional_score
            });
            updateGauges({
                academic_performance: student.latest_assessment.academic_performance,
                attendance_rate: student.latest_assessment.attendance_rate,
                behavioral_incidents: student.latest_assessment.behavioral_incidents,
                social_emotional_score: student.latest_assessment.social_emotional_score
            });
            updateRiskLevel(student.latest_assessment.patterns);
        }
    }

    function updateRiskIndicators(patterns) {
        Object.entries(patterns).forEach(([shape, color]) => {
            const indicator = getIndicatorForShape(shape);
            if (indicator) {
                indicator.classList.remove('risk-red', 'risk-yellow', 'risk-green', 'risk-blue');
                indicator.classList.add(`risk-${color}`);
            }
        });
    }

    function updateMetrics(metrics) {
        values.academic.textContent = `${(metrics.academic_performance * 100).toFixed(1)}%`;
        values.attendance.textContent = `${(metrics.attendance_rate * 100).toFixed(1)}%`;
        values.behavioral.textContent = metrics.behavioral_incidents;
        values.socialEmotional.textContent = `${(metrics.social_emotional_score * 100).toFixed(1)}%`;
    }

    function updateGauges(metrics) {
        gauges.academic.style.width = `${metrics.academic_performance * 100}%`;
        gauges.attendance.style.width = `${metrics.attendance_rate * 100}%`;
        gauges.behavioral.style.width = `${((10 - metrics.behavioral_incidents) / 10) * 100}%`;
        gauges.socialEmotional.style.width = `${metrics.social_emotional_score * 100}%`;

        // Update gauge colors
        Object.entries(gauges).forEach(([key, gauge]) => {
            let value = key === 'behavioral' 
                ? (10 - metrics.behavioral_incidents) / 10 
                : metrics[key === 'academic' ? 'academic_performance' : key === 'attendance' ? 'attendance_rate' : 'social_emotional_score'];
            
            gauge.style.backgroundColor = value >= 0.8 ? 'var(--risk-green)' 
                : value >= 0.6 ? 'var(--risk-yellow)' 
                : 'var(--risk-red)';
        });
    }

    function updateChart(metrics) {
        const riskScores = [0, 0, 0]; // [low, medium, high]
        const values = [
            metrics.academic_performance,
            metrics.attendance_rate,
            (10 - metrics.behavioral_incidents) / 10,
            metrics.social_emotional_score
        ];

        values.forEach(value => {
            if (value >= 0.8) riskScores[0]++;
            else if (value >= 0.6) riskScores[1]++;
            else riskScores[2]++;
        });

        riskChart.data.datasets[0].data = riskScores;
        riskChart.update();
    }

    function updateRiskLevel(patterns) {
        const riskColors = Object.values(patterns);
        const riskScore = calculateRiskScore(riskColors);
        let riskLevel = 'Low';
        
        if (riskScore >= 0.7) riskLevel = 'High';
        else if (riskScore >= 0.4) riskLevel = 'Medium';
        
        riskLevelSpan.textContent = riskLevel;
        riskLevelSpan.className = `risk-${riskLevel.toLowerCase()}`;
    }

    function updateRiskFactors(factors) {
        currentRiskFactors.innerHTML = '';
        
        const categories = {
            academic: [],
            attendance: [],
            behavioral: []
        };

        factors.forEach(factor => {
            if (factor.includes('grade') || factor.includes('completion') || factor.includes('engagement')) {
                categories.academic.push(formatFactorName(factor));
            } else if (factor.includes('attendance') || factor.includes('tardiness') || factor.includes('skipping')) {
                categories.attendance.push(formatFactorName(factor));
            } else {
                categories.behavioral.push(formatFactorName(factor));
            }
        });

        Object.entries(categories).forEach(([category, items]) => {
            if (items.length > 0) {
                const div = document.createElement('div');
                div.className = `risk-factor-item ${category}`;
                div.innerHTML = `
                    <strong class="d-block mb-1">${category.charAt(0).toUpperCase() + category.slice(1)}</strong>
                    <ul class="mb-0">
                        ${items.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                `;
                currentRiskFactors.appendChild(div);
            }
        });
    }

    function clearData() {
        currentStudent = null;
        studentIdInput.value = '';
        checkboxes.forEach(cb => cb.checked = false);
        riskLevelSpan.textContent = 'N/A';
        riskLevelSpan.className = '';
        currentRiskFactors.innerHTML = '';
        studentInfo.classList.add('hidden');
        studentName.textContent = '-';
        studentGrade.textContent = '-';
        
        // Reset indicators
        Object.values(indicators).forEach(indicator => {
            indicator.classList.remove('risk-red', 'risk-yellow', 'risk-green', 'risk-blue');
        });
        
        // Reset values
        Object.values(values).forEach(value => {
            value.textContent = '-';
        });

        // Reset gauges
        Object.values(gauges).forEach(gauge => {
            gauge.style.width = '0%';
            gauge.style.backgroundColor = '#e9ecef';
        });

        // Reset chart
        riskChart.data.datasets[0].data = [0, 0, 0];
        riskChart.update();
    }

    function getIndicatorForShape(shape) {
        switch (shape) {
            case 'circle': return indicators.academic;
            case 'triangle': return indicators.attendance;
            case 'square': return indicators.behavioral;
            default: return null;
        }
    }

    function calculateRiskScore(colors) {
        const weights = {
            red: 1,
            yellow: 0.6,
            green: 0.3,
            blue: 0
        };
        
        const total = colors.length;
        const score = colors.reduce((sum, color) => sum + weights[color], 0);
        return score / total;
    }

    function formatFactorName(factor) {
        return factor
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
}); 