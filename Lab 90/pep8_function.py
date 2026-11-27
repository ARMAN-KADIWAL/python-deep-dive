def calculate_student_grade(assignments, exams, participation):
    """
    Calculate a student's final grade based on assignments, exams, and participation.
    
    Args:
        assignments (list): List of assignment scores (0-100)
        exams (list): List of exam scores (0-100)
        participation (float): Participation score (0-100)
    
    Returns:
        dict: Dictionary containing grade information
    """
    # Validate input parameters
    if not assignments or not exams:
        raise ValueError("Assignments and exams lists cannot be empty")
    
    if not (0 <= participation <= 100):
        raise ValueError("Participation score must be between 0 and 100")
    
    # Calculate averages
    assignment_average = sum(assignments) / len(assignments)
    exam_average = sum(exams) / len(exams)
    
    # Weight the components (assignments: 40%, exams: 50%, participation: 10%)
    final_score = (assignment_average * 0.4 + 
                   exam_average * 0.5 + 
                   participation * 0.1)
    
    # Determine letter grade
    if final_score >= 90:
        letter_grade = 'A'
    elif final_score >= 80:
        letter_grade = 'B'
    elif final_score >= 70:
        letter_grade = 'C'
    elif final_score >= 60:
        letter_grade = 'D'
    else:
        letter_grade = 'F'
    
    # Return comprehensive grade information
    grade_info = {
        'assignment_average': round(assignment_average, 2),
        'exam_average': round(exam_average, 2),
        'participation_score': participation,
        'final_score': round(final_score, 2),
        'letter_grade': letter_grade
    }
    
    return grade_info


def main():
    """Demonstrate the grade calculation function."""
    # Sample student data
    student_assignments = [85, 92, 78, 88, 95]
    student_exams = [82, 89, 91]
    student_participation = 95.0
    
    try:
        grade_result = calculate_student_grade(
            student_assignments, 
            student_exams, 
            student_participation
        )
        
        print("Student Grade Report:")
        print("-" * 25)
        print(f"Assignment Average: {grade_result['assignment_average']}%")
        print(f"Exam Average: {grade_result['exam_average']}%")
        print(f"Participation: {grade_result['participation_score']}%")
        print(f"Final Score: {grade_result['final_score']}%")
        print(f"Letter Grade: {grade_result['letter_grade']}")
        
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    main()
