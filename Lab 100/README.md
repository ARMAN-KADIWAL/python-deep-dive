# Lab 100: Capstone Project - Full Stack Python Application

Task Management option selected to match provided code. The truncated production app was reconstructed from the earlier complete app using an application factory, template paths, independent test DBs, and WSGI entry point. Run `python -m pytest tests/ -v` and `python -m src.app`, then open http://127.0.0.1:5000. Public production deployment and load testing are not verified. Automated CI enforces a minimum 81% line coverage target for this lab.

## Files

- `requirements.txt`
- `src/app.py`
- `templates/base.html`
- `templates/dashboard.html`
- `templates/login.html`
- `templates/register.html`
- `templates/index.html`
- `tests/test_app.py`
- `tests/test_models.py`
- `.flake8`
- `pyproject.toml`
- `config.py`
- `src/__init__.py`
- `wsgi.py`
- `.env.example`
- `.gitignore`
- `docs/architecture.md`
- `docs/requirements.md`
- `docs/deployment.md`

- `tests/test_task_lifecycle.py`

## Verification status

Source-based implementation with reconstructed endings where the supplied material was truncated. Automated checks are provided separately; no unobserved cloud-lab results or completion screenshots are claimed.

Recorded CI verification: 11 tests passed, with 5 warnings and 97.58% line coverage (81% minimum enforced). See [GitHub Actions](https://github.com/ARMAN-KADIWAL/python-deep-dive/actions/runs/46041721824) for the exact run and scope.
