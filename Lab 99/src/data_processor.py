# src/data_processor.py
from typing import Dict, List, Optional, Union, Callable
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import statistics

from .models import Product, ProcessingConfig, SalesReport, ProductId, CategoryName
from .utils import (
    load_csv_data, load_typed_json, parse_numeric_value, 
    group_by_key, safe_divide, SalesDataRow, ConfigData
)

class SalesDataProcessor:
    """Main data processor with comprehensive type safety."""
    
    def __init__(self, config: ProcessingConfig) -> None:
        self.config = config
        self._products: List[Product] = []
        self._processing_errors: List[str] = []
    
    def load_data_from_csv(self, csv_path: Path) -> None:
        """Load and parse CSV data into Product objects."""
        try:
            raw_data = load_csv_data(csv_path)
            self._products = self._convert_raw_data_to_products(raw_data)
            print(f"Successfully loaded {len(self._products)} products")
        except Exception as e:
            error_msg = f"Error loading CSV data: {e}"
            self._processing_errors.append(error_msg)
            raise ValueError(error_msg)
    
    def _convert_raw_data_to_products(self, raw_data: List[SalesDataRow]) -> List[Product]:
        """Convert raw CSV data to typed Product objects."""
        products: List[Product] = []
        
        for row_index, row in enumerate(raw_data):
            try:
                product = Product(
                    product_id=int(row['product_id']),
                    product_name=row['product_name'],
                    category=row['category'],
                    price=Decimal(row['price']),
                    quantity_sold=int(row['quantity_sold']),
                    sale_date=datetime.strptime(row['sale_date'], '%Y-%m-%d')
                )
                
                # Apply filters if configured
                if self._should_include_product(product):
                    products.append(product)
                    
            except (ValueError, KeyError) as e:
                error_msg = f"Error processing row {row_index + 1}: {e}"
                self._processing_errors.append(error_msg)
                continue
        
        return products
    
    def _should_include_product(self, product: Product) -> bool:
        """Check if product meets filter criteria."""
        # Price range filter
        if self.config.min_price is not None and float(product.price) < self.config.min_price:
            return False
        if self.config.max_price is not None and float(product.price) > self.config.max_price:
            return False
        
        # Category filter
        if self.config.categories is not None and product.category not in self.config.categories:
            return False
        
        return True
    
    def calculate_statistics(self) -> SalesReport:
        """Calculate comprehensive sales statistics."""
        if not self._products:
            raise ValueError("No products loaded for analysis")
        
        # Basic statistics
        total_products = len(self._products)
        tax_rate = self.config.tax_rate if self.config.include_tax else 0.0
        total_revenue: Decimal = sum(
            (product.calculate_revenue(tax_rate) for product in self._products),
            Decimal("0"),
        )
        prices = [product.price for product in self._products]
        average_price: Decimal = sum(prices, Decimal("0")) / len(prices) if prices else Decimal("0")
        
        # Group by category
        products_by_category = self._group_products_by_category()
        revenue_by_category = self._calculate_revenue_by_category()
        
        # Find top category
        top_category = max(products_by_category.keys(), 
                          key=lambda cat: products_by_category[cat])
        
        return SalesReport(
            total_products=total_products,
            total_revenue=total_revenue,
            average_price=average_price,
            top_category=top_category,
            products_by_category=products_by_category,
            revenue_by_category=revenue_by_category,
            processing_timestamp=datetime.now()
        )
    
    def _group_products_by_category(self) -> Dict[CategoryName, int]:
        """Group products by category and count them."""
        category_groups = group_by_key(self._products, lambda p: p.category)
        return {category: len(products) for category, products in category_groups.items()}
    
    def _calculate_revenue_by_category(self) -> Dict[CategoryName, Decimal]:
        """Calculate total revenue by category."""
        revenue_by_category: Dict[CategoryName, Decimal] = {}
        
        for product in self._products:
            category = product.category
            revenue = product.calculate_revenue(
                self.config.tax_rate if self.config.include_tax else 0.0
            )
            
            if category not in revenue_by_category:
                revenue_by_category[category] = Decimal('0')
            revenue_by_category[category] += revenue
        
        return revenue_by_category
    
    def get_top_products(self, n: int = 5) -> List[Product]:
        """Get top N products by revenue."""
        if n <= 0:
            raise ValueError("Number of products must be positive")
        
        sorted_products = sorted(
            self._products,
            key=lambda p: p.calculate_revenue(
                self.config.tax_rate if self.config.include_tax else 0.0
            ),
            reverse=True
        )
        
        return sorted_products[:n]
    
    def filter_products_by_criteria(
        self, 
        filter_func: Callable[[Product], bool]
    ) -> List[Product]:
        """Filter products using a custom function."""
        return [product for product in self._products if filter_func(product)]
    
    def get_processing_errors(self) -> List[str]:
        """Get list of processing errors encountered."""
        return self._processing_errors.copy()
    
    def export_report(self, report: SalesReport, output_path: Path) -> None:
        """Export sales report to file."""
        try:
            with open(output_path, 'w') as f:
                f.write(f"Sales Report - Generated: {report.processing_timestamp}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Total Products: {report.total_products}\n")
                f.write(f"Total Revenue: ${report.total_revenue:.2f}\n")
                f.write(f"Average Price: ${report.average_price:.2f}\n")
                f.write(f"Top Category: {report.top_category}\n\n")
                
                f.write("Products by Category:\n")
                for category, count in report.products_by_category.items():
                    percentage = report.get_category_percentage(category)
                    f.write(f"  {category}: {count} ({percentage:.1f}%)\n")
                
                f.write("\nRevenue by Category:\n")
                for category, revenue in report.revenue_by_category.items():
                    f.write(f"  {category}: ${revenue:.2f}\n")
                    
        except IOError as e:
            raise ValueError(f"Error writing report to {output_path}: {e}")

def create_processor_from_config_file(config_path: Path) -> SalesDataProcessor:
    """Create a processor after validating JSON fields."""
    from typing import cast
    from .models import CurrencyCode, OutputFormat

    def optional_price(value: object) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Price must be numeric")
        return float(value)

    def optional_categories(value: object) -> Optional[List[str]]:
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("Categories must be a list")
        result: List[str] = []
        for category in value:
            if not isinstance(category, str):
                raise ValueError("Category must be text")
            result.append(category)
        return result

    data = load_typed_json(config_path)
    options, filters = data["processing_options"], data["filters"]
    include_tax = options["include_tax"]
    tax_rate = options["tax_rate"]
    currency = options["currency"]
    output_format = options["output_format"]
    if not isinstance(include_tax, bool):
        raise ValueError("include_tax must be boolean")
    if isinstance(tax_rate, bool) or not isinstance(tax_rate, (int, float)):
        raise ValueError("tax_rate must be numeric")
    if currency not in ("USD", "EUR", "GBP"):
        raise ValueError("Invalid currency")
    if output_format not in ("summary", "detailed", "json"):
        raise ValueError("Invalid output format")
    return SalesDataProcessor(ProcessingConfig(
        include_tax=include_tax, tax_rate=float(tax_rate),
        currency=cast(CurrencyCode, currency),
        output_format=cast(OutputFormat, output_format),
        min_price=optional_price(filters.get("min_price")),
        max_price=optional_price(filters.get("max_price")),
        categories=optional_categories(filters.get("categories")),
    ))
