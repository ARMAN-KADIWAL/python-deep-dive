import time

class NotificationSystem:
    def __init__(self):
        self.email_config = {'smtp_server': 'smtp.example.com', 'port': 587,
                             'username': 'system@example.com', 'password': 'DEMO_ONLY'}
        self.sms_config = {'api_key': 'DEMO_ONLY', 'sender_id': 'NOTIFY',
                           'base_url': 'https://api.sms.com'}
        self.push_config = {'app_id': 'push_app_123', 'api_key': 'DEMO_ONLY',
                            'server_url': 'https://push.example.com'}
        self.notification_log = []

    def send_email_notification(self, recipient, subject, message):
        print(f"Simulating email via {self.email_config['smtp_server']} to {recipient}: {subject}: {message}")
        time.sleep(1)
        self.notification_log.append(dict(type='email', recipient=recipient, subject=subject,
                                          message=message, timestamp=time.time(), status='sent'))
        return True

    def send_sms_notification(self, phone_number, message):
        print(f"Simulating SMS via {self.sms_config['base_url']} to {phone_number}: {message}")
        time.sleep(0.5)
        self.notification_log.append(dict(type='sms', recipient=phone_number,
                                          message=message, timestamp=time.time(), status='sent'))
        return True

    def send_push_notification(self, device_id, title, message):
        print(f"Simulating push via {self.push_config['server_url']} to {device_id}: {title}: {message}")
        time.sleep(0.3)
        self.notification_log.append(dict(type='push', recipient=device_id, title=title,
                                          message=message, timestamp=time.time(), status='sent'))
        return True

    def send_notification_by_preference(self, user_id, preference, **kwargs):
        if preference == 'email' and all(k in kwargs for k in ('email', 'subject', 'message')):
            return self.send_email_notification(kwargs['email'], kwargs['subject'], kwargs['message'])
        elif preference == 'sms' and all(k in kwargs for k in ('phone', 'message')):
            return self.send_sms_notification(kwargs['phone'], kwargs['message'])
        elif preference == 'push' and all(k in kwargs for k in ('device_id', 'title', 'message')):
            return self.send_push_notification(kwargs['device_id'], kwargs['title'], kwargs['message'])
        return False

    def get_notification_history(self):
        return self.notification_log

    def clear_notification_history(self):
        self.notification_log = []

def test_original_system():
    notifier = NotificationSystem()
    notifier.send_email_notification("user@example.com", "Welcome!", "Thank you for joining!")
    notifier.send_sms_notification("+1234567890", "Verification code: 123456")
    notifier.send_push_notification("device_abc123", "New Message", "You have a new message!")
    notifier.send_notification_by_preference("user123", "email", email="user@example.com",
                                             subject="Account Update", message="Updated")
    assert len(notifier.get_notification_history()) == 4
    for i, record in enumerate(notifier.get_notification_history(), 1):
        print(f"{i}. {record['type'].upper()}: {record['recipient']}")

if __name__ == "__main__":
    test_original_system()
