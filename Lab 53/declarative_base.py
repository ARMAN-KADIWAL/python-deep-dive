"""A lightweight SQLAlchemy-style declarative base built with a metaclass."""


class Integer:
    pass


class String:
    def __init__(self, length=None):
        self.length = length


class Column:
    def __init__(self, type_class, primary_key=False, nullable=True, default=None):
        self.type_class = type_class
        self.primary_key = primary_key
        self.nullable = nullable and not primary_key
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def validate(self, value):
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column {self.name} cannot be null")
            return
        if self.type_class is Integer:
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"Column {self.name} expects integer, got {type(value).__name__}")
        elif isinstance(self.type_class, String):
            if not isinstance(value, str):
                raise TypeError(f"Column {self.name} expects string, got {type(value).__name__}")
            if self.type_class.length is not None and len(value) > self.type_class.length:
                raise ValueError(f"Column {self.name} exceeds maximum length {self.type_class.length}")

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def __repr__(self):
        type_name = self.type_class.__name__ if isinstance(self.type_class, type) else "String"
        return f"Column({type_name}, pk={self.primary_key})"


class DeclarativeMeta(type):
    def __new__(mcls, name, bases, attrs):
        if name == "Base":
            return super().__new__(mcls, name, bases, attrs)

        columns = {}
        for base in bases:
            columns.update(getattr(base, "__columns__", {}))
        for key, value in attrs.items():
            if isinstance(value, Column):
                columns[key] = value

        attrs["__tablename__"] = attrs.get("__tablename__", name.lower())
        attrs["__columns__"] = columns

        def __init__(self, **kwargs):
            unknown = set(kwargs) - set(self.__columns__)
            if unknown:
                raise TypeError(f"Unknown column(s) for {name}: {sorted(unknown)}")
            for column_name, column in self.__columns__.items():
                setattr(self, column_name, kwargs.get(column_name, column.default))

        def to_dict(self):
            return {column_name: getattr(self, column_name) for column_name in self.__columns__}

        def __repr__(self):
            values = ", ".join(
                f"{column_name}={getattr(self, column_name)!r}"
                for column_name in self.__columns__
            )
            return f"{name}({values})"

        attrs["__init__"] = __init__
        attrs["to_dict"] = to_dict
        attrs["__repr__"] = __repr__
        return super().__new__(mcls, name, bases, attrs)


class Base(metaclass=DeclarativeMeta):
    pass


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer, default=0)


class Article(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(5000), nullable=False)
    author = Column(String(100), nullable=False)
    views = Column(Integer, default=0)


def main():
    print("=== SQLAlchemy-Style Declarative Base ===")
    user = User(id=1, username="john_doe", email="john@example.com", age=25)
    print("User:", user)
    print("User table:", User.__tablename__)
    print("User columns:", User.__columns__)
    print("User dictionary:", user.to_dict())

    article = Article(
        id=1,
        title="Understanding Metaclasses",
        content="A practical introduction to Python metaclasses.",
        author="John Smith",
    )
    print("\nArticle:", article)
    print("Article table:", Article.__tablename__)
    print("Article dictionary:", article.to_dict())

    print("\n=== Validation checks ===")
    try:
        User(id=2, username="x" * 60, email="x@example.com")
    except ValueError as error:
        print("Length validation:", error)
    try:
        User(id=3, username=None, email="x@example.com")
    except ValueError as error:
        print("Null validation:", error)
    try:
        User(id=4, username="valid", email="x@example.com", age="twenty")
    except TypeError as error:
        print("Type validation:", error)


if __name__ == "__main__":
    main()
