# Lab 66 — Building RESTful APIs with Flask

> **Outcome:** JSON API for item creation, retrieval, filtering, sorting, and summary statistics.

## Tasks covered

1. Install Flask and Flask-RESTful.
2. Expose a basic JSON endpoint.
3. Implement `GET` (all/single) and `POST` (create).
4. Build filtered/sorted/limited list results.
5. Compute total, average, category statistics, and most expensive item.
6. Test valid and invalid requests (browser, curl, Postman or HTTPie).

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
python app.py
```

## Try the API

```bash
curl http://127.0.0.1:5000/api/items
curl http://127.0.0.1:5000/api/items/1
curl 'http://127.0.0.1:5000/api/items/list?category=Electronics&sort_by=price&order=desc&limit=5'
curl http://127.0.0.1:5000/api/items/stats
curl -X POST http://127.0.0.1:5000/api/items -H 'Content-Type: application/json' -d '{"name":"Mouse","category":"Electronics","price":25}'
```

## Notes

- Items are **in memory**, so POSTed entries reset on restart, as in the original lab.
- Input validation returns clear 400 responses instead of server errors.
- The built-in Flask server is suitable for this lab, not public production hosting.
