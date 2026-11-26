from abc import ABC, abstractmethod
import time

class NotificationInterface(ABC):
    @abstractmethod
    def send(self, recipient, message, **kwargs):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def log_notification(self, recipient, message, **kwargs):
        return dict(kwargs, type=self.get_type(), recipient=recipient,
                    message=message, timestamp=time.time(), status='sent')

class ConfigurationInterface(ABC):
    @abstractmethod
    def get_config(self):
        pass

    @abstractmethod
    def validate_config(self):
        pass
