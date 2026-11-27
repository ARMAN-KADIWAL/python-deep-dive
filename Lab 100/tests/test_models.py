import unittest
from datetime import datetime
from src.app import create_app, db, User, Task

class ModelTestCase(unittest.TestCase):
    
    def setUp(self):
        self.flask_app = create_app(test_config={
            "TESTING": True,
            "SECRET_KEY": "unit-test-only",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.app_context = self.flask_app.app_context()
        self.app_context.push()
        self.addCleanup(self.app_context.pop)
        url = db.engine.url
        if url.get_backend_name() != "sqlite" or url.database not in (None, "", ":memory:") or url.query:
            raise RuntimeError("Refusing persistent test database")
        db.create_all()
        self.app = self.flask_app.test_client()

    def tearDown(self):
        db.session.remove()
        db.engine.dispose()

    def test_user_model(self):
        """Test User model functionality"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Test user creation
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))
        self.assertIsInstance(user.created_at, datetime)
    
    def test_task_model(self):
        """Test Task model functionality"""
        # Create user first
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Create task
        task = Task(
            title='Test Task',
            description='Test Description',
            priority='high',
            user_id=user.id
        )
        db.session.add(task)
        db.session.commit()
        
        # Test task creation
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.priority, 'high')
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.user_id, user.id)
        self.assertIsInstance(task.created_at, datetime)

if __name__ == '__main__':
    unittest.main()
