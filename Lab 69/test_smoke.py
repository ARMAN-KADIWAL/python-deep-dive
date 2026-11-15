"""Smoke test the lab routes and authentication with Flask's test client."""

import os
import re
import tempfile
from pathlib import Path

# Use a fresh, temporary SQLite database; never test against a student's real accounts.
_temporary_database = tempfile.TemporaryDirectory()
os.environ["FLASK_DATABASE_URI"] = (
    "sqlite:///" + str(Path(_temporary_database.name) / "test_users.db")
)

from app import app


def get_token(page):
    match = re.search(rb'name="csrf_token"[^>]*value="([^"]+)"', page)
    assert match, "CSRF token missing from page"
    return match.group(1).decode("utf-8")


def main():
    app.config["TESTING"] = True
    client = app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/register").status_code == 200
    assert client.get("/login").status_code == 200
    assert client.get("/dashboard").status_code == 302
    assert client.get("/profile").status_code == 302
    assert client.get("/does-not-exist").status_code == 404

    token = get_token(client.get("/register").data)
    response = client.post(
        "/register",
        data={
            "csrf_token": token,
            "username": "smoke_tester",
            "email": "smoke@example.org",
            "password": "correct-horse-battery-staple",
            "password2": "correct-horse-battery-staple",
        },
    )
    assert response.status_code == 302, response.data[:300]
    assert response.headers["Location"].endswith("/login")

    token = get_token(client.get("/login").data)
    bad_response = client.post(
        "/login",
        data={"csrf_token": token, "username": "smoke_tester", "password": "wrong"},
    )
    assert bad_response.status_code == 200
    assert b"Invalid username or password" in bad_response.data

    token = get_token(client.get("/login").data)
    response = client.post(
        "/login",
        data={
            "csrf_token": token,
            "username": "smoke_tester",
            "password": "correct-horse-battery-staple",
        },
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/dashboard")
    assert client.get("/dashboard").status_code == 200
    assert client.get("/profile").status_code == 200

    token = get_token(client.get("/dashboard").data)
    response = client.post("/logout", data={"csrf_token": token})
    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 302

    print("PASS: home, forms, 404, protected pages, register, failed login, login, logout, CSRF")


if __name__ == "__main__":
    main()
