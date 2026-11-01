"""A metaclass that adds class metadata and enhanced method aliases."""
from datetime import datetime


class SimpleMeta(type):
    def __new__(mcls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        attrs["class_id"] = f"{name.lower()}_class"
        new_attrs = {}
        for key, value in attrs.items():
            if callable(value) and not key.startswith("__"):
                new_attrs[f"enhanced_{key}"] = value
            new_attrs[key] = value
        print(f"Creating class '{name}' with SimpleMeta metaclass")
        return super().__new__(mcls, name, bases, new_attrs)

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        print(f"Initialized class '{name}' with {len(attrs)} attributes")


class TestClass(metaclass=SimpleMeta):
    def greet(self):
        return "Hello from TestClass!"

    def calculate(self, x, y):
        return x + y


def main():
    print("=== Testing SimpleMeta Metaclass ===")
    print("Class created at:", TestClass.created_at)
    print("Class ID:", TestClass.class_id)
    instance = TestClass()
    print("Original greet:", instance.greet())
    print("Enhanced greet:", instance.enhanced_greet())
    print("Calculate result:", instance.calculate(5, 3))
    print("Enhanced calculate:", instance.enhanced_calculate(10, 7))


if __name__ == "__main__":
    main()
