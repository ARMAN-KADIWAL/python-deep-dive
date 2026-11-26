import unittest
from custom_exceptions_demo import (
    ValidationError, DatabaseConnectionError, InsufficientFundsError
)
from exception_hierarchy_demo import (
    ApplicationError, NetworkError, APIError, DataError,
    ValidationError as HierarchyValidationError
)


class TestErrorMessages(unittest.TestCase):
    def test_index_error(self):
        with self.assertRaises(IndexError):
            [1, 2, 3][5]

    def test_type_error(self):
        with self.assertRaises(TypeError):
            "10" * 5.5

    def test_value_error(self):
        with self.assertRaises(ValueError):
            int("hello")

    def test_validation(self):
        error = ValidationError("age", -5, int, "Age cannot be negative")
        self.assertIn("Age cannot be negative", str(error))

    def test_database(self):
        error = DatabaseConnectionError("localhost", 3306, "CONN_REFUSED")
        self.assertEqual(error.error_code, "CONN_REFUSED")

    def test_funds(self):
        error = InsufficientFundsError("ACC-1", 75, 50)
        self.assertIn("25.00", str(error))

    def test_hierarchy(self):
        self.assertTrue(issubclass(APIError, NetworkError))
        self.assertTrue(issubclass(NetworkError, ApplicationError))
        self.assertTrue(issubclass(HierarchyValidationError, DataError))
        self.assertTrue(issubclass(DataError, ApplicationError))

    def test_api_context(self):
        error = APIError("Invalid endpoint", endpoint="/invalid",
                         status_code=404, response_body="Not Found")
        self.assertEqual(error.context["status_code"], 404)


if __name__ == "__main__":
    unittest.main()
