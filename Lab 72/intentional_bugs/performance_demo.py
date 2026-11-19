import time

def inefficient_search(data, target):
    """Inefficient search with debugging points"""
    print(f"Searching for {target} in {len(data)} items")
    
    found_indices = []
    
    # Bug: Inefficient nested loops
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j and data[i] == target:
                found_indices.append(i)
                print(f"Found {target} at index {i}")
    
    return found_indices

def generate_large_dataset(size):
    """Generate test data"""
    import random
    data = []
    for i in range(size):
        data.append(random.randint(1, 100))
    return data

def main():
    print("=== Performance Debugging Demo ===")
    
    # Generate test data
    data_size = 1000
    test_data = generate_large_dataset(data_size)
    target_value = 50
    
    start_time = time.time()
    results = inefficient_search(test_data, target_value)
    end_time = time.time()
    
    print(f"Search completed in {end_time - start_time:.4f} seconds")
    print(f"Found {len(results)} occurrences")

if __name__ == "__main__":
    main()
