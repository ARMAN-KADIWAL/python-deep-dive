import csv


def write_basic_csv(filename, data):
    header = ["Product", "Price", "Quantity", "Category"]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(data)
        print(f"Data successfully written to {filename}")
        return True
    except (OSError, csv.Error) as error:
        print(f"Error writing to file: {error}")
        return False


def display_written_file(filename):
    print(f"\nContents of {filename}:")
    print("-" * 40)

    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row_num, row in enumerate(csv_reader):
                if row_num == 0:
                    print(f"Header: {', '.join(row)}")
                    print("-" * 40)
                else:
                    print(f"Row {row_num}: {', '.join(row)}")
    except (OSError, csv.Error) as error:
        print(f"Error reading file: {error}")


product_data = [
    ["Laptop", "999.99", "10", "Electronics"],
    ["Mouse", "25.50", "50", "Electronics"],
    ["Keyboard", "75.00", "30", "Electronics"],
    ["Monitor", "299.99", "15", "Electronics"],
    ["Desk Chair", "150.00", "8", "Furniture"],
]


if __name__ == "__main__":
    filename = "products.csv"
    if write_basic_csv(filename, product_data):
        display_written_file(filename)
