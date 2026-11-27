# type_check_demo.py
from typing import List, Dict, Optional, Union
from literal_types import Status, Priority
from typed_dict_example import PersonDict, EmployeeDict

def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

def process_user_data(user: PersonDict) -> str:
    """Process user data and return a summary."""
    return f"User: {user['name']}, Age: {user['age']}, Email: {user['email']}"

def update_status(current_status: Status, new_status: Status) -> Status:
    """Update status with validation."""
    valid_transitions = {
        "pending": ["approved", "rejected"],
        "approved": ["pending"],
        "rejected": ["pending"]
    }
    
    if new_status in valid_transitions.get(current_status, []):
        return new_status
    else:
        raise ValueError(f"Invalid transition from {current_status} to {new_status}")

def find_employee_by_id(employees: List[EmployeeDict], emp_id: int) -> Optional[EmployeeDict]:
    """Find an employee by ID."""
    for employee in employees:
        if employee["id"] == emp_id:
            return employee
    return None

# Corrected version
def corrected_function() -> tuple[float, PersonDict, Status, str]:
    """This function has proper type usage."""
    
    # Correct: Passing proper types
    result1 = calculate_average([1.0, 2.0, 3.0])
    
    # Correct: Complete PersonDict
    good_user: PersonDict = {
        "name": "John",
        "age": 30,
        "email": "john@example.com"
    }
    
    # Correct: Valid literal value
    status = update_status("pending", "approved")
    
    # Correct: Proper return type
    def get_number() -> int:
        return 42
    
    # Correct: Handle None case
    employees: List[EmployeeDict] = []
    employee = find_employee_by_id(employees, 123)
    if employee is not None:
        name = employee["personal_info"]["name"]
    else:
        name = "Employee not found"
    
    return result1, good_user, status, name

if __name__ == "__main__":
    print("Running corrected function:")
    result = corrected_function()
    print(f"Results: {result}")
