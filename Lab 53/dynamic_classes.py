"""Create classes dynamically with type() and a custom metaclass."""


class DynamicMeta(type):
    def __new__(mcls, name, bases, attrs):
        attrs["_created_dynamically"] = True
        attrs["_creation_method"] = "type_function"

        def get_info(self):
            return {
                "class_name": self.__class__.__name__,
                "created_dynamically": getattr(self, "_created_dynamically", False),
                "creation_method": getattr(self, "_creation_method", "unknown"),
                "attributes": [
                    attribute for attribute in dir(self)
                    if not attribute.startswith("_")
                ],
            }

        attrs["get_info"] = get_info
        return super().__new__(mcls, name, bases, attrs)


def _build_model_attributes(class_name, fields, methods=None):
    fields = tuple(fields)

    def __init__(self, **kwargs):
        unknown = set(kwargs) - set(fields)
        if unknown:
            raise TypeError(f"Unknown fields for {class_name}: {sorted(unknown)}")
        for field in fields:
            setattr(self, field, kwargs.get(field))

    def __str__(self):
        values = [f"{field}={getattr(self, field)}" for field in fields]
        return f"{class_name}({', '.join(values)})"

    attributes = {
        "__init__": __init__,
        "__str__": __str__,
        "__repr__": __str__,
        "_fields": fields,
    }
    if methods:
        attributes.update(methods)
    return attributes


def create_model_class(class_name, fields, methods=None):
    return type(class_name, (), _build_model_attributes(class_name, fields, methods))


def create_model_with_metaclass(class_name, fields, methods=None):
    return DynamicMeta(class_name, (), _build_model_attributes(class_name, fields, methods))


def main():
    print("=== Dynamic Class Creation with type() ===")
    Book = create_model_class(
        "Book",
        ["title", "author", "isbn", "price"],
        {
            "get_summary": lambda self: f"'{self.title}' by {self.author}",
            "is_expensive": lambda self: self.price > 50 if self.price is not None else False,
        },
    )
    book = Book(
        title="Python Metaclasses",
        author="John Smith",
        isbn="978-1234567890",
        price=45.99,
    )
    print("Book:", book)
    print("Summary:", book.get_summary())
    print("Is expensive:", book.is_expensive())
    print("Fields:", Book._fields)

    print("\n=== Dynamic Class with Custom Metaclass ===")
    Car = create_model_with_metaclass(
        "Car",
        ["make", "model", "year", "price"],
        {
            "get_age": lambda self: 2024 - self.year if self.year else 0,
            "is_vintage": lambda self: self.get_age() > 25,
        },
    )
    car = Car(make="Toyota", model="Camry", year=1995, price=5000)
    print("Car:", car)
    print("Age:", car.get_age())
    print("Is vintage:", car.is_vintage())
    print("Dynamic info:", car.get_info())

    models = {
        "Employee": {
            "fields": ["name", "employee_id", "department", "salary"],
            "methods": {
                "get_annual_salary": lambda self: self.salary * 12 if self.salary else 0,
                "promote": lambda self, new_salary: setattr(self, "salary", new_salary),
            },
        },
        "Course": {
            "fields": ["name", "code", "credits", "instructor"],
            "methods": {
                "is_full_course": lambda self: self.credits >= 3,
                "get_course_info": lambda self: f"{self.code}: {self.name} ({self.credits} credits)",
            },
        },
    }
    dynamic_classes = {
        name: create_model_with_metaclass(name, config["fields"], config["methods"])
        for name, config in models.items()
    }
    employee = dynamic_classes["Employee"](
        name="Alice Johnson", employee_id="E001",
        department="Engineering", salary=75000,
    )
    course = dynamic_classes["Course"](
        name="Advanced Python Programming", code="CS401",
        credits=4, instructor="Dr. Smith",
    )
    print("\nEmployee:", employee)
    print("Annual salary:", employee.get_annual_salary())
    print("Employee info:", employee.get_info())
    print("\nCourse:", course)
    print("Course info:", course.get_course_info())
    print("Is full course:", course.is_full_course())
    print("Course dynamic info:", course.get_info())


if __name__ == "__main__":
    main()
