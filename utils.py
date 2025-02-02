def validate_student_id(student_id):
    """Validate if the student ID starts with 'TP' and is 8 characters long."""
    return student_id.startswith("TP") and len(student_id) == 8 and student_id[2:].isdigit()
