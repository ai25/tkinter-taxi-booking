import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from app.database.queries.booking import BookingQueries
from app.database.queries.payment_method import PaymentMethodQueries
from app.database.queries.user import UserQueries


class Database:
    _instance: Optional["Database"] = None
    _db_path = "app.db"
    _schema_path = Path(__file__).parent / "schema.sql"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if not self._initialised:
            self._create_tables()
            self._initialised = True

    def _create_tables(self):
        try:
            with sqlite3.connect(self._db_path) as conn:
                schema = self._schema_path.read_text()
                conn.executescript(schema)
                conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Failed to create tables: {e}")

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @property
    def user(self):
        return UserQueries(self)

    @property
    def booking(self):
        return BookingQueries(self)

    @property
    def payment_method(self):
        return PaymentMethodQueries(self)
