"""Validate required methods and method signatures at class creation."""
import inspect


class MethodValidator(type):
    REQUIRED_METHODS = ["validate", "serialize"]

    def __new__(mcls, name, bases, attrs):
        if not bases:
            return super().__new__(mcls, name, bases, attrs)

        missing_methods = []
        for required_name in mcls.REQUIRED_METHODS:
            method = attrs.get(required_name)
            if method is None:
                method = next(
                    (getattr(base, required_name) for base in bases
                     if hasattr(base, required_name)),
                    None,
                )
            if method is None:
                missing_methods.append(required_name)

        if missing_methods:
            raise TypeError(
                f"Class '{name}' is missing required methods: {missing_methods}"
            )

        validate_method = attrs.get("validate")
        if validate_method is not None and callable(validate_method):
            signature = inspect.signature(validate_method)
            if len(signature.parameters) != 1:
                raise TypeError(
                    f"Method 'validate' in class '{name}' should only take 'self'"
                )

        attrs["_validated_by"] = mcls.__name__
        attrs["_required_methods"] = mcls.REQUIRED_METHODS.copy()
        print(f"Class '{name}' passed validation")
        return super().__new__(mcls, name, bases, attrs)


class ValidatedBase(metaclass=MethodValidator):
    def validate(self):
        return True

    def serialize(self):
        return {}


class User(ValidatedBase):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def validate(self):
        return bool(self.username and len(self.username) >= 3 and "@" in self.email)

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "valid": self.validate(),
        }


class Product(ValidatedBase):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def validate(self):
        return bool(self.name) and self.price > 0

    def serialize(self):
        return {"name": self.name, "price": self.price, "valid": self.validate()}


def main():
    print("=== Testing Method Validation Metaclass ===")
    user = User("john_doe", "john@example.com")
    print("User validation:", user.validate())
    print("User serialization:", user.serialize())
    product = Product("Laptop", 999.99)
    print("Product validation:", product.validate())
    print("Product serialization:", product.serialize())
    print("\nUser class validated by:", User._validated_by)
    print("Required methods:", User._required_methods)

    print("\n=== Testing Invalid Class Creation ===")
    class BareBase(metaclass=MethodValidator):
        pass

    try:
        class InvalidClass(BareBase):
            def some_other_method(self):
                return None
    except TypeError as error:
        print("Error creating invalid class:", error)

    try:
        class WrongSignature(ValidatedBase):
            def validate(self, extra_param):
                return True
            def serialize(self):
                return {}
    except TypeError as error:
        print("Error with wrong signature:", error)


if __name__ == "__main__":
    main()
