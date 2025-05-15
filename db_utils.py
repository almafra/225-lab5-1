# db_utils.py

import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with the contacts table."""
    db = connect_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        );
    ''')
    db.commit()
    db.close()
