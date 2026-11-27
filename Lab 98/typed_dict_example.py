# typed_dict_example.py
from typing import TypedDict, List, Optional, NotRequired
from datetime import datetime

# Define TypedDict classes for structured data
class PersonDict(TypedDict):
    name: str
    age: int
    email: str

class AddressDict(TypedDict):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class EmployeeDict(TypedDict):
    id: int
    personal_info: PersonDict
    address: AddressDict
    department: str
    salary: float
    start_date: str

# TypedDict with optional fields (Python 3.11+)
class ProductDict(TypedDict):
    id: int
    name: str
    price: float
    description: NotRequired[str]  # Optional field
    category: NotRequired[str]     # Optional field

def create_person(name: str, age: int, email: str) -> PersonDict:
    """Create a person dictionary with proper typing."""
    return {
        "name": name,
        "age": age,
        "email": email
    }

def create_employee(
    emp_id: int,
    person: PersonDict,
    address: AddressDict,
    department: str,
    salary: float
) -> EmployeeDict:
    """Create an employee record."""
    return {
        "id": emp_id,
        "personal_info": person,
        "address": address,
        "department": department,
        "salary": salary,
        "start_date": datetime.now().strftime("%Y-%m-%d")
    }

def process_employees(employees: List[EmployeeDict]) -> Dict[str, float]:
    """Calculate average salary by department."""
    from collections import defaultdict
    
    dept_salaries: Dict[str, List[float]] = defaultdict(list)
    
    for employee in employees:
        dept = employee["department"]
        salary = employee["salary"]
        dept_salaries[dept].append(salary)
    
    return {
        dept: sum(salaries) / len(salaries)
        for dept, salaries in dept_salaries.items()
    }

def create_product(
    product_id: int,
    name: str,
    price: float,
    description: Optional[str] = None,
    category: Optional[str] = None
) -> ProductDict:
    """Create a product dictionary."""
    product: ProductDict = {
        "id": product_id,
        "name": name,
        "price": price
    }
    
    if description is not None:
        product["description"] = description
    if category is not None:
        product["category"] = category
    
    return product

# Example usage
if __name__ == "__main__":
    # Create sample data
    person1 = create_person("Alice Johnson", 30, "alice@example.com")
    address1: AddressDict = {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "country": "USA"
    }
    
    employee1 = create_employee(1001, person1, address1, "Engineering", 75000.0)
    
    person2 = create_person("Bob Smith", 28, "bob@example.com")
    address2: AddressDict = {
        "street": "456 Oak Ave",
        "city": "San Francisco",
        "state": "CA",
        "zip_code": "94102",
        "country": "USA"
    }
    
    employee2 = create_employee(1002, person2, address2, "Marketing", 65000.0)
    
    employees = [employee1, employee2]
    
    print("Employee 1:", employee1["personal_info"]["name"])
    print("Department averages:", process_employees(employees))
    
    # Create products
    product1 = create_product(1, "Laptop", 999.99, "High-performance laptop", "Electronics")
    product2 = create_product(2, "Mouse", 29.99)  # No description or category
    
    print("Product 1:", product1)
    print("Product 2:", product2)
