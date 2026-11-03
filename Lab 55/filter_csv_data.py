import csv


def filter_csv_data(input_file, output_file, filter_column, filter_value):
    try:
        with open(input_file, "r", newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader, None)

            if header is None:
                print("Input CSV is empty.")
                return [], []

            if filter_column not in header:
                print(f"Error: Column '{filter_column}' not found in CSV file.")
                return [], header

            filter_index = header.index(filter_column)
            filtered_rows = [
                row for row in csv_reader
                if len(row) > filter_index and row[filter_index] == filter_value
            ]

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(filtered_rows)

        print(f"Filtered data written to {output_file}")
        print(
            f"Found {len(filtered_rows)} rows matching "
            f"{filter_value!r} in column {filter_column!r}"
        )
        return filtered_rows, header

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return [], []
    except (OSError, csv.Error) as error:
        print(f"Error: {error}")
        return [], []


def display_filtered_results(filtered_rows, header, filter_info):
    print(f"\nFiltered Results: {filter_info}")
    print("=" * 60)

    if not filtered_rows:
        print("No matching records found.")
        return

    print(f"{'Index':<5} {' | '.join(header)}")
    print("-" * 60)
    for index, row in enumerate(filtered_rows, 1):
        print(f"{index:<5} {' | '.join(row)}")


def advanced_filter_demo():
    input_file = "students.csv"

    print("FILTER 1: Students with Grade 'A'")
    filtered_rows, header = filter_csv_data(
        input_file, "grade_a_students.csv", "Grade", "A"
    )
    display_filtered_results(filtered_rows, header, "Grade = A")

    print("\n" + "=" * 80 + "\n")

    print("FILTER 2: Students studying Mathematics")
    filtered_rows, header = filter_csv_data(
        input_file, "math_students.csv", "Subject", "Mathematics"
    )
    display_filtered_results(filtered_rows, header, "Subject = Mathematics")


if __name__ == "__main__":
    advanced_filter_demo()
