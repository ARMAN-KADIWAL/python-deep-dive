"""Automated tests for Lab 53 metaclass examples."""
import unittest

from basic_metaclass import TestClass
from custom_class_creation import AttributeTracker, Student, Teacher
from validation_metaclass import MethodValidator, User as ValidatedUser, Product as ValidatedProduct
from dynamic_classes import create_model_class, create_model_with_metaclass
from framework_metaclass import User as FrameworkUser, Product as FrameworkProduct
from declarative_base import User as DeclarativeUser


class MetaclassLabTests(unittest.TestCase):
    def test_simple_metaclass(self):
        instance = TestClass()
        self.assertTrue(TestClass.class_id.endswith("_class"))
        self.assertIsNotNone(TestClass.created_at)
        self.assertEqual(instance.greet(), instance.enhanced_greet())
        self.assertEqual(instance.enhanced_calculate(2, 3), 5)

    def test_attribute_tracker(self):
        names = [entry["name"] for entry in AttributeTracker.get_class_info()]
        self.assertIn("Person", names)
        self.assertIn("Student", names)
        self.assertIn("Teacher", names)
        self.assertEqual(Student().study("Python"), "Unknown is studying Python")
        self.assertEqual(Teacher().teach("OOP"), "Teaching OOP in General")

    def test_method_validator(self):
        self.assertTrue(ValidatedUser("john_doe", "john@example.com").validate())
        self.assertTrue(ValidatedProduct("Laptop", 10).validate())

        class BareBase(metaclass=MethodValidator):
            pass

        with self.assertRaises(TypeError):
            class MissingMethods(BareBase):
                pass

        with self.assertRaises(TypeError):
            class WrongValidate(BareBase):
                def validate(self, extra):
                    return True
                def serialize(self):
                    return {}

    def test_dynamic_classes(self):
        Book = create_model_class("Book", ["title", "price"], {
            "is_expensive": lambda self: self.price > 50
        })
        book = Book(title="Python", price=100)
        self.assertTrue(book.is_expensive())
        Car = create_model_with_metaclass("Car", ["make"])
        car = Car(make="Toyota")
        self.assertTrue(car.get_info()["created_dynamically"])
        with self.assertRaises(TypeError):
            Book(title="Incomplete", extra="not allowed")

    def test_framework_style_models(self):
        user = FrameworkUser(username="john", email="john@example.com")
        self.assertTrue(user.save())
        with self.assertRaises(ValueError):
            FrameworkUser(username="", email="bad").save()
        FrameworkProduct.objects.objects.clear()
        FrameworkProduct.objects.create(name="Laptop", price=999, category="Electronics")
        FrameworkProduct.objects.create(name="Book", price=20, category="Education")
        self.assertEqual(len(FrameworkProduct.objects.filter(category="Electronics")), 1)

    def test_declarative_base(self):
        user = DeclarativeUser(id=1, username="john", email="john@example.com")
        self.assertEqual(user.age, 0)
        self.assertEqual(user.to_dict()["username"], "john")
        with self.assertRaises(ValueError):
            DeclarativeUser(id=2, username=None, email="john@example.com")
        with self.assertRaises(TypeError):
            DeclarativeUser(id=3, username="john", email="john@example.com", age="old")


if __name__ == "__main__":
    unittest.main(verbosity=2)
