from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from pathlib import Path
import os
import secrets
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


def create_app(config_name=None, test_config=None):
    root = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(root / "templates"),
                static_folder=str(root / "static"))
    app.config.from_object(config[config_name or os.environ.get("FLASK_ENV", "default")])
    if test_config is not None:
        app.config.update(test_config)
    db.init_app(app)
    login_manager.init_app(app)
    register_routes(app)
    return app

# Database Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Example model for Task Management App
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



def register_routes(app):
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            tasks = Task.query.filter_by(user_id=current_user.id).all()
            return render_template('dashboard.html', tasks=tasks)
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('Username or email already exists')
                return redirect(url_for('register'))
            
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful')
            return redirect(url_for('login'))
        
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
        
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/add_task', methods=['POST'])
    @login_required
    def add_task():
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        
        task = Task(title=title, description=description, priority=priority, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        
        flash('Task added successfully')
        return redirect(url_for('index'))

    @app.route('/update_task/<int:task_id>', methods=['POST'])
    @login_required
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('Unauthorized')
            return redirect(url_for('index'))
        
        if request.form.get('status') not in ('pending', 'in_progress', 'completed'):
            return jsonify({'success': False}), 400
        task.status = request.form['status']
        db.session.commit()
        
        return jsonify({'success': True})

    @app.route('/delete_task/<int:task_id>', methods=['POST'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            flash('Unauthorized')
            return redirect(url_for('index'))
        
        db.session.delete(task)
        db.session.commit()
        
        flash('Task deleted successfully')
        return redirect(url_for('index'))

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy", "application": "Task Manager"})


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=False)
