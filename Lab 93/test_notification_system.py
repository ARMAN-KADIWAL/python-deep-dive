import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from notification_factory import NotificationFactory
from notification_logger import NotificationLogger
from configuration_manager import ConfigurationManager
from refactored_notification_system import RefactoredNotificationSystem
from original_notification_system import NotificationSystem

class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.logger = NotificationLogger()
        self.config = ConfigurationManager()
        self.old_log_path = self.logger._log_file
        self.old_config_path = self.config._config_file
        self.logger._log_file = str(Path(self.temp.name) / 'history.json')
        self.config._config_file = str(Path(self.temp.name) / 'config.json')
        self.logger.clear_logs()
        self.config.reset_to_defaults()
        self.system = RefactoredNotificationSystem()

    def tearDown(self):
        self.logger.clear_logs()
        self.config.reset_to_defaults()
        self.logger._log_file = self.old_log_path
        self.config._config_file = self.old_config_path
        self.temp.cleanup()

    def test_singletons(self):
        self.assertIs(NotificationLogger(), self.logger)
        self.assertIs(ConfigurationManager(), self.config)

    def test_factory(self):
        for kind in ('email', 'sms', 'push', 'slack'):
            self.assertEqual(NotificationFactory.create_notification(kind).get_type(), kind)
        with self.assertRaises(ValueError):
            NotificationFactory.create_notification('invalid')

    @patch('time.sleep')
    def test_bulk_and_history(self, sleep):
        results = self.system.send_bulk_notifications([
            dict(notification_type=kind, recipient='demo', message='test')
            for kind in ('email', 'sms', 'push', 'slack')])
        self.assertTrue(all(r['success'] for r in results))
        self.assertEqual(self.logger.get_log_count(), 4)
        self.assertEqual(len(self.logger.get_logs('email')), 1)
        self.assertEqual(len(self.logger.get_logs(limit=2)), 2)
        self.assertEqual(self.logger.get_logs(limit=0), [])

    def test_failed_notification(self):
        self.assertFalse(self.system.send_notification('unknown', 'demo', 'test'))
        self.assertEqual(self.logger.get_logs()[0]['status'], 'failed')
        self.logger.clear_logs()
        self.assertTrue(self.logger.load_logs_from_file())
        self.assertEqual(self.logger.get_logs()[0]['status'], 'failed')

    def test_shared_configuration(self):
        self.assertTrue(self.system.update_configuration('email', 'timeout', 45))
        email = NotificationFactory.create_notification('email')
        self.assertEqual(email.config.get_config()['timeout'], 45)
        self.config.reset_to_defaults()
        self.assertTrue(self.config.load_config())
        self.assertEqual(self.config.get_config('email', 'timeout'), 45)

    @patch('time.sleep')
    def test_original_behavior(self, sleep):
        original = NotificationSystem()
        self.assertTrue(original.send_email_notification('demo', 'subject', 'message'))
        self.assertTrue(original.send_sms_notification('demo', 'message'))
        self.assertTrue(original.send_push_notification('demo', 'title', 'message'))
        self.assertEqual(len(original.get_notification_history()), 3)

if __name__ == '__main__':
    unittest.main()
