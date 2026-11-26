import time
from notification_interfaces import NotificationInterface
from notification_implementations import EmailNotification, SMSNotification, PushNotification

class NotificationFactory:
    _notification_types = {
        'email': EmailNotification, 'sms': SMSNotification, 'push': PushNotification
    }

    @classmethod
    def create_notification(cls, notification_type):
        notification_type = notification_type.lower()
        if notification_type not in cls._notification_types:
            available = ', '.join(cls._notification_types)
            raise ValueError(f"Unknown notification type: {notification_type}. Available types: {available}")
        return cls._notification_types[notification_type]()

    @classmethod
    def get_available_types(cls):
        return list(cls._notification_types)

    @classmethod
    def register_notification_type(cls, type_name, notification_class):
        if not isinstance(notification_class, type) or not issubclass(notification_class, NotificationInterface):
            raise TypeError("Notification class must implement NotificationInterface")
        cls._notification_types[type_name.lower()] = notification_class

class SlackNotification(NotificationInterface):
    def send(self, recipient, message, **kwargs):
        channel = kwargs.get('channel', '#general')
        print(f"Simulating Slack message to {channel}: {recipient}: {message}")
        time.sleep(0.2)
        return self.log_notification(recipient, message, channel=channel)

    def get_type(self):
        return 'slack'

NotificationFactory.register_notification_type('slack', SlackNotification)
