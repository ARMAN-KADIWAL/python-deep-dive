# type_guard_example.py
from typing import TypeGuard, Union, List, Any, Dict, Optional

def is_string(value: Any) -> TypeGuard[str]:
    """Type guard to check if value is a string."""
    return isinstance(value, str)

def is_int(value: Any) -> TypeGuard[int]:
    """Type guard to check if value is an integer."""
    return isinstance(value, int)

def is_list_of_strings(value: Any) -> TypeGuard[List[str]]:
    """Type guard to check if value is a list of strings."""
    return (isinstance(value, list) and 
            all(isinstance(item, str) for item in value))

def is_dict_str_int(value: Any) -> TypeGuard[Dict[str, int]]:
    """Type guard to check if value is a dict with string keys and int values."""
    return (isinstance(value, dict) and
            all(isinstance(k, str) and isinstance(v, int) 
                for k, v in value.items()))

def process_mixed_input(data: Union[str, int, List[str], Dict[str, int]]) -> str:
    """Process different types of input using type guards."""
    
    if is_string(data):
        # TypeGuard ensures data is str here
        return f"Processing string: '{data}' (length: {len(data)})"
    
    elif is_int(data):
        # TypeGuard ensures data is int here
        return f"Processing integer: {data} (squared: {data ** 2})"
    
    elif is_list_of_strings(data):
        # TypeGuard ensures data is List[str] here
        return f"Processing string list: {len(data)} items, joined: '{', '.join(data)}'"
    
    elif is_dict_str_int(data):
        # TypeGuard ensures data is Dict[str, int] here
        total = sum(data.values())
        return f"Processing dict: {len(data)} items, sum of values: {total}"
    
    else:
        return "Unknown data type"

def filter_strings(items: List[Any]) -> List[str]:
    """Filter a list to return only string items."""
    result: List[str] = []
    for item in items:
        if is_string(item):
            # TypeGuard ensures item is str here
            result.append(item)
    return result

def safe_string_operations(value: Any) -> Optional[str]:
    """Safely perform string operations only if value is a string."""
    if is_string(value):
        # TypeGuard ensures value is str here
        return value.upper().strip()
    return None

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"

def is_person(value: Any) -> TypeGuard[Person]:
    """Type guard to check if value is a Person instance."""
    return isinstance(value, Person)

def process_person_data(data: Union[Person, Dict[str, Any], str]) -> str:
    """Process different representations of person data."""
    
    if is_person(data):
        # TypeGuard ensures data is Person here
        return f"Person object: {data.name} is {data.age} years old"
    
    elif isinstance(data, dict) and "name" in data and "age" in data:
        return f"Person dict: {data['name']} is {data['age']} years old"
    
    elif is_string(data):
        # TypeGuard ensures data is str here
        return f"Person name only: {data}"
    
    else:
        return "Invalid person data"

# Example usage
if __name__ == "__main__":
    # Test type guards with mixed data
    test_data: List[Any] = [
        "Hello World",
        42,
        ["apple", "banana", "cherry"],
        {"alice": 25, "bob": 30, "charlie": 35},
        [1, 2, 3],  # This won't match any type guard
        {"invalid": "dict"}  # This won't match the dict type guard
    ]
    
    print("Processing mixed input:")
    for i, data in enumerate(test_data):
        result = process_mixed_input(data)
        print(f"  {i+1}. {result}")
    
    # Test filtering strings
    mixed_items = ["hello", 123, "world", 45.6, "python", True, "typing"]
    strings_only = filter_strings(mixed_items)
    print(f"\nFiltered strings: {strings_only}")
    
    # Test safe string operations
    test_values = ["  Hello World  ", 123, None, "PYTHON"]
    print("\nSafe string operations:")
    for value in test_values:
        string_result = safe_string_operations(value)
        print(f"  {value} -> {string_result}")
    
    # Test person data processing
    person_obj = Person("Alice", 30)
    person_dict = {"name": "Bob", "age": 25}
    person_name = "Charlie"
    
    print("\nProcessing person data:")
    print(f"  {process_person_data(person_obj)}")
    print(f"  {process_person_data(person_dict)}")
    print(f"  {process_person_data(person_name)}")
