import json
import os
from copy import deepcopy
from threading import Lock

class ConfigurationManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                obj = super().__new__(cls)
                obj._config_file = "app_config.json"
                obj._load_default_config()
                cls._instance = obj
        return cls._instance

    def _load_default_config(self):
        self._config = {
            'email': {'smtp_server': 'smtp.example.com', 'port': 587,
                      'username': 'system@example.com', 'password': 'DEMO_ONLY',
                      'timeout': 30},
            'sms': {'api_key': 'DEMO_ONLY', 'sender_id': 'NOTIFY',
                    'base_url': 'https://api.sms.com', 'timeout': 15},
            'push': {'app_id': 'push_app_123', 'api_key': 'DEMO_ONLY',
                     'server_url': 'https://push.example.com', 'timeout': 10},
            'logging': {'level': 'INFO', 'max_log_entries': 1000, 'auto_save': True},
            'general': {'retry_attempts': 3, 'retry_delay': 1, 'debug_mode': False}
        }

    def get_config(self, section=None, key=None):
        if section is None:
            return deepcopy(self._config)
        if key is None:
            return deepcopy(self._config[section])
        return deepcopy(self._config[section][key])

    def set_config(self, section, key, value):
        self._config.setdefault(section, {})[key] = value

    def update_section(self, section, config_dict):
        self._config.setdefault(section, {}).update(config_dict)

    def save_config(self):
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            return True
        except OSError as e:
            print(f"Error saving configuration: {e}")
            return False

    def load_config(self):
        if not os.path.exists(self._config_file):
            return False
        try:
            with open(self._config_file, encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict) or not all(isinstance(v, dict) for v in data.values()):
                raise ValueError("Expected configuration sections")
            for section, values in data.items():
                self.update_section(section, values)
            return True
        except (OSError, ValueError) as e:
            print(f"Error loading configuration: {e}")
            return False

    def reset_to_defaults(self):
        self._load_default_config()

    def get_all_sections(self):
        return list(self._config)

    def validate_config(self):
        return all(isinstance(self._config.get(section), dict)
                   for section in ('email', 'sms', 'push', 'logging', 'general'))
