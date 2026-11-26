import json
import time
from copy import deepcopy
from threading import Lock
from collections import Counter

class NotificationLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                obj = super().__new__(cls)
                obj._notification_log = []
                obj._log_file = "notification_history.json"
                obj._data_lock = Lock()
                cls._instance = obj
        return cls._instance

    def add_log_entry(self, log_entry):
        with self._data_lock:
            self._notification_log.append(deepcopy(log_entry))

    def get_logs(self, notification_type=None, limit=None):
        with self._data_lock:
            logs = deepcopy(self._notification_log)
        if notification_type:
            logs = [log for log in logs if log['type'] == notification_type.lower()]
        if limit is not None:
            if limit < 0:
                raise ValueError("Limit must be nonnegative")
            logs = logs[-limit:] if limit else []
        return logs

    def get_log_count(self):
        return len(self.get_logs())

    def get_log_summary(self):
        return dict(Counter(log['type'] for log in self.get_logs()))

    def save_logs_to_file(self):
        try:
            with self._data_lock:
                with open(self._log_file, 'w', encoding='utf-8') as f:
                    json.dump(self._notification_log, f, indent=2)
            return True
        except (OSError, TypeError) as e:
            print(f"Error saving logs: {e}")
            return False

    def load_logs_from_file(self):
        try:
            with self._data_lock:
                with open(self._log_file, encoding='utf-8') as f:
                    logs = json.load(f)
                if not isinstance(logs, list) or not all(isinstance(log, dict) for log in logs):
                    raise ValueError("Expected a list of log objects")
                self._notification_log = logs
            return True
        except FileNotFoundError:
            return False
        except (OSError, ValueError) as e:
            print(f"Error loading logs: {e}")
            return False

    def clear_logs(self):
        with self._data_lock:
            self._notification_log.clear()

    def export_logs_by_date_range(self, start_time, end_time):
        return [log for log in self.get_logs()
                if start_time <= log['timestamp'] <= end_time]

def test_singleton_behavior():
    logger1 = NotificationLogger()
    logger2 = NotificationLogger()
    logger3 = NotificationLogger()
    assert logger1 is logger2 is logger3
    logger1.add_log_entry(dict(type='test', recipient='test@example.com',
                               message='Test', timestamp=time.time(), status='sent'))
    assert logger2.get_log_count() == logger3.get_log_count() == 1
    print("Singleton shared state: PASSED")

if __name__ == "__main__":
    test_singleton_behavior()
