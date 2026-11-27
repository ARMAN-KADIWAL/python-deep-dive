# basic_generics.py
from typing import List, Tuple, Dict, Set, Optional, Union

def process_names(names: List[str]) -> List[str]:
    """Process a list of names and return them in uppercase."""
    return [name.upper() for name in names]

def create_person_info(name: str, age: int) -> Tuple[str, int]:
    """Create a tuple containing person information."""
    return (name, age)

def get_student_grades(students: Dict[str, int]) -> Dict[str, str]:
    """Convert numeric grades to letter grades."""
    grade_map = {
        90: 'A', 80: 'B', 70: 'C', 60: 'D'
    }
    
    result: Dict[str, str] = {}
    for student, grade in students.items():
        for min_grade in sorted(grade_map.keys(), reverse=True):
            if grade >= min_grade:
                result[student] = grade_map[min_grade]
                break
        else:
            result[student] = 'F'
    
    return result

def find_unique_numbers(numbers: List[int]) -> Set[int]:
    """Return unique numbers from a list."""
    return set(numbers)

def get_optional_value(data: Dict[str, int], key: str) -> Optional[int]:
    """Get a value from dictionary that might not exist."""
    return data.get(key)

def process_mixed_data(data: Union[str, int, List[str]]) -> str:
    """Process data that can be of multiple types."""
    if isinstance(data, str):
        return f"String: {data}"
    elif isinstance(data, int):
        return f"Integer: {data}"
    else:
        return f"List with {len(data)} items"

# Example usage
if __name__ == "__main__":
    # Test the functions
    names = ["alice", "bob", "charlie"]
    print("Processed names:", process_names(names))
    
    person = create_person_info("John", 25)
    print("Person info:", person)
    
    grades = {"Alice": 95, "Bob": 87, "Charlie": 72}
    print("Letter grades:", get_student_grades(grades))
    
    numbers = [1, 2, 2, 3, 3, 4]
    print("Unique numbers:", find_unique_numbers(numbers))
    
    value = get_optional_value(grades, "Alice")
    print("Optional value:", value)
    
    print("Mixed data processing:", process_mixed_data("Hello"))
    print("Mixed data processing:", process_mixed_data(42))
    print("Mixed data processing:", process_mixed_data(["a", "b", "c"]))
