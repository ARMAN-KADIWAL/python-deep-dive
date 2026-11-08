"""Create Pandas DataFrames from dictionaries and lists of lists."""
import pandas as pd


def create_student_dataframe():
    student_data = {
        "Name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Eve Wilson"],
        "Age": [20, 21, 19, 22, 20],
        "Grade": ["A", "B", "A-", "A+", "B+"],
        "Major": ["Computer Science", "Mathematics", "Physics", "Engineering", "Biology"],
        "GPA": [3.8, 3.2, 3.6, 3.9, 3.4],
    }
    return pd.DataFrame(student_data)


def create_product_dataframe():
    product_data = [
        ["Laptop", "Electronics", 999.99, 25],
        ["Smartphone", "Electronics", 699.99, 50],
        ["Desk Chair", "Furniture", 149.99, 15],
        ["Coffee Maker", "Appliances", 79.99, 30],
        ["Notebook", "Stationery", 2.99, 100],
    ]
    columns = ["Product", "Category", "Price", "Stock"]
    return pd.DataFrame(product_data, columns=columns)


def main():
    print("DataFrame created from dictionary:")
    print(create_student_dataframe())
    print("\n" + "=" * 50 + "\n")
    print("DataFrame created from list of lists:")
    print(create_product_dataframe())


if __name__ == "__main__":
    main()
