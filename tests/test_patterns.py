import pytest
from app import generate_pattern_colors, generate_color_for_pattern, PATTERNS

def test_pattern_color_generation():
    """Test pattern color generation for consistency"""
    student_id = "12345"
    patterns = ['connection', 'engagement', 'learning']
    
    # Test color generation
    colors = generate_pattern_colors(student_id, patterns)
    assert isinstance(colors, dict)
    assert 'circle' in colors
    assert 'triangle' in colors
    assert 'square' in colors
    
    # Test color validity
    valid_colors = ['red', 'yellow', 'green', 'blue']
    for shape, color in colors.items():
        assert color in valid_colors

def test_pattern_color_consistency():
    """Test that pattern colors are consistent for same input"""
    student_id = "12345"
    patterns = ['connection', 'engagement', 'learning']
    
    # Generate colors twice with same input
    colors1 = generate_pattern_colors(student_id, patterns)
    colors2 = generate_pattern_colors(student_id, patterns)
    
    # Colors should be identical for same input
    assert colors1 == colors2

def test_pattern_color_variation():
    """Test that pattern colors vary with different inputs"""
    patterns = ['connection', 'engagement', 'learning']
    
    # Generate colors for different student IDs
    colors1 = generate_pattern_colors("12345", patterns)
    colors2 = generate_pattern_colors("67890", patterns)
    
    # Colors should be different for different students
    assert colors1 != colors2

def test_pattern_descriptions():
    """Test pattern descriptions are valid"""
    for shape, colors in PATTERNS.items():
        for color, description in colors.items():
            assert isinstance(description, str)
            assert len(description) > 0

def test_color_generation_for_pattern():
    """Test individual pattern color generation"""
    pattern_count = 3
    category = 'connection'
    
    # Test multiple color generations
    colors = set()
    for _ in range(100):
        color = generate_color_for_pattern(['connection', 'engagement', 'learning'], category)
        assert color in ['red', 'yellow', 'green', 'blue']
        colors.add(color)
    
    # Should generate different colors over multiple runs
    assert len(colors) > 1

def test_pattern_color_weights():
    """Test pattern color weight distribution"""
    patterns = ['connection']
    category = 'connection'
    
    # Generate many colors to test distribution
    color_counts = {'red': 0, 'yellow': 0, 'green': 0, 'blue': 0}
    iterations = 1000
    
    for _ in range(iterations):
        color = generate_color_for_pattern(patterns, category)
        color_counts[color] += 1
    
    # Check that all colors are represented
    for count in color_counts.values():
        assert count > 0
        
    # Check that no color dominates completely (should be somewhat distributed)
    for count in color_counts.values():
        assert count < iterations * 0.5  # No color should appear more than 50% of the time 