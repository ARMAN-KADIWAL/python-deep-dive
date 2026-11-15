"""Lab 67: Jinja template rendering, dynamic data, loops, and search."""

import os

from flask import Flask, abort, render_template, request

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com",
     "role": "Admin", "is_active": True, "posts_count": 25},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com",
     "role": "User", "is_active": True, "posts_count": 12},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com",
     "role": "Moderator", "is_active": False, "posts_count": 8},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com",
     "role": "User", "is_active": True, "posts_count": 31},
]

ITEMS = [
    {"id": 1, "title": "Flask Tutorial", "category": "tutorial",
     "author": "Alice", "content": "Learn Flask web development", "date": "2024-01-15"},
    {"id": 2, "title": "Python Basics", "category": "tutorial",
     "author": "Bob", "content": "Introduction to Python programming", "date": "2024-01-10"},
    {"id": 3, "title": "Web Development News", "category": "news",
     "author": "Charlie", "content": "Latest trends in web development", "date": "2024-01-20"},
    {"id": 4, "title": "Flask Templates Guide", "category": "tutorial",
     "author": "Diana", "content": "Master Jinja2 templates in Flask", "date": "2024-01-18"},
    {"id": 5, "title": "Python 3.12 Released", "category": "news",
     "author": "Eve", "content": "New features in Python 3.12", "date": "2024-01-22"},
    {"id": 6, "title": "Database Integration", "category": "tutorial",
     "author": "Frank", "content": "Connect Flask with databases", "date": "2024-01-12"},
]


@app.get("/")
def home():
    return render_template("index.html", title="Welcome to Flask Templates")


@app.get("/user/<username>")
def user_profile(username):
    user_data = {
        "name": username,
        "email": f"{username}@example.com",
        "joined_date": "2024-01-15",
        "is_active": True,
    }
    return render_template("user_profile.html", user=user_data)


@app.get("/users")
def users_list():
    return render_template("users_list.html", users=USERS, filter_type="All Users")


@app.get("/users/active")
def active_users():
    active = [user for user in USERS if user["is_active"]]
    return render_template("users_list.html", users=active, filter_type="Active Users Only")


@app.get("/search")
def search():
    return render_template("search.html")


@app.get("/search/results")
def search_results():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "all").strip().lower()
    if category not in {"all", "tutorial", "news"}:
        category = "all"
    results = [
        item for item in ITEMS
        if query.casefold() in (
            f'{item["title"]} {item["author"]} {item["content"]}'
        ).casefold()
        and (category == "all" or item["category"] == category)
    ] if query else []
    return render_template(
        "search_results.html", query=query, category=category,
        results=results, total_results=len(results),
    )


@app.get("/item/<int:item_id>")
def view_item(item_id):
    item = next((item for item in ITEMS if item["id"] == item_id), None)
    if item is None:
        abort(404)
    return render_template("item_detail.html", item=item)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
