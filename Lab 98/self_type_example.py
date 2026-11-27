# self_type_example.py
from typing import Self, List, Optional
from datetime import datetime

class ChainableCalculator:
    """A calculator that supports method chaining using Self type."""
    
    def __init__(self, initial_value: float = 0) -> None:
        self.value = initial_value
        self.history: List[str] = []
    
    def add(self, number: float) -> Self:
        """Add a number and return self for chaining."""
        old_value = self.value
        self.value += number
        self.history.append(f"{old_value} + {number} = {self.value}")
        return self
    
    def subtract(self, number: float) -> Self:
        """Subtract a number and return self for chaining."""
        old_value = self.value
        self.value -= number
        self.history.append(f"{old_value} - {number} = {self.value}")
        return self
    
    def multiply(self, number: float) -> Self:
        """Multiply by a number and return self for chaining."""
        old_value = self.value
        self.value *= number
        self.history.append(f"{old_value} * {number} = {self.value}")
        return self
    
    def divide(self, number: float) -> Self:
        """Divide by a number and return self for chaining."""
        if number == 0:
            raise ValueError("Cannot divide by zero")
        old_value = self.value
        self.value /= number
        self.history.append(f"{old_value} / {number} = {self.value}")
        return self
    
    def reset(self) -> Self:
        """Reset the calculator and return self for chaining."""
        self.value = 0
        self.history.append("Reset to 0")
        return self
    
    def get_result(self) -> float:
        """Get the current result."""
        return self.value
    
    def get_history(self) -> List[str]:
        """Get the calculation history."""
        return self.history.copy()

class Builder:
    """A builder pattern example using Self type."""
    
    def __init__(self) -> None:
        self.data: dict = {}
    
    def set_name(self, name: str) -> Self:
        """Set the name and return self."""
        self.data["name"] = name
        return self
    
    def set_age(self, age: int) -> Self:
        """Set the age and return self."""
        self.data["age"] = age
        return self
    
    def set_email(self, email: str) -> Self:
        """Set the email and return self."""
        self.data["email"] = email
        return self
    
    def add_skill(self, skill: str) -> Self:
        """Add a skill and return self."""
        if "skills" not in self.data:
            self.data["skills"] = []
        self.data["skills"].append(skill)
        return self
    
    def build(self) -> dict:
        """Build and return the final object."""
        return self.data.copy()

# Example usage
if __name__ == "__main__":
    # Test ChainableCalculator
    calc = ChainableCalculator(10)
    result = (calc
              .add(5)
              .multiply(2)
              .subtract(3)
              .divide(2)
              .get_result())
    
    print(f"Final result: {result}")
    print("Calculation history:")
    for step in calc.get_history():
        print(f"  {step}")
    
    # Test Builder pattern
    person = (Builder()
              .set_name("John Doe")
              .set_age(30)
              .set_email("john@example.com")
              .add_skill("Python")
              .add_skill("JavaScript")
              .add_skill("SQL")
              .build())
    
    print("\nBuilt person:", person)
