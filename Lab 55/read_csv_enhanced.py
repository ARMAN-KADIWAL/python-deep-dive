import csv


def read_csv_with_column_access(filename):
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader, None)

            if header is None:
                print("CSV file is empty.")
                return

            required = ["Name", "Age", "Grade", "Subject"]
            indexes = {}

            for column in required:
                if column not in header:
                    raise ValueError(f"Required column '{column}' not found.")
                indexes[column] = header.index(column)

            print("Enhanced CSV Reader")
            print("=" * 60)
            print("Student Information Summary:")
            print("-" * 40)

            for row_num, row in enumerate(csv_reader, 1):
                if len(row) < len(header):
                    print(f"Skipping malformed row {row_num}: {row}")
                    continue
                name = row[indexes["Name"]]
                age = row[indexes["Age"]]
                grade = row[indexes["Grade"]]
                subject = row[indexes["Subject"]]
                print(f"{row_num}. {name} (Age: {age}) - Grade: {grade} in {subject}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except (OSError, csv.Error, ValueError) as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    read_csv_with_column_access("students.csv")
