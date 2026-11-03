import csv


def write_csv_with_custom_format(
    filename, data, delimiter=",", quoting=csv.QUOTE_MINIMAL
):
    header = ["Employee_ID", "Full_Name", "Department", "Salary", "Join_Date"]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(
                csvfile, delimiter=delimiter, quoting=quoting
            )
            csv_writer.writerow(header)
            csv_writer.writerows(data)
        print(f"Employee data written to {filename} with delimiter {delimiter!r}")
        return True
    except (OSError, csv.Error) as error:
        print(f"Error writing CSV: {error}")
        return False


def append_to_csv(filename, new_data, delimiter=","):
    try:
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter)
            csv_writer.writerows(new_data)
        print(f"New data appended to {filename}")
        return True
    except (OSError, csv.Error) as error:
        print(f"Error appending data: {error}")
        return False


def display_csv(filename, delimiter=","):
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            for row_num, row in enumerate(csv_reader):
                print(f"Row {row_num}: {', '.join(row)}")
    except (OSError, csv.Error) as error:
        print(f"Error reading CSV: {error}")


employee_data = [
    ["E001", "John Doe", "Engineering", "75000", "2023-01-15"],
    ["E002", "Jane Smith", "Marketing", "65000", "2023-02-20"],
    ["E003", "Mike Johnson", "Sales", "55000", "2023-03-10"],
    ["E004", "Sarah Wilson", "HR", "60000", "2023-01-25"],
]

new_employees = [
    ["E005", "Tom Brown", "Engineering", "78000", "2023-04-01"],
    ["E006", "Lisa Davis", "Finance", "70000", "2023-04-15"],
]


if __name__ == "__main__":
    filename = "employees.csv"
    if write_csv_with_custom_format(filename, employee_data):
        append_to_csv(filename, new_employees)
        print(f"\nFinal contents of {filename}:")
        print("=" * 60)
        display_csv(filename)
