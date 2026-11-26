import sys
import traceback


class DataProcessor:
    def generate_report(self):
        return "Report generated"


def process_user_data(user_id, user_info):
    if not isinstance(user_id, int):
        raise TypeError("user_id must be an integer")

    if not isinstance(user_info, dict):
        raise TypeError("user_info must be a dictionary")

    return {"id": user_id, "info": user_info}


examples = [
    (
        "KeyError",
        lambda: {"database": {"host": "localhost"}}["database"]["password"]
    ),
    (
        "AttributeError",
        lambda: DataProcessor().generate_reprot()
    ),
    (
        "TypeError",
        lambda: process_user_data("123", "John Doe")
    ),
    (
        "IndexError",
        lambda: [[1, 2, 3], ["a", "b"]][1][5]
    )
]


if __name__ == "__main__":
    print("Python version:", sys.version)

    for name, example in examples:
        print("\n===", name, "===")

        try:
            example()
        except Exception:
            traceback.print_exc(file=sys.stdout)

    print("\nVersion demonstration completed!")
