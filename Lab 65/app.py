"""Lab 65: Intro to Flask — routes, URL parameters, navigation, and 404 handling."""

import os
from html import escape

from flask import Flask, url_for

app = Flask(__name__)


def page(title, content):
    """A small shared HTML layout for every page."""
    links = [
        ("Home", url_for("home")),
        ("About", url_for("about")),
        ("Contact", url_for("contact")),
        ("Sample User", url_for("user_profile", name="Arman")),
        ("Sample Product", url_for("product", product_id=42)),
    ]
    navigation = " ".join(
        f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'
        for label, url in links
    )
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} | Flask Lab 65</title>
    <style>
      body {{ font: 17px/1.6 system-ui, sans-serif; background: #f2f5fa;
              color: #182b45; max-width: 800px; margin: 3rem auto; padding: 1rem; }}
      nav {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
      a {{ color: #0758a6; }}
      main {{ margin-top: 1.5rem; background: white; border-radius: 12px;
              padding: 1.5rem; box-shadow: 0 4px 16px #16345b18; }}
    </style>
</head>
<body>
  <nav>{navigation}</nav>
  <main><h1>{escape(title)}</h1>{content}</main>
</body>
</html>"""


@app.get("/")
def home():
    return page("Welcome to Flask", "<p>Hello World! Your first Flask app is running.</p>")


@app.get("/about")
def about():
    return page("About", "<p>This lab introduces Flask routes and responses.</p>")


@app.get("/contact")
def contact():
    return page("Contact", "<p>Practice contact: hello@example.com</p>")


@app.get("/user/<name>")
def user_profile(name):
    return page("User Profile", f"<p>Hello, <strong>{escape(name)}</strong>!</p>")


@app.get("/product/<int:product_id>")
def product(product_id):
    return page("Product Details", f"<p>Product ID: {product_id}</p>")


@app.errorhandler(404)
def not_found(error):
    return page("Page Not Found", "<p>Sorry, this page does not exist.</p>"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
