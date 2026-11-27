# tests/test_data_processor.py
from typing import List, Dict
import unittest
from decimal import Decimal
from datetime import datetime
from pathlib import Path
import tempfile
import os

from src.models import Product, ProcessingConfig, SalesReport
from src.data_processor import SalesDataProcessor
from src.utils import parse_numeric_value, safe_divide

class TestDataProcessor(unittest.TestCase):
    """Test suite for data processor with type safety."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = ProcessingConfig(
            include_tax=True,
            tax_rate=0.08,
            currency="USD",
            output_format="summary"
        )
        self.processor = SalesDataProcessor(self.config)
        
        # Create sample products
        self.sample_products: List[Product] = [
            Product(
                product_id=1,
                product_name="Test Laptop",
                category="Electronics",
                price=Decimal("999.99"),
                quantity_sold=10,
                sale_date=datetime(2024, 1, 15)
            ),
            Product(
                product_id=2,
                product_name="Test Chair",
                category="Furniture",
                price=Decimal("199.99"),
                quantity_sold=5,
                sale_date=datetime(2024, 1, 16)
            )
        ]
    
    def test_product_revenue_calculation(self) -> None:
        """Test product revenue calculation with tax."""
        product = self.sample_products[0]
        expected_revenue = Decimal("999.99") * 10 * Decimal("1.08")
        actual_revenue = product.calculate_revenue(0.08)
        self.assertEqual(actual_revenue, expected_revenue)
    
    def test_safe_divide_function(self) -> None:
        """Test safe division utility function."""
        result = safe_divide(10, 2)
        self.assertEqual(result, Decimal("5"))
        
        # Test division by zero
        result = safe_divide(10, 0)
        self.assertIsNone(result)
    
    def test_parse_numeric_value(self) -> None:
        """Test numeric value parsing with different types."""
        # Test string to int
        result = parse_numeric_value("42")
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)
        
        # Test string to float
        result = parse_numeric_value("42.5")
        self.assertEqual(result, 42.5)
        self.assertIsInstance(result, float)
        
        # Test passthrough
        result = parse_numeric_value(100)
        self.assertEqual(result, 100)
    
    def test_processing_config_validation(self) -> None:
        """Test configuration validation."""
        # Valid configuration
        config = ProcessingConfig(
            include_tax=True,
            tax_rate=0.1,
            currency="USD",
            output_format="summary"
        )
        self.assertEqual(config.tax_rate, 0.1)
        
        # Invalid tax rate
        with self.assertRaises(ValueError):
            ProcessingConfig(
                include_tax=True,
                tax_rate=1.5,  # Invalid: > 1
                currency="USD",
                output_format="summary"
            )
    
    def test_report_generation(self) -> None:
        """Test sales report generation."""
        # Manually add products to processor
        self.processor._products = self.sample_products
        
        report = self.processor.calculate_statistics()
        
        self.assertIsInstance(report, SalesReport)
        self.assertEqual(report.total_products, 2)
        self.assertGreater(report.total_revenue, Decimal("0"))
        self.assertIn(report.top_category, ["Electronics", "Furniture"])
    
    def test_top_products_retrieval(self) -> None:
        """Test top products functionality."""
        self.processor._products = self.sample_products
        
        top_products = self.processor.get_top_products(1)
        self.assertEqual(len(top_products), 1)
        self.assertIsInstance(top_products[0], Product)
        
        # Test invalid input
        with self.assertRaises(ValueError):
            self.processor.get_top_products(0)

def run_tests() -> None:
    """Run all tests with proper type annotations."""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests()
