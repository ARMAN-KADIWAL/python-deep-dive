import csv
import json
import os
import tempfile
import unittest

from write_csv_basic import write_basic_csv
from write_csv_advanced import write_csv_with_custom_format, append_to_csv
from filter_csv_data import filter_csv_data
from advanced_filter import CSVFilter
from csv_dict_operations import read_csv_as_dictionaries, write_csv_from_dictionaries, manipulate_dictionary_data
from advanced_dict_csv import CSVDictionaryManager


class CSVLabTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.students_file = os.path.join(self.temp_dir.name, "students.csv")
        with open(self.students_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Grade", "Subject"])
            writer.writerows([
                ["Alice", "20", "A", "Math"],
                ["Bob", "19", "B", "Physics"],
                ["Carol", "21", "A", "Chemistry"],
            ])

    def test_basic_csv_write(self):
        output = os.path.join(self.temp_dir.name, "products.csv")
        self.assertTrue(write_basic_csv(output, [["Laptop", "999", "2", "Tech"]]))
        with open(output, newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
        self.assertEqual(rows[0], ["Product", "Price", "Quantity", "Category"])
        self.assertEqual(rows[1][0], "Laptop")

    def test_advanced_csv_write_and_append(self):
        output = os.path.join(self.temp_dir.name, "employees.csv")
        self.assertTrue(write_csv_with_custom_format(
            output, [["E1", "Alice", "Engineering", "70000", "2024-01-01"]]
        ))
        self.assertTrue(append_to_csv(
            output, [["E2", "Bob", "Sales", "50000", "2024-02-01"]]
        ))
        with open(output, newline="", encoding="utf-8") as file:
            self.assertEqual(len(list(csv.reader(file))), 3)

    def test_basic_filter(self):
        output = os.path.join(self.temp_dir.name, "grade_a.csv")
        rows, header = filter_csv_data(self.students_file, output, "Grade", "A")
        self.assertEqual(len(rows), 2)
        self.assertEqual(header[0], "Name")
        with open(output, newline="", encoding="utf-8") as file:
            self.assertEqual(len(list(csv.reader(file))), 3)

    def test_advanced_filter_numeric_and_contains(self):
        csv_filter = CSVFilter(self.students_file)
        self.assertEqual(len(csv_filter.filter_by_condition("Age", ">", "19")), 2)
        self.assertEqual(len(csv_filter.filter_by_condition("Name", "contains", "o")), 2)
        self.assertEqual(len(csv_filter.filter_by_condition("Grade", "!=", "A")), 1)

    def test_dictionary_read_write_and_honor_students(self):
        data = read_csv_as_dictionaries(self.students_file)
        self.assertEqual(len(data), 3)
        honor = manipulate_dictionary_data(data)
        self.assertEqual(len(honor), 2)
        output = os.path.join(self.temp_dir.name, "honor.csv")
        fields = list(honor[0].keys())
        self.assertTrue(write_csv_from_dictionaries(output, honor, fields))
        reread = read_csv_as_dictionaries(output)
        self.assertEqual(reread[0]["Status"], "Honor Student")

    def test_dictionary_manager_crud_and_json(self):
        manager = CSVDictionaryManager()
        self.assertTrue(manager.load_from_csv(self.students_file))
        self.assertEqual(len(manager.search_records({"Grade": "A"})), 2)
        self.assertEqual(manager.update_record("Subject", "Physics", {"Note": "Review"}), 1)
        self.assertEqual(manager.delete_records("Name", "Bob"), 1)
        output = os.path.join(self.temp_dir.name, "managed.csv")
        json_output = os.path.join(self.temp_dir.name, "managed.json")
        self.assertTrue(manager.save_to_csv(output))
        self.assertTrue(manager.export_to_json(json_output))
        with open(json_output, encoding="utf-8") as file:
            exported = json.load(file)
        self.assertEqual(len(exported), 2)
        self.assertEqual(exported[0]["Note"], "Review")


if __name__ == "__main__":
    unittest.main(verbosity=2)
