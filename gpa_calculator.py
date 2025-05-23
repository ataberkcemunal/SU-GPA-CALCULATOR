import re
import pdfplumber
import os
import sys

# Grading system from Sabancı University
GRADE_POINTS = {
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'F': 0.0
}

class SuppressStderr:
    def __enter__(self):
        self.stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr.close()
        sys.stderr = self.stderr

def extract_registered_courses(document):
    """Extract registered courses from the document's OCR content."""
    registered_courses = []
    current_semester = None
    lines = document.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect semester headers
        semester_match = re.search(r'(Fall|Spring|Summer)\s+\d{4}-\d{4}', line)
        if semester_match:
            current_semester = semester_match.group(0)
            continue
        # Try pipe-separated format first
        course_match = re.search(
            r'([A-Z]{2,4}\s+\d{3})\s*\|\s*([^|]+?)\s*\|\s*UG\s*\|\s*Registered\s*\|\s*(\d+\.\d{2})\s*\|\s*(\d+\.\d{2})',
            line
        )
        # If not found, try space-separated format
        if not course_match:
            course_match = re.search(
                r'([A-Z]{2,4}\s+\d{3})\s+([^\d]+)\s+UG\s+Registered\s+(\d+\.\d{2})\s+(\d+\.\d{2})',
                line
            )
        if course_match and current_semester:
            course_code = course_match.group(1).strip()
            course_title = course_match.group(2).strip()
            credits = float(course_match.group(3))
            ects = float(course_match.group(4))
            course_info = {
                'code': course_code,
                'title': course_title,
                'credits': credits,
                'ects': ects,
                'semester': current_semester
            }
            registered_courses.append(course_info)
    return registered_courses

def get_valid_grade(course_code, course_title):
    """Prompt user for a valid grade for a given course."""
    valid_grades = list(GRADE_POINTS.keys()) + ['S', 'U']
    while True:
        grade = input(f"{course_code}: ").strip().upper()
        if grade in valid_grades:
            return grade
        print("Not a valid grade.")
        print(f"Valid grades: {', '.join(valid_grades)}")

def calculate_term_gpa(courses, target_semester='Spring 2024-2025'):
    """Calculate Term GPA for the specified semester based on user-input grades."""
    total_grade_points = 0.0
    total_credits = 0.0
    total_ects = 0.0
    total_su_credits = 0.0  # For transcript purposes

    print(f"\nEnter estimated grades for registered courses in {target_semester}:")
    print("\nValid grades: A, A-, B+, B, B-, C+, C, C-, D+, D, F, S, U\n")
    for course in courses:
        # Only process courses from the target semester
        if course['semester'] != target_semester:
            continue
        # Skip courses with 0 SU credits as they do not affect GPA
        if course['credits'] == 0.00:
            continue
        grade = get_valid_grade(course['code'], course['title'])
        if grade in ['S', 'U']:
            # Satisfactory/Unsatisfactory: add credits to total_su_credits, but not to GPA
            total_su_credits += course['credits']
            total_ects += course['ects']
            continue
        grade_points = GRADE_POINTS[grade]
        total_grade_points += grade_points * course['credits']
        total_credits += course['credits']
        total_su_credits += course['credits']
        total_ects += course['ects']

    # Calculate GPA
    if total_credits == 0:
        return 0.0, total_su_credits, total_ects
    gpa = total_grade_points / total_credits
    return gpa, total_su_credits, total_ects

def extract_summary_values(document):
    """Extracts Total Earned SU Credits, Total Earned ECTS, and CGPA from the document, supporting both table and space-separated formats."""
    su_credits = None
    ects = None
    cgpa = None
    lines = document.split('\n')
    for i, line in enumerate(lines):
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        # Look for the summary header row
        if re.search(r'Total Earned SU Credits', clean_line, re.IGNORECASE) and \
           re.search(r'Total Earned ECTS', clean_line, re.IGNORECASE) and \
           re.search(r'CGPA', clean_line, re.IGNORECASE):
            # Try to extract values from the next non-empty line
            for j in range(i+1, len(lines)):
                value_line = lines[j].strip()
                if value_line:
                    # Try to extract three numbers separated by whitespace
                    values = re.findall(r'\d+\.\d+', value_line)
                    if len(values) >= 3:
                        try:
                            su_credits = float(values[0])
                            ects = float(values[1])
                            cgpa = float(values[2])
                        except ValueError:
                            pass
                    break
    return su_credits, ects, cgpa

def extract_latest_semester(document):
    """Extracts the most recent semester header from the document."""
    semesters = []
    for line in document.split('\n'):
        match = re.search(r'(Fall|Spring|Summer)\s+\d{4}-\d{4}', line)
        if match:
            semesters.append(match.group(0))
    return semesters[-1] if semesters else None

def get_semesters_with_registered_courses(courses):
    """Return a sorted list of semesters that have at least one Registered course with SU credits > 0."""
    semesters = set()
    for course in courses:
        if course['credits'] > 0:
            semesters.add(course['semester'])
    return sorted(semesters)

def main():
    # Find all PDF files in the current directory
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    if len(pdf_files) == 0:
        print("No PDF file found in the current directory.")
        return
    if len(pdf_files) > 1:
        print("Multiple PDF files found in the current directory. Please keep only one PDF file.")
        return
    pdf_path = pdf_files[0]
    try:
        with SuppressStderr():
            with pdfplumber.open(pdf_path) as pdf:
                document = ""
                for page in pdf.pages:
                    document += page.extract_text() + "\n"
    except Exception as e:
        print(f"PDF could not be read: {e}")
        return

    # Extract previous summary values
    su_credits, ects, cgpa = extract_summary_values(document)
    if cgpa is None or su_credits is None or ects is None:
        print("Could not extract previous CGPA, SU Credits, or ECTS from the document.")
        return

    prev_grade_points = cgpa * su_credits

    # Extract registered courses
    registered_courses = extract_registered_courses(document)
    if not registered_courses:
        print("No registered courses found in the document.")
        return

    # Filter all Registered courses with SU credits > 0
    courses_for_input = [c for c in registered_courses if c['credits'] > 0]
    if not courses_for_input:
        print("No Registered courses with SU credits > 0 found.")
        return

    print("Enter estimated grades:")

    # GPA calculation for all such courses
    total_grade_points = 0.0
    total_credits = 0.0
    total_ects = 0.0
    total_su_credits = 0.0
    for course in courses_for_input:
        grade = get_valid_grade(course['code'], course['title'])
        if grade in ['S', 'U']:
            total_su_credits += course['credits']
            total_ects += course['ects']
            continue
        grade_points = GRADE_POINTS[grade]
        total_grade_points += grade_points * course['credits']
        total_credits += course['credits']
        total_su_credits += course['credits']
        total_ects += course['ects']

    # Calculate new totals
    new_total_grade_points = prev_grade_points + total_grade_points
    new_total_credits = su_credits + total_credits
    new_total_ects = ects + total_ects

    # Calculate new CGPA
    if new_total_credits == 0:
        new_cgpa = cgpa
    else:
        new_cgpa = new_total_grade_points / new_total_credits

    print(f"\nNew Total Earned SU Credits: {new_total_credits:.2f}")
    print(f"New Total Earned ECTS: {new_total_ects:.2f}")
    print(f"New CGPA: {new_cgpa:.2f}")

if __name__ == "__main__":
    main()
