import time
from notification_interfaces import NotificationInterface, ConfigurationInterface
from configuration_manager import ConfigurationManager

class BaseConfiguration(ConfigurationInterface):
    def get_config(self):
        return ConfigurationManager().get_config(self.section)

    def validate_config(self):
        config = self.get_config()
        return all(key in config for key in self.required_keys)

class EmailConfiguration(BaseConfiguration):
    section = 'email'
    required_keys = ('smtp_server', 'port', 'username', 'password')

class SMSConfiguration(BaseConfiguration):
    section = 'sms'
    required_keys = ('api_key', 'sender_id', 'base_url')

class PushConfiguration(BaseConfiguration):
    section = 'push'
    required_keys = ('app_id', 'api_key', 'server_url')

class EmailNotification(NotificationInterface):
    def __init__(self):
        self.config = EmailConfiguration()
        if not self.config.validate_config():
            raise ValueError("Invalid email configuration")

    def send(self, recipient, message, **kwargs):
        subject = kwargs.get('subject', 'Notification')
        config = self.config.get_config()
        print(f"Connecting to SMTP server: {config['smtp_server']}")
        print(f"Sending email to: {recipient}; Subject: {subject}; Message: {message}")
        time.sleep(1)
        print("Email simulated successfully!")
        return self.log_notification(recipient, message, subject=subject)

    def get_type(self):
        return 'email'

class SMSNotification(NotificationInterface):
    def __init__(self):
        self.config = SMSConfiguration()
        if not self.config.validate_config():
            raise ValueError("Invalid SMS configuration")

    def send(self, recipient, message, **kwargs):
        config = self.config.get_config()
        print(f"Connecting to SMS API: {config['base_url']}")
        print(f"Sending SMS to: {recipient}; Message: {message}")
        time.sleep(0.5)
        print("SMS simulated successfully!")
        return self.log_notification(recipient, message)

    def get_type(self):
        return 'sms'

class PushNotification(NotificationInterface):
    def __init__(self):
        self.config = PushConfiguration()
        if not self.config.validate_config():
            raise ValueError("Invalid push configuration")

    def send(self, recipient, message, **kwargs):
        title = kwargs.get('title', 'Notification')
        config = self.config.get_config()
        print(f"Connecting to Push server: {config['server_url']}")
        print(f"Sending push to: {recipient}; Title: {title}; Message: {message}")
        time.sleep(0.3)
        print("Push simulated successfully!")
        return self.log_notification(recipient, message, title=title)

    def get_type(self):
        return 'push'
