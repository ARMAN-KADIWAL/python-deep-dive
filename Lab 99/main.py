# main.py
from typing import Optional
from pathlib import Path
import sys
import argparse

from src.data_processor import SalesDataProcessor, create_processor_from_config_file
from src.models import ProcessingConfig

def main() -> int:
    """Main application entry point with proper return type."""
    parser = argparse.ArgumentParser(description='Sales Data Processing Application')
    parser.add_argument('--config', type=str, default='data/config.json',
                       help='Path to configuration file')
    parser.add_argument('--data', type=str, default='data/sales_data.csv',
                       help='Path to sales data CSV file')
    parser.add_argument('--output', type=str, default='sales_report.txt',
                       help='Output file for the report')
    
    args = parser.parse_args()
    
    try:
        # Create processor from configuration
        config_path = Path(args.config)
        data_path = Path(args.data)
        output_path = Path(args.output)
        
        print("Initializing sales data processor...")
        processor = create_processor_from_config_file(config_path)
        
        print(f"Loading data from {data_path}...")
        processor.load_data_from_csv(data_path)
        
        # Check for processing errors
        errors = processor.get_processing_errors()
        if errors:
            print("Processing errors encountered:")
            for error in errors:
                print(f"  - {error}")
        
        print("Calculating statistics...")
        report = processor.calculate_statistics()
        
        print("Generating report...")
        processor.export_report(report, output_path)
        
        # Display summary
        print("\n" + "="*50)
        print("SALES ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total Products Analyzed: {report.total_products}")
        print(f"Total Revenue: ${report.total_revenue:.2f}")
        print(f"Average Product Price: ${report.average_price:.2f}")
        print(f"Top Category: {report.top_category}")
        print(f"Report saved to: {output_path}")
        
        # Show top products
        print("\nTop 3 Products by Revenue:")
        top_products = processor.get_top_products(3)
        for i, product in enumerate(top_products, 1):
            revenue = product.calculate_revenue(
                processor.config.tax_rate if processor.config.include_tax else 0.0
            )
            print(f"  {i}. {product.product_name}: ${revenue:.2f}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
