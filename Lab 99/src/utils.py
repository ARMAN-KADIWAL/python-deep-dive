# src/utils.py
from typing import (
    Dict, List, Optional, Union, Callable, TypeVar, Generic,
    Protocol, runtime_checkable, overload, Any, TypedDict
)
from collections.abc import Iterable, Mapping
from datetime import datetime
from typing import cast
import json
import csv
from decimal import Decimal
from pathlib import Path

# Python 3.13 enhanced typing features
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# TypedDict for structured dictionaries (Python 3.13 enhanced)
class SalesDataRow(TypedDict):
    product_id: str
    product_name: str
    category: str
    price: str
    quantity_sold: str
    sale_date: str

class ConfigData(TypedDict):
    processing_options: Dict[str, Union[bool, float, str]]
    filters: Dict[str, Union[float, List[str]]]

# Protocol for type-safe data validation
@runtime_checkable
class Validator(Protocol):
    """Protocol for data validation functions."""
    def validate(self, data: Any) -> bool: ...
    def get_error_message(self) -> str: ...

class DataProcessor(Generic[T]):
    """Generic data processor with type safety."""
    
    def __init__(self, validator: Optional[Validator] = None) -> None:
        self._validator = validator
        self._processed_items: List[T] = []
    
    def process_batch(self, items: Iterable[T]) -> List[T]:
        """Process a batch of items with type safety."""
        processed: List[T] = []
        for item in items:
            if self._validator is None or self._validator.validate(item):
                processed.append(item)
            else:
                print(f"Validation failed: {self._validator.get_error_message()}")
        self._processed_items.extend(processed)
        return processed
    
    def get_processed_count(self) -> int:
        """Get count of processed items."""
        return len(self._processed_items)

# Overloaded functions for different input types
@overload
def parse_numeric_value(value: str) -> Union[int, float]: ...

@overload
def parse_numeric_value(value: Union[int, float]) -> Union[int, float]: ...

def parse_numeric_value(value: Union[str, int, float]) -> Union[int, float]:
    """Parse numeric value with proper type handling."""
    if isinstance(value, str):
        try:
            # Try integer first
            if '.' not in value:
                return int(value)
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot parse '{value}' as numeric")
    return value

def load_typed_json(file_path: Path) -> ConfigData:
    """Load JSON with strict typing validation."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Validate structure matches TypedDict
            if not isinstance(data, dict):
                raise TypeError("JSON root must be an object")
            if 'processing_options' not in data or 'filters' not in data:
                raise KeyError("Missing required keys in configuration")
            return cast(ConfigData, data)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise ValueError(f"Error loading configuration: {e}")

def load_csv_data(file_path: Path) -> List[SalesDataRow]:
    """Load CSV data with typed dictionary structure."""
    rows: List[SalesDataRow] = []
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Ensure all required fields are present
                typed_row: SalesDataRow = {
                    'product_id': row.get('product_id', ''),
                    'product_name': row.get('product_name', ''),
                    'category': row.get('category', ''),
                    'price': row.get('price', '0'),
                    'quantity_sold': row.get('quantity_sold', '0'),
                    'sale_date': row.get('sale_date', '')
                }
                rows.append(typed_row)
    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {file_path}")
    return rows

# Advanced type manipulation functions
def group_by_key(items: List[T], key_func: Callable[[T], K]) -> Dict[K, List[T]]:
    """Group items by a key function with proper typing."""
    groups: Dict[K, List[T]] = {}
    for item in items:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def safe_divide(numerator: Union[int, float, Decimal], 
                denominator: Union[int, float, Decimal]) -> Optional[Decimal]:
    """Safely divide two numbers, returning None if division by zero."""
    if denominator == 0:
        return None
    return Decimal(str(numerator)) / Decimal(str(denominator))
