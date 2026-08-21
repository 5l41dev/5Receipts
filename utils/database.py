# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
"""
Database helpers.

The licenses table is created automatically on first run, so a fresh clone
works without manually creating any database.
"""

import sqlite3

DB_PATH = "data.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS licenses (
    owner_id INTEGER,
    email TEXT,
    key TEXT,
    expiry DATE,
    emailtf BOOLEAN,
    credentialstf BOOLEAN,
    last_email_update DATE,
    name TEXT,
    street TEXT,
    city TEXT,
    zipp TEXT,
    country TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_owner_id ON licenses (owner_id);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the schema if it does not exist yet."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
