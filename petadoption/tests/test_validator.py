import pytest
from petadoption import validator

def test_validate_lower_single_color():
    colors = ['black']
    v = validator.Validator()
    valid_colors = v.eval_colors(colors)
    assert valid_colors == colors
    
def test_validate_upper_single_color():
    colors = ['Black']
    v = validator.Validator()
    valid_colors = v.eval_colors(colors)
    assert valid_colors == ['black']
    
def test_negative_validate_lower_single_color():
    colors = ['orange']
    v = validator.Validator()
    valid_colors = v.eval_colors(colors)
    assert valid_colors == []
    
def test_validate_three_colors():
    colors = ['black', 'white', 'gray']
    v = validator.Validator()
    valid_colors = v.eval_colors(colors)
    assert valid_colors == colors
    
def test_validate_four_colors():
    colors = ['black', 'white', 'golden', 'gray']
    v = validator.Validator()
    valid_colors = v.eval_colors(colors)
    assert valid_colors == colors[:3]