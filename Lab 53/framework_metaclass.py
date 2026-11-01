"""Framework-style model metaclasses and a small in-memory query manager."""


class Field:
    def __init__(self, max_length=None, required=True, default=None):
        self.max_length = max_length
        self.required = required
        self.default = default

    def validate(self, value):
        if self.required and value is None:
            raise ValueError("This field is required")
        return True


class CharField(Field):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Value must be a string")
            if self.max_length and len(value) > self.max_length:
                raise ValueError(f"Value too long (max {self.max_length} characters)")
        return True


class IntegerField(Field):
    def validate(self, value):
        super().validate(value)
        if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
            raise ValueError("Value must be an integer")
        return True


class EmailField(CharField):
    def validate(self, value):
        super().validate(value)
        if value is not None and ("@" not in value or "." not in value.rsplit("@", 1)[-1]):
            raise ValueError("Invalid email format")
        return True


class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        if name == "Model":
            return super().__new__(mcls, name, bases, attrs)

        fields = {}
        for base in bases:
            fields.update(getattr(base, "_fields", {}))
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                del attrs[key]

        attrs["_fields"] = fields
        attrs["_model_name"] = name

        def __init__(self, **kwargs):
            unknown = set(kwargs) - set(self._fields)
            if unknown:
                raise AttributeError(f"{name} has no field(s): {sorted(unknown)}")
            for field_name, field in self._fields.items():
                setattr(self, field_name, kwargs.get(field_name, field.default))

        def full_clean(self):
            for field_name, field in self._fields.items():
                try:
                    field.validate(getattr(self, field_name))
                except ValueError as error:
                    raise ValueError(f"Field '{field_name}': {error}") from error

        def save(self):
            self.full_clean()
            print(f"Saving {self._model_name}: {self}")
            return True

        def to_dict(self):
            return {field_name: getattr(self, field_name) for field_name in self._fields}

        def __str__(self):
            values = [f"{field}={getattr(self, field)}" for field in self._fields]
            return f"{name}({', '.join(values)})"

        attrs["__init__"] = __init__
        attrs["full_clean"] = full_clean
        attrs["save"] = save
        attrs["to_dict"] = to_dict
        attrs["__str__"] = __str__
        new_class = super().__new__(mcls, name, bases, attrs)
        print(f"Created model '{name}' with fields: {list(fields)}")
        return new_class


class Model(metaclass=ModelMeta):
    pass


class User(Model):
    username = CharField(max_length=50, required=True)
    email = EmailField(max_length=100, required=True)
    age = IntegerField(required=False, default=0)
    is_active = Field(required=False, default=True)


class Article(Model):
    title = CharField(max_length=200, required=True)
    content = CharField(max_length=5000, required=True)
    author = CharField(max_length=100, required=True)
    views = IntegerField(required=False, default=0)


class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.objects = []

    def create(self, **kwargs):
        instance = self.model_class(**kwargs)
        instance.save()
        self.objects.append(instance)
        return instance

    def all(self):
        return self.objects.copy()

    def filter(self, **kwargs):
        unknown = set(kwargs) - set(self.model_class._fields)
        if unknown:
            raise AttributeError(f"Unknown filter field(s): {sorted(unknown)}")
        return [
            instance for instance in self.objects
            if all(getattr(instance, key) == value for key, value in kwargs.items())
        ]


class AdvancedModelMeta(ModelMeta):
    def __new__(mcls, name, bases, attrs):
        new_class = super().__new__(mcls, name, bases, attrs)
        if name != "AdvancedModel":
            new_class.objects = QuerySet(new_class)
        return new_class


class AdvancedModel(Model, metaclass=AdvancedModelMeta):
    pass


class Product(AdvancedModel):
    name = CharField(max_length=100, required=True)
    price = IntegerField(required=True)
    category = CharField(max_length=50, required=True)
    in_stock = Field(required=False, default=True)


def main():
    print("=== Framework-Style Metaclass Demo ===")
    print("\n--- Basic Model Usage ---")
    user1 = User(username="john_doe", email="john@example.com", age=25)
    print("Created user:", user1)
    user1.save()
    user2 = User(username="jane_smith", email="jane@example.com")
    print("Created user:", user2)
    user2.save()

    print("\n--- Testing Validation ---")
    try:
        User(username="", email="invalid-email").save()
    except ValueError as error:
        print("Validation caught:", error)

    print("\n--- Advanced Model with ORM Features ---")
    Product.objects.create(name="Laptop", price=999, category="Electronics")
    Product.objects.create(name="Book", price=25, category="Education")
    Product.objects.create(name="Phone", price=599, category="Electronics")
    print("All products:", len(Product.objects.all()))
    electronics = Product.objects.filter(category="Electronics")
    print("Electronics:", [product.name for product in electronics])
    expensive = Product.objects.filter(price=999)
    print("Expensive items:", [product.name for product in expensive])
    print("\nProduct fields:", list(Product._fields))
    print("User fields:", list(User._fields))


if __name__ == "__main__":
    main()
