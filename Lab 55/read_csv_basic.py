import csv


def read_csv_file(filename):
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader, None)

            if header is None:
                print("CSV file is empty.")
                return

            print("CSV File Contents:")
            print("-" * 50)
            print(f"Header: {', '.join(header)}")
            print("-" * 50)

            row_count = 0
            for row in csv_reader:
                row_count += 1
                print(f"Row {row_count}: {', '.join(row)}")

            print(f"\nTotal rows (excluding header): {row_count}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except (OSError, csv.Error) as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    read_csv_file("students.csv")
