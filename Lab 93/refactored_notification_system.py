import time
from notification_factory import NotificationFactory
from notification_logger import NotificationLogger
from configuration_manager import ConfigurationManager

class RefactoredNotificationSystem:
    def __init__(self):
        self.logger = NotificationLogger()
        self.config_manager = ConfigurationManager()
        self.config_manager.load_config()
        self.logger.load_logs_from_file()

    def send_notification(self, notification_type, recipient, message, **kwargs):
        try:
            notification = NotificationFactory.create_notification(notification_type)
            log_entry = notification.send(recipient, message, **kwargs)
            success = True
        except Exception as e:
            print(f"Failed to send {notification_type} notification: {e}")
            log_entry = dict(type=notification_type.lower(), recipient=recipient, message=message,
                             timestamp=time.time(), status='failed', error=str(e))
            success = False
        self.logger.add_log_entry(log_entry)
        if self.config_manager.get_config('logging', 'auto_save'):
            self.logger.save_logs_to_file()
        return success

    def send_bulk_notifications(self, notifications_list):
        results = [{'notification': data, 'success': self.send_notification(**data)}
                   for data in notifications_list]
        print(f"Bulk notification complete: {sum(r['success'] for r in results)}/{len(results)} successful")
        return results

    def get_notification_history(self, notification_type=None, limit=None):
        return self.logger.get_logs(notification_type, limit)

    def get_notification_summary(self):
        return self.logger.get_log_summary()

    def get_available_notification_types(self):
        return NotificationFactory.get_available_types()

    def update_configuration(self, section, key, value):
        self.config_manager.set_config(section, key, value)
        return self.config_manager.save_config()

    def get_configuration(self, section=None, key=None):
        return self.config_manager.get_config(section, key)

    def export_logs(self):
        return self.logger.save_logs_to_file()

    def clear_logs(self):
        self.logger.clear_logs()
        if self.config_manager.get_config('logging', 'auto_save'):
            self.logger.save_logs_to_file()

def test_refactored_system():
    print("=== Testing Refactored Notification System ===")
    system = RefactoredNotificationSystem()
    print(f"Available notification types: {system.get_available_notification_types()}")
    assert system.send_notification('email', 'user@example.com', 'Welcome!', subject='Upgrade')
    assert system.send_notification('sms', '+1234567890', 'Account upgraded')
    assert system.send_notification('push', 'device_xyz789', 'New features!', title='App Update')
    assert system.send_notification('slack', '@john.doe', 'Refactoring complete!', channel='#development')
    results = system.send_bulk_notifications([
        dict(notification_type='email', recipient='admin@example.com', message='Maintenance completed', subject='Report'),
        dict(notification_type='sms', recipient='+1987654321', message='Order shipped'),
        dict(notification_type='push', recipient='device_abc456', message='New message', title='Inbox')
    ])
    assert all(r['success'] for r in results)
    print("Notification summary:", system.get_notification_summary())
    print("Recent history:", system.get_notification_history(limit=5))
    print("Current email timeout:", system.get_configuration('email', 'timeout'))
    assert system.update_configuration('email', 'timeout', 45)
    assert system.get_configuration('email', 'timeout') == 45
    print("Updated email timeout: 45")
    assert NotificationLogger() is NotificationLogger()
    assert ConfigurationManager() is ConfigurationManager()
    print("Logger Singleton: PASSED")
    print("Configuration Singleton: PASSED")
    for notification_type in system.get_available_notification_types():
        notification = NotificationFactory.create_notification(notification_type)
        assert notification.get_type() == notification_type
        print(f"{notification_type.upper()} Factory: PASSED")
    assert not system.send_notification('invalid_type', 'test@example.com', 'Testing error handling')
    print("Invalid notification handling: PASSED")
    for log in system.get_notification_history(notification_type='email'):
        print(f"EMAIL: {log['recipient']} - {log['status']}")
    assert system.export_logs()
    print("Lab 93 completed successfully!")

if __name__ == "__main__":
    test_refactored_system()
