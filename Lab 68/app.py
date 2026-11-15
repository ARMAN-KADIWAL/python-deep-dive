"""Lab 68: Form validation, submission storage, detail pages, CSV export."""

import csv
import io
import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
CSRFProtect(app)

# Separate file paths make test isolation and data preservation straightforward.
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_FILE = DATA_DIR / "submissions.json"
TEXT_FILE = DATA_DIR / "form_data.txt"

FIELDS = (
    "submission_time", "first_name", "last_name", "email", "phone",
    "age", "country", "interests", "message", "newsletter",
)


def load_submissions():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open(encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        app.logger.exception("Unable to load saved submissions")
        return []


def save_submissions(submissions):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(submissions, file, indent=2, ensure_ascii=False)


def append_readable_record(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with TEXT_FILE.open("a", encoding="utf-8") as file:
        file.write(f"--- Form Submission {data['submission_time']} ---\n")
        file.write(f"Name: {data['first_name']} {data['last_name']}\n")
        file.write(f"Email: {data['email']}\n")
        file.write(f"Phone: {data['phone']}\n")
        file.write(f"Age: {data['age']}\n")
        file.write(f"Country: {data['country']}\n")
        file.write(f"Interests: {', '.join(data['interests'])}\n")
        file.write(f"Newsletter: {data['newsletter']}\n")
        file.write(f"Message: {data['message']}\n\n")


def validate_form_data(data):
    errors = []
    for field, label in (
        ("first_name", "First name"), ("last_name", "Last name"),
        ("email", "Email"), ("country", "Country"), ("message", "Message"),
    ):
        if not data[field]:
            errors.append(f"{label} is required.")
    if data["first_name"] and len(data["first_name"]) < 2:
        errors.append("First name must be at least 2 characters.")
    if data["last_name"] and len(data["last_name"]) < 2:
        errors.append("Last name must be at least 2 characters.")
    if data["email"] and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", data["email"]):
        errors.append("Please enter a valid email address.")
    if data["age"]:
        try:
            if not 13 <= int(data["age"]) <= 120:
                errors.append("Age must be between 13 and 120.")
        except ValueError:
            errors.append("Please enter a valid age.")
    if data["phone"] and not re.fullmatch(r"\d{3}-\d{3}-\d{4}", data["phone"]):
        errors.append("Phone number format must be 123-456-7890.")
    if data["message"] and len(data["message"]) < 10:
        errors.append("Message must be at least 10 characters.")
    return errors


@app.get("/")
def index():
    return render_template("form.html")


@app.post("/submit")
def submit_form():
    data = {
        "first_name": request.form.get("first_name", "").strip(),
        "last_name": request.form.get("last_name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "age": request.form.get("age", "").strip(),
        "country": request.form.get("country", "").strip(),
        "interests": request.form.getlist("interests"),
        "message": request.form.get("message", "").strip(),
        "newsletter": "yes" if request.form.get("newsletter") == "yes" else "no",
        "submission_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
    errors = validate_form_data(data)
    if errors:
        for message in errors:
            flash(message, "error")
        return redirect(url_for("index"))

    try:
        submissions = load_submissions()
        submissions.append(data)
        save_submissions(submissions)
        append_readable_record(data)
    except OSError:
        app.logger.exception("Unable to save form submission")
        flash("Sorry, your submission could not be saved.", "error")
        return redirect(url_for("index"))
    flash(f"Thank you, {data['first_name']}! Your form was submitted.", "success")
    return redirect(url_for("success_page"))


@app.get("/success")
def success_page():
    return render_template("success.html")


@app.get("/submissions")
def view_submissions():
    submissions = load_submissions()
    return render_template("submissions.html", submissions=submissions)


@app.get("/submission/<int:index>")
def view_submission(index):
    submissions = load_submissions()
    if not 0 <= index < len(submissions):
        flash("Submission not found.", "error")
        return redirect(url_for("view_submissions"))
    return render_template("submission_detail.html", submission=submissions[index], index=index)


@app.get("/export")
def export_submissions():
    submissions = load_submissions()
    if not submissions:
        flash("No submissions to export.", "info")
        return redirect(url_for("view_submissions"))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(FIELDS)
    for submission in submissions:
        writer.writerow([
            ", ".join(submission[field]) if field == "interests"
            else submission[field] for field in FIELDS
        ])
    return Response(
        output.getvalue(), mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=form_submissions.csv"},
    )


@app.post("/clear")
def clear_submissions():
    # Destructive action is POST-only, guarded by Flask-WTF CSRF protection.
    save_submissions([])
    TEXT_FILE.unlink(missing_ok=True)
    flash("Saved submissions cleared.", "info")
    return redirect(url_for("view_submissions"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
