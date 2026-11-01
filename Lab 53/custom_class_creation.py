"""Track class attributes and inheritance during class creation."""


class AttributeTracker(type):
    created_classes = []

    def __new__(mcls, name, bases, attrs):
        attr_info = {
            key: type(value).__name__
            for key, value in attrs.items()
            if not key.startswith("__")
        }
        attrs["_attribute_info"] = attr_info
        attrs["_class_name"] = name
        new_class = super().__new__(mcls, name, bases, attrs)
        mcls.created_classes.append({
            "name": name,
            "attributes": attr_info,
            "bases": [base.__name__ for base in bases],
        })
        return new_class

    @classmethod
    def get_class_info(mcls):
        return list(mcls.created_classes)


class Person(metaclass=AttributeTracker):
    name = "Unknown"
    age = 0

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old"

    def celebrate_birthday(self):
        self.age += 1
        return f"Happy birthday! Now {self.age} years old"


class Student(Person):
    student_id = "000000"
    grade = "A"

    def study(self, subject):
        return f"{self.name} is studying {subject}"


class Teacher(Person):
    employee_id = "T000"
    subject = "General"

    def teach(self, topic):
        return f"Teaching {topic} in {self.subject}"


def main():
    print("=== Class Creation with AttributeTracker ===")
    for info in AttributeTracker.get_class_info():
        print(f"\nClass: {info['name']}")
        print("Inherits from:", info["bases"])
        print("Attributes:", info["attributes"])

    student = Student()
    student.name = "Alice"
    student.age = 20
    student.student_id = "S12345"
    print("\nStudent info:", student._attribute_info)
    print("Student introduction:", student.introduce())
    print("Student studying:", student.study("Python Programming"))

    teacher = Teacher()
    teacher.name = "Dr. Smith"
    teacher.age = 45
    teacher.subject = "Computer Science"
    print("\nTeacher info:", teacher._attribute_info)
    print("Teacher introduction:", teacher.introduce())
    print("Teacher teaching:", teacher.teach("Metaclasses"))


if __name__ == "__main__":
    main()
