# Final Clean Calculator - Simplified Conditionals and Loops
import math
from typing import List, Union, Callable, Dict, Any

class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass

class Calculator:
    """A clean, well-structured calculator class."""
    
    def __init__(self):
        self.operations = {
            "add": self._add,
            "subtract": self._subtract,
            "sub": self._subtract,
            "multiply": self._multiply,
            "mul": self._multiply,
            "divide": self._divide,
            "div": self._divide,
            "power": self._power,
            "sqrt": self._square_root
        }
    
    def _add(self, first: float, second: float, third: float = 0) -> float:
        """Add numbers together."""
        result = first + second
        return result + third if third != 0 else result
    
    def _subtract(self, first: float, second: float, third: float = 0) -> float:
        """Subtract numbers."""
        result = first - second
        return result - third if third != 0 else result
    
    def _multiply(self, first: float, second: float, third: float = 0) -> float:
        """Multiply numbers."""
        result = first * second
        return result * third if third != 0 else result
    
    def _divide(self, first: float, second: float, third: float = 0) -> float:
        """Divide numbers with zero-division protection."""
        if second == 0 or (third != 0 and third == 0):  # Fixed redundant check
            raise CalculationError("Division by zero")
        
        result = first / second
        return result / third if third != 0 else result
    
    def _power(self, base: float, exponent: float, second_exponent: float = 0) -> float:
        """Calculate power of numbers."""
        result = base ** exponent
        return result ** second_exponent if second_exponent != 0 else result
    
    def _square_root(self, number: float, *args) -> float:
        """Calculate square root."""
        if number < 0:
            raise CalculationError("Cannot calculate square root of negative number")
        return math.sqrt(number)
    
    def calculate(self, first: float, second: float, third: float, operation: str) -> Union[float, str]:
        """Perform calculation based on operation type."""
        operation_lower = operation.lower()
        
        if operation_lower not in self.operations:
            return f"Error: Unknown operation '{operation}'"
        
        try:
            return self.operations[operation_lower](first, second, third)
        except CalculationError as error:
            return f"Error: {error}"

class DataProcessor:
    """A class for processing numerical data."""
    
    @staticmethod
    def calculate_sum(numbers: List[float]) -> float:
        """Calculate sum using built-in function."""
        return sum(numbers)
    
    @staticmethod
    def calculate_average(numbers: List[float]) -> float:
        """Calculate average of numbers."""
        return sum(numbers) / len(numbers) if numbers else 0
    
    @staticmethod
    def find_extreme(numbers: List[float], find_max: bool = True) -> Union[float, None]:
        """Find maximum or minimum value."""
        if not numbers:
            return None
        return max(numbers) if find_max else min(numbers)
    
    @classmethod
    def calculate_statistics(cls, data: List[float]) -> Dict[str, Union[float, None]]:
        """Calculate comprehensive statistics."""
        if not data:
            return {'total': 0, 'average': 0, 'maximum': None, 'minimum': None}
        
        return {
            'total': cls.calculate_sum(data),
            'average': cls.calculate_average(data),
            'maximum': cls.find_extreme(data, find_max=True),
            'minimum': cls.find_extreme(data, find_max=False)
        }
    
    @staticmethod
    def display_statistics(statistics: Dict[str, Any]) -> None:
        """Display statistics in a clean format."""
        for name, value in statistics.items():
            formatted_name = name.replace('_', ' ').title()
            print(f"{formatted_name}: {value}")

def demonstrate_calculator():
    """Demonstrate calculator functionality."""
    calculator = Calculator()
    
    test_cases = [
        (10, 5, 2, "add"),
        (10, 5, 2, "multiply"),
        (16, 0, 0, "sqrt"),
        (10, 0, 0, "divide")
    ]
    
    print("Calculator Results:")
    for first, second, third, operation in test_cases:
        result = calculator.calculate(first, second, third, operation)
        print(f"{operation}({first}, {second}, {third}) = {result}")

def demonstrate_data_processing():
    """Demonstrate data processing functionality."""
    processor = DataProcessor()
    sample_data = [10, 20, 30, 40, 50]
    
    print("\nData Processing Results:")
    statistics = processor.calculate_statistics(sample_data)
    processor.display_statistics(statistics)

def main():
    """Main function to run demonstrations."""
    demonstrate_calculator()
    demonstrate_data_processing()

if __name__ == "__main__":
    main()
