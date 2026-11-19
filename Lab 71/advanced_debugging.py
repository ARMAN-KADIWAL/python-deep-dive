# advanced_debugging.py - Complex debugging scenario
import pdb

class StudentGradeCalculator:
    def __init__(self):
        self.students = {}
    
    def add_student(self, name, grades):
        """Add a student with their grades"""
        print(f"Adding student: {name}")
        pdb.set_trace()  # Breakpoint 1
        
        if not isinstance(grades, list):
            print("Error: Grades must be a list")
            return False
        
        self.students[name] = grades
        return True
    
    def calculate_average(self, name):
        """Calculate average grade for a student"""
        print(f"Calculating average for: {name}")
        pdb.set_trace()  # Breakpoint 2
        
        if name not in self.students:
            return None
        
        grades = self.students[name]
        if len(grades) == 0:
            return 0
        
        total = sum(grades)
        average = total / len(grades)
        return average
    
    def get_letter_grade(self, average):
        """Convert numerical average to letter grade"""
        print(f"Converting {average} to letter grade")
        pdb.set_trace()  # Breakpoint 3
        
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'
    
    def generate_report(self, name):
        """Generate a grade report for a student"""
        print(f"Generating report for: {name}")
        
        average = self.calculate_average(name)
        if average is None:
            return f"Student {name} not found"
        
        letter_grade = self.get_letter_grade(average)
        return f"Student: {name}, Average: {average:.2f}, Grade: {letter_grade}"

def main():
    print("=== Student Grade Calculator ===")
    
    calculator = StudentGradeCalculator()
    
    # Add some students
    calculator.add_student("Alice", [85, 92, 78, 96])
    calculator.add_student("Bob", [72, 68, 75, 80])
    calculator.add_student("Charlie", [])  # Empty grades list
    
    # Generate reports
    students = ["Alice", "Bob", "Charlie", "David"]  # David doesn't exist
    
    for student in students:
        print(f"\n--- Report for {student} ---")
        report = calculator.generate_report(student)
        print(report)

if __name__ == "__main__":
    main()
