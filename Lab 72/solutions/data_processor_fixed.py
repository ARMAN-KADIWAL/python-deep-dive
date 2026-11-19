"""Resilient data processor with repeatable per-run statistics."""

from pathlib import Path


class DataProcessor:
    def __init__(self):
        self.data = []

    def load_data(self, filename=None):
        if filename is not None:
            self.data = Path(filename).read_text(encoding="utf-8").splitlines()
        else:
            self.data = [
                "100", "200", "invalid", "300", "", "400",
                "500", None, "600", "700", "abc", "800",
            ]
        return len(self.data)

    @staticmethod
    def process_item(item):
        try:
            if item is None or not str(item).strip():
                return None
            return int(item) * 2
        except (TypeError, ValueError):
            return None

    def calculate_statistics(self):
        processed = [self.process_item(item) for item in self.data]
        valid = [value for value in processed if value is not None]
        total = len(self.data)
        return {
            "average": (sum(valid) / len(valid)) if valid else 0,
            "maximum": max(valid) if valid else None,
            "minimum": min(valid) if valid else None,
            "total_processed": len(valid),
            "total_errors": total - len(valid),
            "success_rate": 100 * len(valid) / total if total else 0,
            "processed_data": valid,
        }

    def generate_report(self):
        result = self.calculate_statistics()
        for key, value in result.items():
            print(f"{key}: {value}")
        return result


if __name__ == "__main__":
    processor = DataProcessor()
    processor.load_data()
    processor.generate_report()
