import csv
import json


class CSVDictionaryManager:
    def __init__(self):
        self.data = []
        self.fieldnames = []

    def load_from_csv(self, filename):
        try:
            with open(filename, "r", newline="", encoding="utf-8") as csvfile:
                dict_reader = csv.DictReader(csvfile)
                if not dict_reader.fieldnames:
                    raise ValueError("CSV file is empty or has no header.")
                self.fieldnames = list(dict_reader.fieldnames)
                self.data = [dict(row) for row in dict_reader]
            print(f"Loaded {len(self.data)} records from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except (OSError, csv.Error, ValueError) as error:
            print(f"Error loading file: {error}")
            return False

    def save_to_csv(self, filename, data=None):
        records = self.data if data is None else data
        if not records:
            print("No data to save")
            return False
        try:
            fieldnames = self.fieldnames or list(records[0].keys())
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                dict_writer = csv.DictWriter(
                    csvfile, fieldnames=fieldnames, extrasaction="ignore"
                )
                dict_writer.writeheader()
                dict_writer.writerows(records)
            print(f"Saved {len(records)} records to {filename}")
            return True
        except (OSError, csv.Error) as error:
            print(f"Error saving file: {error}")
            return False

    def add_record(self, record_dict):
        record = dict(record_dict)
        if self.fieldnames:
            record = {field: record.get(field, "") for field in self.fieldnames}
        else:
            self.fieldnames = list(record.keys())
        self.data.append(record)
        print(f"Added new record: {record}")

    def update_record(self, search_field, search_value, updates):
        if search_field not in self.fieldnames:
            print(f"Field '{search_field}' not found")
            return 0
        updated_count = 0
        for record in self.data:
            if record.get(search_field) == search_value:
                record.update(updates)
                for field in updates:
                    if field not in self.fieldnames:
                        self.fieldnames.append(field)
                updated_count += 1
        print(f"Updated {updated_count} records")
        return updated_count

    def delete_records(self, search_field, search_value):
        original_count = len(self.data)
        self.data = [
            record for record in self.data
            if record.get(search_field) != search_value
        ]
        deleted_count = original_count - len(self.data)
        print(f"Deleted {deleted_count} records")
        return deleted_count

    def search_records(self, search_criteria):
        results = []
        for record in self.data:
            matches = all(
                str(record.get(field, "")).casefold() == str(value).casefold()
                for field, value in search_criteria.items()
            )
            if matches:
                results.append(record)
        return results

    def generate_report(self):
        if not self.data:
            print("No data available for report")
            return
        print("\nDATA SUMMARY REPORT")
        print("=" * 60)
        print(f"Total Records: {len(self.data)}")
        print(f"Fields: {', '.join(self.fieldnames)}")
        for field in self.fieldnames:
            values = [str(record.get(field, "")) for record in self.data]
            unique_values = set(values)
            print(f"\n{field}:")
            print(f"  Unique values: {len(unique_values)}")
            if len(unique_values) <= 10:
                print(f"  Values: {', '.join(sorted(unique_values))}")

    def export_to_json(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as jsonfile:
                json.dump(self.data, jsonfile, indent=2)
            print(f"Data exported to {filename}")
            return True
        except (OSError, TypeError, ValueError) as error:
            print(f"Error exporting to JSON: {error}")
            return False


def demonstrate_advanced_operations():
    manager = CSVDictionaryManager()

    print("LOADING EXISTING DATA:")
    print("-" * 40)
    if not manager.load_from_csv("students.csv"):
        return
    manager.generate_report()

    print("\nADDING NEW RECORDS:")
    print("-" * 40)
    new_students = [
        {
            "Name": "Alex Thompson",
            "Age": "19",
            "Grade": "B",
            "Subject": "Computer Science",
        },
        {
            "Name": "Maria Garcia",
            "Age": "21",
            "Grade": "A",
            "Subject": "Mathematics",
        },
    ]
    for student in new_students:
        manager.add_record(student)

    print("\nSEARCH OPERATIONS:")
    print("-" * 40)
    grade_a_students = manager.search_records({"Grade": "A"})
    print(f"Found {len(grade_a_students)} Grade A students:")
    for student in grade_a_students:
        print(f"  - {student['Name']} ({student['Subject']})")

    math_students = manager.search_records({"Subject": "Mathematics"})
    print(f"\nFound {len(math_students)} Mathematics students:")
    for student in math_students:
        print(f"  - {student['Name']} (Grade: {student['Grade']})")

    print("\nUPDATE OPERATIONS:")
    print("-" * 40)
    updated = manager.update_record(
        "Subject", "Physics", {"Note": "Lab session required"}
    )
    print(f"Physics records updated: {updated}")

    print("\nDELETE OPERATIONS:")
    print("-" * 40)
    deleted = manager.delete_records("Name", "David Wilson")
    print(f"Records deleted: {deleted}")

    print("\nFINAL REPORT:")
    manager.generate_report()
    manager.save_to_csv("managed_students.csv")
    manager.export_to_json("students_export.json")


if __name__ == "__main__":
    demonstrate_advanced_operations()
