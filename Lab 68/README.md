# Lab 68 — Web Forms with Flask

> **Outcome:** A working validated Flask form with success feedback, saved submissions, detail pages, CSV export, and a protected clear action.

## Completed tasks

1. Set up Flask, templates, and static CSS.
2. Create an HTML form with text, email, number, select, checkbox, and textarea inputs.
3. Process `POST /submit` with server-side validation and flashed errors.
4. Save submissions to `data/submissions.json` and human-readable `data/form_data.txt`.
5. List saved submissions, view an individual record, export CSV, and clear records.
6. **Reconstructed ending of truncated handout:** finish the detail template, add tests, and verify persistence/export.

## Run and test

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
python app.py
```

Open `http://127.0.0.1:5000` if running locally, or use your cloud lab's port-forwarded URL.

## Privacy and safety

- Saved form data contains personal information. Keep `data/` private; it is excluded from Git.
- The form app is for local/classroom use; submissions are not access-controlled.
- The clear action requires `POST` and a CSRF token, unlike the original handout's `GET /clear` suggestion.
- Set `FLASK_SECRET_KEY` in your environment before deployment.
