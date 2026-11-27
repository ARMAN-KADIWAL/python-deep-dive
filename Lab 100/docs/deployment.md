# Deployment and maintenance (reconstructed)

From the project root, create an approved virtual environment and install requirements. Generate a strong SECRET_KEY and keep .env private. Initialize the database with `python -m src.app`, or use `gunicorn --bind 127.0.0.1:5000 wsgi:app`. Check `/health`, run tests, back up SQLite before changes, and review logs. This is a local/cloud-VM lab demonstration; do not expose it publicly before CSRF, TLS, session hardening and migration work. No AWS/Heroku deployment is claimed.
