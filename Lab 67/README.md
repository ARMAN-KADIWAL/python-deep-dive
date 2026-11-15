# Lab 67 — Template Rendering with Flask

> **Outcome:** A multi-page Jinja website with reusable layout, dynamic profiles, conditional user cards, searchable content, and item detail pages.

## Original lab scope and reconstructed ending

1. Base template and home page.
2. Pass Python dictionaries into Jinja templates.
3. Use `for`, `if`, and `else` for a users list.
4. Search with URL query parameters and category filtering.
5. **Reconstructed from the truncated handout:** complete `search_results.html`, individual `item_detail.html`, 404 handling, and final tests.

## Run and test

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
python app.py
```

Try: `/`, `/user/Arman`, `/users`, `/users/active`, `/search`, `/search/results?q=Flask&category=tutorial`, `/item/1`.

**Note:** The supplied Lab 67 handout ends partway through the search-results HTML. Remaining screens and checks are a functional completion, not a verbatim reproduction of missing lab text.
