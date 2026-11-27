# Task Manager architecture

Browser → Flask routes → SQLAlchemy → SQLite. Flask-Login handles sessions. The application factory initializes extensions after configuration, and tests use independent in-memory SQLite databases. Templates are loaded from the project root.
