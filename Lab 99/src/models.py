# src/models.py
from typing import Dict, List, Optional, Union, Literal
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

# Type aliases for better readability
ProductId = int
CategoryName = str
CurrencyCode = Literal["USD", "EUR", "GBP"]
OutputFormat = Literal["summary", "detailed", "json"]

@dataclass
class Product:
    """Represents a product with comprehensive type annotations."""
    product_id: ProductId
    product_name: str
    category: CategoryName
    price: Decimal
    quantity_sold: int
    sale_date: datetime
    
    def calculate_revenue(self, tax_rate: float = 0.0) -> Decimal:
        """Calculate total revenue including optional tax."""
        base_revenue = self.price * self.quantity_sold
        return base_revenue * (Decimal("1") + Decimal(str(tax_rate)))
    
    def to_dict(self) -> Dict[str, Union[int, str, float, datetime]]:
        """Convert product to dictionary representation."""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'price': float(self.price),
            'quantity_sold': self.quantity_sold,
            'sale_date': self.sale_date
        }

@dataclass
class ProcessingConfig:
    """Configuration for data processing with strict typing."""
    include_tax: bool
    tax_rate: float
    currency: CurrencyCode
    output_format: OutputFormat
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    categories: Optional[List[CategoryName]] = None
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.tax_rate < 0 or self.tax_rate > 1:
            raise ValueError("Tax rate must be between 0 and 1")
        if self.min_price is not None and self.min_price < 0:
            raise ValueError("Minimum price cannot be negative")

@dataclass
class SalesReport:
    """Sales report with typed summary statistics."""
    total_products: int
    total_revenue: Decimal
    average_price: Decimal
    top_category: CategoryName
    products_by_category: Dict[CategoryName, int]
    revenue_by_category: Dict[CategoryName, Decimal]
    processing_timestamp: datetime
    
    def get_category_percentage(self, category: CategoryName) -> float:
        """Get percentage of products in a specific category."""
        if self.total_products == 0:
            return 0.0
        return (self.products_by_category.get(category, 0) / self.total_products) * 100
