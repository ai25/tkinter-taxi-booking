import sqlite3
from pathlib import Path


class Database:
    db_path = "app.db"

    def __init__(self):
        self._initialise()

    def _initialise(self):
        self._create_tables()

    def _create_tables(self):
        try:
            with sqlite3.connect(self.db_path) as conn, Path.open("app/database/schema.sql") as schema:
                conn.executescript(schema.read())
                print(schema.read())
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to create tables", e)

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
