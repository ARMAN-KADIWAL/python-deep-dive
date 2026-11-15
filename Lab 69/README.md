# Lab 69 — User Authentication with Flask

> **Outcome:** Working user registration, hashed passwords, login sessions, protected dashboard/profile pages, logout, and CSRF-aware forms.

## Tasks completed

1. Create the Flask project with a Python virtual environment.
2. Model `User` in SQLite using Flask-SQLAlchemy.
3. Build `RegistrationForm` and `LoginForm` with Flask-WTF.
4. Configure Flask-Login sessions and password hashing.
5. Implement registration, login, dashboard, profile, and logout.
6. Add reusable templates, CSS styling, feedback messages, and custom 404 handling.
7. Verify the full authentication flow with an isolated temporary database.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python3 -m py_compile app.py models.py forms.py
python test_smoke.py
flask --app app routes
python app.py
```

Use `http://127.0.0.1:5000` only when running Flask on your computer; on a cloud lab, use its port-forwarded URL.

## Why the earlier lab code failed

- The database config key must be **`SQLALCHEMY_DATABASE_URI`** (not `..._URL`).
- Import names are case-sensitive: `LoginForm`, `Flask`, `flash`, `werkzeug`.
- Assignment uses `=`: `user = User.query...`.
- Flask routes start with forward slash: `/profile`, not `\\profile`.
- `email-validator` is required by WTForms' email field validator.
- All route definitions belong **before** `app.run()`.

## Security notes

- Passwords are hashed with Werkzeug, never stored as plaintext.
- `logout` is POST-only and has a CSRF token.
- SQLite database and `.env` are ignored by Git.
- Set a strong, persistent `FLASK_SECRET_KEY` for deployment. If unset, the server generates a new one on restart, invalidating older login sessions.
- This is a classroom project; use production-grade deployment and additional protections for real user accounts.
