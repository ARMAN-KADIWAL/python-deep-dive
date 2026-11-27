# advanced_types.py
from typing import (
    List, Dict, Tuple, Optional, Union, Callable, Generic, TypeVar,
    Protocol, runtime_checkable, Awaitable, Iterator, Generator
)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import asyncio

# Type variables for generic programming
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Protocol for type-safe duck typing
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str:
        ...

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...
    
    @abstractmethod
    def perimeter(self) -> float:
        ...

@dataclass
class Rectangle(Shape):
    width: float
    height: float
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def draw(self) -> str:
        return f"Rectangle({self.width}x{self.height})"

@dataclass
class Circle(Shape):
    radius: float
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius
    
    def draw(self) -> str:
        return f"Circle(r={self.radius})"

# Generic container class
class Container(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, func: Callable[[T], K]) -> List[K]:
        return [func(item) for item in self._items]

# Complex function with multiple type parameters
def process_data_pipeline(
    data: List[Dict[str, Union[str, int, float]]],
    filters: List[Callable[[Dict[str, Union[str, int, float]]], bool]],
    transformers: List[Callable[[Dict[str, Union[str, int, float]]], Dict[str, Union[str, int, float]]]],
    aggregator: Callable[[List[Dict[str, Union[str, int, float]]]], Dict[str, Union[str, int, float]]]
) -> Tuple[List[Dict[str, Union[str, int, float]]], Dict[str, Union[str, int, float]]]:
    """
    Process data through a pipeline of filters, transformers, and aggregation.
    
    Returns:
        Tuple of (processed_data, aggregated_result)
    """
    # Apply filters
    filtered_data = data
    for filter_func in filters:
        filtered_data = [item for item in filtered_data if filter_func(item)]
    
    # Apply transformers
    transformed_data = filtered_data
    for transformer in transformers:
        transformed_data = [transformer(item) for item in transformed_data]
    
    # Apply aggregation
    aggregated = aggregator(transformed_data)
    
    return transformed_data, aggregated

# Async function with complex types
async def fetch_and_process_data(
    urls: List[str],
    processor: Callable[[str], Awaitable[Dict[str, Union[str, int]]]]
) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """Fetch data from URLs and process them asynchronously."""
    
    async def fetch_url(url: str) -> Tuple[str, Dict[str, Union[str, int]]]:
        # Simulate async data fetching
        await asyncio.sleep(0.1)
        result = await processor(url)
        return url, result
    
    # Process all URLs concurrently
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    # Group results by domain
    grouped: Dict[str, List[Dict[str, Union[str, int]]]] = {}
    for url, data in results:
        domain = url.split('/')[2] if '://' in url else url
        if domain not in grouped:
            grouped[domain] = []
        grouped[domain].append(data)
    
    return grouped

# Generator function with type hints
def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

# Higher-order function with complex types
def create_validator(
    rules: Dict[str, Callable[[Union[str, int, float]], bool]]
) -> Callable[[Dict[str, Union[str, int, float]]], Tuple[bool, List[str]]]:
    """Create a validator function from a set of rules."""
    
    def validator(data: Dict[str, Union[str, int, float]]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        
        for field, rule in rules.items():

            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not rule(data[field]):
                errors.append(f"Invalid value for field: {field}")
        return not errors, errors
    return validator


Record = Dict[str, Union[str, int, float]]


async def mock_processor(url: str) -> Dict[str, Union[str, int]]:
    return {"url": url, "length": len(url)}


def aggregate_records(records: List[Record]) -> Record:
    return {"count": len(records)}


if __name__ == "__main__":
    shapes: List[Shape] = [Rectangle(5, 3), Circle(4)]
    for shape in shapes:
        print(shape.area(), shape.perimeter())
        if isinstance(shape, Drawable):
            print(shape.draw())
    container = Container[int]()
    for number in range(5):
        container.add(number)
    print(container.find(lambda x: x % 2 == 0))
    print(container.filter(lambda x: x > 2))
    print(container.map(lambda x: x * 2))
    records: List[Record] = [{"status": "active"}, {"status": "inactive"}]
    print(process_data_pipeline(records, [lambda r: r["status"] == "active"], [], aggregate_records))
    print(asyncio.run(fetch_and_process_data(["https://example.com/api"], mock_processor)))
    print(list(fibonacci_generator(100)))
    validator = create_validator({"age": lambda value: isinstance(value, int) and value >= 18})
    assert validator({"age": 20}) == (True, [])
    assert validator({})[0] is False
    print(validator({"age": 15}))
