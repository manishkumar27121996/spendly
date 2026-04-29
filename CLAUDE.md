# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**Spendly** is a personal expense tracking web app built with Python/Flask and SQLite. It is structured as a step-by-step student project — the UI shell, routes, and templates are in place, but the auth and database logic are placeholders to be implemented incrementally across ~9 steps.

## Commands

```bash
# Set up virtual environment (first time)
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt

# Run the dev server
./venv/bin/python app.py          # runs on http://localhost:5001

# Run tests
./venv/bin/python -m pytest

# Run a single test file
./venv/bin/python -m pytest tests/test_foo.py

# Run a single test
./venv/bin/python -m pytest tests/test_foo.py::test_function_name
```

> Always use `./venv/bin/python` — the system Python is externally managed and `pip`/`python` are not on PATH.

## Architecture

**`app.py`** — single entry point. All Flask routes are defined here. Currently maps URLs to templates; auth and expense logic will be added inline as the project progresses.

**`database/db.py`** — the only layer that touches SQLite. Students implement three functions:
- `get_db()` — returns a SQLite connection with `row_factory` set and foreign keys enabled
- `init_db()` — creates all tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — inserts sample data

No ORM; raw SQL via Python's built-in `sqlite3`.

**`templates/`** — Jinja2 templates using `{% extends "base.html" %}` / `{% block %}` inheritance. `base.html` contains the full page shell (navbar, footer, Google Fonts links, CSS/JS includes). All other templates extend it.

**`static/css/`** — two CSS files:
- `style.css` — global design system. All design tokens (colors, fonts, spacing, radii) are CSS custom properties defined in `:root`. Components like navbar, auth forms, footer are styled here.
- `landing.css` — styles specific to the landing page only.

**`static/js/main.js`** — currently empty; students add JS as features are built.

## Planned route structure (from stubs in app.py)

| Route | Step |
|---|---|
| `/` | landing |
| `/register`, `/login`, `/logout` | Steps 2–3 |
| `/profile` | Step 4 |
| `/expenses/add` | Step 7 |
| `/expenses/<id>/edit` | Step 8 |
| `/expenses/<id>/delete` | Step 9 |
