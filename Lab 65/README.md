# Lab 65 — Introduction to Flask

> **Outcome:** A working beginner-friendly Flask website with five routes, dynamic URL parameters, navigation, and a custom 404 response.

## Tasks covered

1. Install Flask in a Python virtual environment.
2. Build a Hello World route at `/`.
3. Add About, Contact, User, and Product routes.
4. Test dynamic string/integer URL converters.
5. Add navigation links and HTML styling.
6. Handle unknown URLs with a helpful 404 page.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` on the **same machine** running Flask. On a cloud lab, use the lab's port-forwarded URL.

## Verify

```bash
python -m unittest discover -v
```

Sample routes: `/`, `/about`, `/contact`, `/user/Arman`, `/product/42`, `/missing`.

**Note:** This is an educational development server, not a production deployment.
