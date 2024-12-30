import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.mark.frontend
def test_dashboard_loads(selenium_driver):
    """Test that the dashboard loads correctly"""
    try:
        selenium_driver.get('http://localhost:5000')
        WebDriverWait(selenium_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        assert "Student Risk Assessment Dashboard" in selenium_driver.title
        
        # Check for main components with better error handling
        components = ['risk-chart', 'student-info', 'pattern-selection']
        for component_id in components:
            try:
                element = WebDriverWait(selenium_driver, 10).until(
                    EC.presence_of_element_located((By.ID, component_id))
                )
                assert element.is_displayed(), f"Component {component_id} is not displayed"
            except TimeoutException:
                pytest.fail(f"Component {component_id} not found within timeout")
    except Exception as e:
        pytest.fail(f"Dashboard failed to load properly: {str(e)}")

@pytest.mark.frontend
def test_generate_student_button(selenium_driver):
    """Test the generate student button functionality"""
    try:
        selenium_driver.get('http://localhost:5000')
        
        # Wait for and click generate button
        generate_btn = WebDriverWait(selenium_driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'generate-student'))
        )
        generate_btn.click()
        
        # Wait for student info with better error handling
        try:
            student_info = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'student-details'))
            )
            assert student_info.text != "", "Student details are empty"
            assert "ID:" in student_info.text, "Student ID not found"
            assert "Grade:" in student_info.text, "Student grade not found"
        except TimeoutException:
            pytest.fail("Student information did not load within timeout")
    except Exception as e:
        pytest.fail(f"Generate student functionality failed: {str(e)}")

@pytest.mark.frontend
def test_pattern_selection(selenium_driver):
    """Test pattern selection functionality"""
    try:
        selenium_driver.get('http://localhost:5000')
        
        # Generate student first
        generate_btn = WebDriverWait(selenium_driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'generate-student'))
        )
        generate_btn.click()
        
        # Wait for and test pattern selection
        try:
            WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pattern-item'))
            )
            patterns = selenium_driver.find_elements(By.CLASS_NAME, 'pattern-item')
            assert len(patterns) > 0, "No pattern items found"
            
            for pattern in patterns[:2]:
                pattern.click()
                assert 'selected' in pattern.get_attribute('class'), "Pattern not selected after click"
        except TimeoutException:
            pytest.fail("Pattern selection elements did not load within timeout")
    except Exception as e:
        pytest.fail(f"Pattern selection test failed: {str(e)}")

@pytest.mark.frontend
def test_chart_interaction(selenium_driver):
    """Test chart interaction and tooltips"""
    try:
        selenium_driver.get('http://localhost:5000')
        
        # Generate student and wait for chart
        generate_btn = WebDriverWait(selenium_driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'generate-student'))
        )
        generate_btn.click()
        
        try:
            chart_point = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'chart-point'))
            )
            
            # Test hover interaction
            selenium_driver.execute_script(
                "arguments[0].dispatchEvent(new MouseEvent('mouseover', {'bubbles': true}))",
                chart_point
            )
            
            # Verify tooltip
            tooltip = WebDriverWait(selenium_driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tooltip'))
            )
            assert tooltip.is_displayed(), "Tooltip not displayed on hover"
            assert "Risk Score:" in tooltip.text, "Tooltip missing risk score information"
        except TimeoutException:
            pytest.fail("Chart elements did not load within timeout")
    except Exception as e:
        pytest.fail(f"Chart interaction test failed: {str(e)}")

@pytest.mark.frontend
def test_form_submission(selenium_driver):
    """Test assessment form submission"""
    try:
        selenium_driver.get('http://localhost:5000')
        
        # Setup: Generate student
        generate_btn = WebDriverWait(selenium_driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'generate-student'))
        )
        generate_btn.click()
        
        # Wait for and fill form
        try:
            form = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.ID, 'assessment-form'))
            )
            
            notes_input = form.find_element(By.ID, 'assessment-notes')
            notes_input.clear()
            notes_input.send_keys("Test assessment notes")
            
            submit_btn = form.find_element(By.ID, 'submit-assessment')
            submit_btn.click()
            
            # Verify submission result
            success_message = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'success-message'))
            )
            assert success_message.is_displayed(), "Success message not displayed"
        except TimeoutException:
            pytest.fail("Form submission elements did not load within timeout")
    except Exception as e:
        pytest.fail(f"Form submission test failed: {str(e)}")

@pytest.mark.frontend
def test_error_handling(selenium_driver):
    """Test frontend error handling"""
    try:
        selenium_driver.get('http://localhost:5000')
        
        # Try to submit form without student
        try:
            submit_btn = WebDriverWait(selenium_driver, 10).until(
                EC.presence_of_element_located((By.ID, 'submit-assessment'))
            )
            submit_btn.click()
            
            # Verify error message
            error_message = WebDriverWait(selenium_driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'error-message'))
            )
            assert error_message.is_displayed(), "Error message not displayed"
            assert "Please generate a student first" in error_message.text, "Incorrect error message"
        except TimeoutException:
            pytest.fail("Error handling elements did not load within timeout")
    except Exception as e:
        pytest.fail(f"Error handling test failed: {str(e)}") 