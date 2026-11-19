class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed_count = 0
        self.error_count = 0
    
    def load_data(self, filename=None):
        """Load data from various sources"""
        if filename:
            try:
                with open(filename, 'r') as file:
                    # Bug: Not handling file format properly
                    self.data = file.read().split('\n')
            except FileNotFoundError:
                print(f"File {filename} not found")
                # Bug: Should return or handle this case
                pass
        else:
            # Generate sample data with intentional issues
            self.data = [
                "100", "200", "invalid", "300", "", "400",
                "500", None, "600", "700", "abc", "800"
            ]
    
    def process_item(self, item):
        """Process individual data item"""
        print(f"Processing item: {item}")
        
        if item is None:
            # Bug: This will cause issues downstream
            return item * 2
        
        if isinstance(item, str) and item.strip() == "":
            # Bug: Should handle empty strings
            return int(item)
        
        try:
            # Convert to number and double it
            number = int(item)
            result = number * 2
            self.processed_count += 1
            return result
        except (ValueError, TypeError) as e:
            print(f"Error processing {item}: {e}")
            self.error_count += 1
            # Bug: Returning None without proper handling
            return None
    
    def calculate_statistics(self):
        """Calculate statistics from processed data"""
        processed_data = []
        
        for item in self.data:
            result = self.process_item(item)
            if result is not None:
                processed_data.append(result)
        
        if not processed_data:
            print("No valid data to process")
            return None
        
        # Bug: Division by zero potential
        average = sum(processed_data) / len(processed_data)
        maximum = max(processed_data)
        minimum = min(processed_data)
        
        # Bug: This might cause issues with None values
        total_items = len(self.data)
        success_rate = (self.processed_count / total_items) * 100
        
        return {
            'average': average,
            'maximum': maximum,
            'minimum': minimum,
            'total_processed': self.processed_count,
            'total_errors': self.error_count,
            'success_rate': success_rate,
            'processed_data': processed_data
        }
    
    def generate_report(self):
        """Generate processing report"""
        print("=== Data Processing Report ===")
        
        stats = self.calculate_statistics()
        
        if stats:
            print(f"Total items processed: {stats['total_processed']}")
            print(f"Total errors: {stats['total_errors']}")
            print(f"Success rate: {stats['success_rate']:.2f}%")
            print(f"Average value: {stats['average']:.2f}")
            print(f"Maximum value: {stats['maximum']}")
            print(f"Minimum value: {stats['minimum']}")
            print(f"Processed data: {stats['processed_data']}")
        else:
            print("No statistics available")

def main():
    print("=== Complex Data Processing Demo ===")
    
    processor = DataProcessor()
    
    # Load sample data
    processor.load_data()
    
    print(f"Loaded {len(processor.data)} items")
    print("Starting processing...")
    
    # Generate report
    processor.generate_report()

if __name__ == "__main__":
    main()
