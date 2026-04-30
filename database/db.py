import sqlite3
import os
from flask import g

_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def _close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL CHECK(amount > 0),
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    db.commit()


def seed_db():
    db = get_db()
    db.execute("""
        INSERT OR IGNORE INTO users (name, email, password_hash)
        VALUES ('Demo User', 'demo@spendly.in', 'placeholder')
    """)
    db.commit()
    user = db.execute("SELECT id FROM users WHERE email = 'demo@spendly.in'").fetchone()
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?,?,?,?,?)",
        [
            (user["id"], 1200.00, "Food",      "Lunch at restaurant", "2024-01-15"),
            (user["id"],  500.00, "Transport", "Cab to office",        "2024-01-16"),
            (user["id"], 3500.00, "Bills",     "Electricity bill",     "2024-01-17"),
            (user["id"],  800.00, "Health",    "Pharmacy",             "2024-01-18"),
            (user["id"], 2200.00, "Food",      "Grocery run",          "2024-01-20"),
        ],
    )
    db.commit()


def init_app(app):
    app.teardown_appcontext(_close_db)
