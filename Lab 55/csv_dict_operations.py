import csv


def read_csv_as_dictionaries(filename):
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            dict_reader = csv.DictReader(csvfile)
            print(f"Reading {filename} as dictionaries...")
            print(f"Fieldnames: {dict_reader.fieldnames}")
            print("-" * 60)
            data_list = []
            for row_num, row_dict in enumerate(dict_reader, 1):
                data_list.append(dict(row_dict))
                print(f"Row {row_num}: {row_dict}")
            return data_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except (OSError, csv.Error) as error:
        print(f"Error reading file: {error}")
        return []


def write_csv_from_dictionaries(filename, data_list, fieldnames):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            dict_writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, extrasaction="ignore"
            )
            dict_writer.writeheader()
            dict_writer.writerows(data_list)
        print(f"Dictionary data successfully written to {filename}")
        return True
    except (OSError, csv.Error) as error:
        print(f"Error writing file: {error}")
        return False


def manipulate_dictionary_data(data_list):
    print("\nDATA MANIPULATION EXAMPLES:")
    print("=" * 60)

    ages = []
    for student in data_list:
        try:
            ages.append(int(student["Age"]))
        except (KeyError, TypeError, ValueError):
            continue

    if ages:
        print(f"Average age of students: {sum(ages) / len(ages):.1f} years")

    subjects = {}
    for student in data_list:
        subject = student.get("Subject", "")
        subjects.setdefault(subject, []).append(student.get("Name", ""))

    print("\nStudents grouped by subject:")
    for subject, students in subjects.items():
        print(f"  {subject}: {', '.join(students)}")

    honor_students = []
    for student in data_list:
        if student.get("Grade") == "A":
            honor_student = student.copy()
            honor_student["Status"] = "Honor Student"
            honor_students.append(honor_student)
    return honor_students


def create_sample_data():
    return [
        {
            "Course_ID": "CS101",
            "Course_Name": "Introduction to Programming",
            "Credits": "3",
            "Instructor": "Dr. Smith",
            "Semester": "Fall 2023",
        },
        {
            "Course_ID": "CS102",
            "Course_Name": "Data Structures",
            "Credits": "4",
            "Instructor": "Dr. Johnson",
            "Semester": "Spring 2024",
        },
        {
            "Course_ID": "MATH201",
            "Course_Name": "Calculus II",
            "Credits": "4",
            "Instructor": "Prof. Davis",
            "Semester": "Fall 2023",
        },
        {
            "Course_ID": "PHYS101",
            "Course_Name": "General Physics",
            "Credits": "3",
            "Instructor": "Dr. Wilson",
            "Semester": "Spring 2024",
        },
    ]


if __name__ == "__main__":
    print("READING EXISTING CSV AS DICTIONARIES:")
    print("=" * 80)
    student_data = read_csv_as_dictionaries("students.csv")

    if student_data:
        honor_students = manipulate_dictionary_data(student_data)
        if honor_students:
            fieldnames = list(honor_students[0].keys())
            write_csv_from_dictionaries("honor_students.csv", honor_students, fieldnames)

    print("\n" + "=" * 80 + "\n")
    print("CREATING NEW CSV FROM DICTIONARY DATA:")
    print("=" * 80)
    course_data = create_sample_data()
    print("Course data to be written:")
    for index, course in enumerate(course_data, 1):
        print(f"{index}. {course}")

    fieldnames = ["Course_ID", "Course_Name", "Credits", "Instructor", "Semester"]
    if write_csv_from_dictionaries("courses.csv", course_data, fieldnames):
        print("\nVerifying written data:")
        print("-" * 40)
        read_csv_as_dictionaries("courses.csv")
