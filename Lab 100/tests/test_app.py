import unittest
from src.app import create_app, db, User, Task

class TaskManagerTestCase(unittest.TestCase):
    
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

    def test_index_page(self):
        """Test the index page loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome to Task Manager', rv.data)
    
    def test_user_registration(self):
        """Test user registration functionality"""
        rv = self.app.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Registration successful', rv.data)
    
    def test_user_login(self):
        """Test user login functionality"""
        # First register a user
        with self.flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
        
        # Then try to login
        rv = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
    
    def test_task_creation(self):
        """Test task creation functionality"""
        # Register and login user
        with self.flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        # Create task
        rv = self.app.post('/add_task', data={
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Task added successfully', rv.data)
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        with self.flask_app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            self.assertTrue(user.check_password('testpassword'))
            self.assertFalse(user.check_password('wrongpassword'))

if __name__ == '__main__':
    unittest.main()
