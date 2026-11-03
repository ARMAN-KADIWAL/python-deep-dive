import csv


class CSVFilter:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.header = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r", newline="", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                self.header = next(csv_reader, [])
                self.data = list(csv_reader)
            print(f"Loaded {len(self.data)} rows from {self.filename}")
            return True
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
            return False
        except (OSError, csv.Error) as error:
            print(f"Error loading data: {error}")
            return False

    def _compare(self, cell_value, operator, value):
        if operator == "=":
            return cell_value == value
        if operator == "!=":
            return cell_value != value
        if operator in {">", "<", ">=", "<="}:
            try:
                left, right = float(cell_value), float(value)
            except ValueError:
                left, right = cell_value, value
            if operator == ">":
                return left > right
            if operator == "<":
                return left < right
            if operator == ">=":
                return left >= right
            return left <= right
        if operator == "contains":
            return value.casefold() in cell_value.casefold()
        raise ValueError(f"Unsupported operator: {operator}")

    def filter_by_condition(self, column, operator, value):
        if column not in self.header:
            print(f"Column '{column}' not found.")
            return []

        column_index = self.header.index(column)
        filtered_data = []
        for row in self.data:
            if len(row) <= column_index:
                continue
            if self._compare(row[column_index], operator, str(value)):
                filtered_data.append(row)
        return filtered_data

    def save_filtered_data(self, filtered_data, output_filename):
        try:
            with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(self.header)
                csv_writer.writerows(filtered_data)
            print(f"Filtered data saved to {output_filename}")
            return True
        except (OSError, csv.Error) as error:
            print(f"Error saving data: {error}")
            return False

    def display_data(self, data, title="Data"):
        print(f"\n{title}")
        print("=" * 80)
        if not data:
            print("No data to display")
            return
        print(f"{'#':<3} {' | '.join(f'{col:<12}' for col in self.header)}")
        print("-" * 80)
        for index, row in enumerate(data, 1):
            formatted_row = " | ".join(f"{cell:<12}" for cell in row)
            print(f"{index:<3} {formatted_row}")


def demonstrate_advanced_filtering():
    csv_filter = CSVFilter("students.csv")

    print("DEMONSTRATION 1: Students older than 19")
    older_students = csv_filter.filter_by_condition("Age", ">", "19")
    csv_filter.display_data(older_students, "Students Age > 19")
    csv_filter.save_filtered_data(older_students, "older_students.csv")

    print("\n" + "=" * 100 + "\n")
    print("DEMONSTRATION 2: Students with Grade A")
    grade_a_students = csv_filter.filter_by_condition("Grade", "=", "A")
    csv_filter.display_data(grade_a_students, "Grade A Students")

    print("\n" + "=" * 100 + "\n")
    print("DEMONSTRATION 3: Students with 'o' in their name")
    name_filter = csv_filter.filter_by_condition("Name", "contains", "o")
    csv_filter.display_data(name_filter, "Names containing 'o'")


if __name__ == "__main__":
    demonstrate_advanced_filtering()
