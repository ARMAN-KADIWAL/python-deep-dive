# src/advanced_types.py
from typing import (
    TypeVar, Generic, Protocol, runtime_checkable, 
    Union, Optional, Dict, List, Callable, Any,
    NewType, Final, ClassVar
)
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal

# New types for better semantic meaning
UserId = NewType('UserId', int)
ProductCode = NewType('ProductCode', str)
Percentage = NewType('Percentage', float)

# Constants with Final annotation
MAX_PRODUCTS_PER_BATCH: Final[int] = 1000
DEFAULT_TAX_RATE: Final[Percentage] = Percentage(0.08)

class ProcessingStatus(Enum):
    """Enumeration for processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Generic type variables
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')
NumericType = TypeVar('NumericType', int, float, Decimal)

# Protocol for serializable objects
@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can be serialized."""
    def to_dict(self) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable': ...

# Generic repository pattern
class Repository(Generic[T], ABC):
    """Abstract repository with generic type support."""
    
    @abstractmethod
    def save(self, entity: T) -> T: ...
    
    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[T]: ...
    
    @abstractmethod
    def find_all(self) -> List[T]: ...
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...

# Concrete implementation
@dataclass
class ProcessingResult(Generic[T]):
    """Generic result container for processing operations."""
    data: T
    status: ProcessingStatus
    errors: List[str]
    processing_time: float
    
    def is_successful(self) -> bool:
        """Check if processing was successful."""
        return self.status == ProcessingStatus.COMPLETED and not self.errors
    
    def get_error_summary(self) -> str:
        """Get formatted error summary."""
        if not self.errors:
            return "No errors"
        return f"{len(self.errors)} error(s): {'; '.join(self.errors[:3])}"

# Advanced function with multiple type constraints
def aggregate_by_key(
    items: List[T],
    key_func: Callable[[T], K],
    value_func: Callable[[T], NumericType],
    aggregator: Callable[[List[NumericType]], NumericType]
) -> Dict[K, NumericType]:
    """Aggregate items by key with flexible numeric operations."""
    groups: Dict[K, List[NumericType]] = {}
    
    for item in items:
        key = key_func(item)

        groups.setdefault(key, []).append(value_func(item))
    return {key: aggregator(values) for key, values in groups.items()}


class InMemoryRepository(Repository[T]):
    def __init__(self, id_func: Callable[[T], int]) -> None:
        self._entities: Dict[int, T] = {}
        self._id_func = id_func

    def save(self, entity: T) -> T:
        self._entities[self._id_func(entity)] = entity
        return entity

    def find_by_id(self, entity_id: int) -> Optional[T]:
        return self._entities.get(entity_id)

    def find_all(self) -> List[T]:
        return list(self._entities.values())

    def delete(self, entity_id: int) -> bool:
        return self._entities.pop(entity_id, None) is not None


@dataclass
class ProductRecord:
    product_id: int
    product_code: ProductCode
    category: str
    revenue: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {"product_id": self.product_id, "product_code": self.product_code,
                "category": self.category, "revenue": str(self.revenue)}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductRecord":
        return cls(int(data["product_id"]), ProductCode(str(data["product_code"])),
                   str(data["category"]), Decimal(str(data["revenue"])))


def calculate_total(values: List[Decimal]) -> Decimal:
    return sum(values, Decimal("0"))


def process_products(products: List[ProductRecord]) -> ProcessingResult[List[ProductRecord]]:
    import time
    start = time.perf_counter()
    errors: List[str] = []
    processed: List[ProductRecord] = []
    if len(products) > MAX_PRODUCTS_PER_BATCH:
        errors.append("Maximum batch size exceeded")
    else:
        for product in products:
            if product.revenue < 0:
                errors.append(f"Invalid revenue: {product.product_code}")
            else:
                processed.append(product)
    status = ProcessingStatus.FAILED if errors else ProcessingStatus.COMPLETED
    return ProcessingResult(processed, status, errors, time.perf_counter() - start)


if __name__ == "__main__":
    repo = InMemoryRepository[ProductRecord](lambda item: item.product_id)
    repo.save(ProductRecord(1, ProductCode("P1"), "Electronics", Decimal("100")))
    repo.save(ProductRecord(2, ProductCode("P2"), "Electronics", Decimal("200")))
    items = repo.find_all()
    print(aggregate_by_key(items, lambda p: p.category, lambda p: p.revenue, calculate_total))
    assert isinstance(items[0], Serializable)
    assert ProductRecord.from_dict(items[0].to_dict()) == items[0]
    assert process_products(items).is_successful()
    assert repo.delete(1)
    print("Advanced type demonstrations completed")
