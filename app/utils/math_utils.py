import random
import math
import numpy as np
from sympy import symbols, solve, simplify, expand, factor
from sympy.parsing.sympy_parser import parse_expr

def generate_addition_problem(grade, difficulty='beginner'):
    """Generate addition problems based on grade level"""
    if grade <= 2:
        if difficulty == 'beginner':
            a = random.randint(1, 20)
            b = random.randint(1, 20)
        else:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
    elif grade <= 4:
        if difficulty == 'beginner':
            a = random.randint(10, 100)
            b = random.randint(10, 100)
        else:
            a = random.randint(100, 999)
            b = random.randint(100, 999)
    else:
        if difficulty == 'beginner':
            a = random.randint(100, 9999)
            b = random.randint(100, 9999)
        else:
            a = random.randint(1000, 99999)
            b = random.randint(1000, 99999)
    
    return {
        'question': f"{a} + {b} = ?",
        'answer': a + b,
        'explanation': f"Add {a} and {b} to get {a + b}"
    }

def generate_multiplication_problem(grade, difficulty='beginner'):
    """Generate multiplication problems based on grade level"""
    if grade <= 3:
        if difficulty == 'beginner':
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(5, 12)
            b = random.randint(5, 12)
    elif grade <= 5:
        if difficulty == 'beginner':
            a = random.randint(10, 25)
            b = random.randint(2, 12)
        else:
            a = random.randint(25, 50)
            b = random.randint(10, 25)
    else:
        if difficulty == 'beginner':
            a = random.randint(50, 100)
            b = random.randint(10, 50)
        else:
            a = random.randint(100, 999)
            b = random.randint(50, 100)
    
    return {
        'question': f"{a} × {b} = ?",
        'answer': a * b,
        'explanation': f"Multiply {a} by {b} to get {a * b}"
    }

def generate_fraction_problem(grade, difficulty='beginner'):
    """Generate fraction problems based on grade level"""
    if grade <= 4:
        # Simple fraction addition with same denominator
        denom = random.randint(2, 10)
        num1 = random.randint(1, denom - 1)
        num2 = random.randint(1, denom - 1)
        
        return {
            'question': f"\\frac{{{num1}}}{{{denom}}} + \\frac{{{num2}}}{{{denom}}} = ?",
            'answer': f"\\frac{{{num1 + num2}}}{{{denom}}}",
            'explanation': f"Add the numerators: {num1} + {num2} = {num1 + num2}, keep denominator {denom}"
        }
    else:
        # Fraction multiplication
        denom1 = random.randint(2, 10)
        num1 = random.randint(1, denom1 - 1)
        denom2 = random.randint(2, 10)
        num2 = random.randint(1, denom2 - 1)
        
        result_num = num1 * num2
        result_denom = denom1 * denom2
        
        return {
            'question': f"\\frac{{{num1}}}{{{denom1}}} × \\frac{{{num2}}}{{{denom2}}} = ?",
            'answer': f"\\frac{{{result_num}}}{{{result_denom}}}",
            'explanation': f"Multiply numerators: {num1} × {num2} = {result_num}, multiply denominators: {denom1} × {denom2} = {result_denom}"
        }

def generate_algebra_problem(grade, difficulty='beginner'):
    """Generate algebra problems based on grade level"""
    if grade <= 7:
        # Simple linear equations
        a = random.randint(1, 10)
        b = random.randint(1, 20)
        x = random.randint(1, 10)
        c = a * x + b
        
        return {
            'question': f"{a}x + {b} = {c}",
            'answer': x,
            'explanation': f"Subtract {b} from both sides: {a}x = {c - b}, then divide by {a}: x = {x}"
        }
    else:
        # Quadratic equations
        x = random.randint(1, 10)
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = -(a * x**2 + b * x)
        
        return {
            'question': f"{a}x² + {b}x + {c} = 0",
            'answer': x,
            'explanation': f"Use quadratic formula or factoring to find x = {x}"
        }

def generate_geometry_problem(grade, difficulty='beginner'):
    """Generate geometry problems based on grade level"""
    if grade <= 5:
        # Area of rectangle
        length = random.randint(5, 20)
        width = random.randint(3, 15)
        
        return {
            'question': f"Find the area of a rectangle with length {length} and width {width}",
            'answer': length * width,
            'explanation': f"Area = length × width = {length} × {width} = {length * width}"
        }
    elif grade <= 8:
        # Area of triangle
        base = random.randint(5, 20)
        height = random.randint(5, 15)
        
        return {
            'question': f"Find the area of a triangle with base {base} and height {height}",
            'answer': (base * height) / 2,
            'explanation': f"Area = (base × height) ÷ 2 = ({base} × {height}) ÷ 2 = {(base * height) / 2}"
        }
    else:
        # Circle area
        radius = random.randint(3, 10)
        
        return {
            'question': f"Find the area of a circle with radius {radius}",
            'answer': round(math.pi * radius**2, 2),
            'explanation': f"Area = π × radius² = π × {radius}² = {round(math.pi * radius**2, 2)}"
        }

def generate_statistics_problem(grade, difficulty='beginner'):
    """Generate statistics problems based on grade level"""
    if grade <= 6:
        # Mean calculation
        numbers = [random.randint(1, 20) for _ in range(5)]
        mean = sum(numbers) / len(numbers)
        
        return {
            'question': f"Find the mean of: {', '.join(map(str, numbers))}",
            'answer': round(mean, 2),
            'explanation': f"Mean = sum of numbers ÷ count = {sum(numbers)} ÷ {len(numbers)} = {round(mean, 2)}"
        }
    else:
        # Mode calculation
        numbers = [random.randint(1, 10) for _ in range(8)]
        from collections import Counter
        counter = Counter(numbers)
        mode = counter.most_common(1)[0][0]
        
        return {
            'question': f"Find the mode of: {', '.join(map(str, numbers))}",
            'answer': mode,
            'explanation': f"The mode is the number that appears most frequently: {mode}"
        }

def create_interactive_simulation(grade, topic, difficulty='beginner'):
    """Create interactive simulation data for mathematical concepts"""
    simulations = {
        'addition': {
            'type': 'number_line',
            'data': generate_addition_problem(grade, difficulty),
            'visualization': 'number_line'
        },
        'multiplication': {
            'type': 'array_model',
            'data': generate_multiplication_problem(grade, difficulty),
            'visualization': 'grid'
        },
        'fractions': {
            'type': 'fraction_circles',
            'data': generate_fraction_problem(grade, difficulty),
            'visualization': 'circles'
        },
        'algebra': {
            'type': 'equation_solver',
            'data': generate_algebra_problem(grade, difficulty),
            'visualization': 'balance_scale'
        },
        'geometry': {
            'type': 'shape_calculator',
            'data': generate_geometry_problem(grade, difficulty),
            'visualization': 'shapes'
        },
        'statistics': {
            'type': 'data_analyzer',
            'data': generate_statistics_problem(grade, difficulty),
            'visualization': 'charts'
        }
    }
    
    return simulations.get(topic.lower(), {
        'type': 'generic',
        'data': {'question': 'Sample question', 'answer': 'Sample answer'},
        'visualization': 'text'
    })

def validate_answer(student_answer, correct_answer, tolerance=0.01):
    """Validate student answer with tolerance for numerical answers"""
    try:
        # Try to convert to float for numerical comparison
        student_float = float(student_answer)
        correct_float = float(correct_answer)
        return abs(student_float - correct_float) <= tolerance
    except (ValueError, TypeError):
        # For non-numerical answers, do exact string comparison
        return str(student_answer).strip().lower() == str(correct_answer).strip().lower()