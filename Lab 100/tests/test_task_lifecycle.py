"""Integration tests for authenticated task lifecycle and ownership checks."""
import unittest

from src.app import Task, User, create_app, db


class TaskLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            test_config={
                "TESTING": True,
                "SECRET_KEY": "unit-test-only",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
            }
        )
        with self.app.app_context():
            url = db.engine.url
            if (
                url.get_backend_name() != "sqlite"
                or url.database not in (None, "", ":memory:")
                or url.query
            ):
                raise RuntimeError("Refusing persistent test database")
            db.create_all()
            for username in ("owner", "other"):
                user = User(username=username, email=f"{username}@example.com")
                user.set_password("testpassword")
                db.session.add(user)
            db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()

    def login(self, username):
        response = self.client.post(
            "/login",
            data={"username": username, "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 302)

    def create_task(self):
        self.login("owner")
        response = self.client.post(
            "/add_task",
            data={"title": "Sample task", "description": "Example", "priority": "high"},
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            return Task.query.filter_by(title="Sample task").one().id

    def test_update_and_delete(self):
        task_id = self.create_task()
        response = self.client.post(
            f"/update_task/{task_id}", data={"status": "invalid"}
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            f"/update_task/{task_id}", data={"status": "completed"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])
        with self.app.app_context():
            self.assertEqual(db.session.get(Task, task_id).status, "completed")
        self.assertEqual(
            self.client.post(f"/delete_task/{task_id}").status_code, 302
        )
        with self.app.app_context():
            self.assertIsNone(db.session.get(Task, task_id))

    def test_other_user_cannot_modify_or_delete_task(self):
        task_id = self.create_task()
        self.assertEqual(self.client.get("/logout").status_code, 302)
        self.login("other")
        self.client.post(f"/update_task/{task_id}", data={"status": "completed"})
        self.client.post(f"/delete_task/{task_id}")
        with self.app.app_context():
            task = db.session.get(Task, task_id)
            self.assertIsNotNone(task)
            self.assertEqual(task.status, "pending")
        self.assertNotIn(b"Sample task", self.client.get("/").data)

    def test_login_failure_duplicate_registration_and_health(self):
        response = self.client.post(
            "/login", data={"username": "owner", "password": "wrong"}
        )
        self.assertIn(b"Invalid username or password", response.data)
        response = self.client.post(
            "/register",
            data={
                "username": "owner",
                "email": "owner@example.com",
                "password": "testpassword",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Username or email already exists", response.data)
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_anonymous_task_creation_requires_login(self):
        response = self.client.post(
            "/add_task", data={"title": "unauthorized", "priority": "high"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])
        with self.app.app_context():
            self.assertEqual(Task.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
