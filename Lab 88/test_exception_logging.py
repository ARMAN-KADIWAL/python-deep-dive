# Create file: test_exception_logging.py
from exception_logger import ExceptionLogger, setup_global_exception_handler
import time

def test_exception_logging():
    """Test various exception logging scenarios"""
    
    # Set up global exception handler
    setup_global_exception_handler()
    
    # Create exception logger
    exc_logger = ExceptionLogger('test_exceptions')
    
    print("Testing exception logging...")
    
    # Test 1: Basic exception logging
    print("\n1. Testing basic exception logging:")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        exc_logger.log_exception(context={'test': 'division_by_zero'})
    
    # Test 2: Exception with decorator
    print("\n2. Testing exception decorator:")
    
    @exc_logger.exception_decorator(reraise=False, context={'test': 'decorator'})
    def problematic_function(x, y):
        """Function that will cause an exception"""
        if y == 0:
            raise ValueError("Y cannot be zero!")
        return x / y
    
    result = problematic_function(10, 0)
    print(f"Function result: {result}")
    
    # Test 3: Multiple exception types
    print("\n3. Testing multiple exception types:")
    
    exceptions_to_test = [
        (lambda: [][10], "IndexError"),
        (lambda: {'a': 1}['b'], "KeyError"),
        (lambda: int('not_a_number'), "ValueError"),
        (lambda: open('nonexistent_file.txt'), "FileNotFoundError")
    ]
    
    for func, desc in exceptions_to_test:
        try:
            func()
        except Exception:
            exc_logger.log_exception(context={'test_type': desc})
    
    # Test 4: Nested exceptions
    print("\n4. Testing nested exceptions:")
    
    def outer_function():
        def inner_function():
            raise RuntimeError("Inner function error")
        
        try:
            inner_function()
        except RuntimeError as e:
            raise ValueError("Outer function error") from e
    
    try:
        outer_function()
    except Exception:
        exc_logger.log_exception(context={'test': 'nested_exceptions'})
    
    print("\nException logging tests complete!")
    print("Check exception_logs.log and exception_logs.json for detailed logs")

if __name__ == "__main__":
    test_exception_logging()
