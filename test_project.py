from unittest.mock import patch
from project import get_integer_input, get_float_input, calculate_grade

def test_get_integer_input_valid():
    with patch('builtins.input', return_value='5'):
        result = get_integer_input("Enter an integer: ")
        assert result == 5, f"Expected 5, but got {result}"

def test_get_float_input_exit():
    with patch('builtins.input', return_value='exit'):
        result = get_float_input("Enter a number or 'exit' to quit: ")
        assert result == 'exit', f"Expected 'exit', but got {result}"

def test_calculate_grade():
    assignments = 2
    quizzes = 2
    tests = 1
    exams = 1
    assignment_weight = 25
    quiz_weight = 25
    test_weight = 25
    exam_weight = 25
    assignment_grades = [80, 90]
    quiz_grades = [85, 90]
    test_grades = [88]
    exam_grades = [92]
    expected_grade = 88.125
    result = calculate_grade(assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, assignment_grades, quiz_grades, test_grades, exam_grades)
    assert result == expected_grade, f"Expected grade {expected_grade}, but got {result}"

