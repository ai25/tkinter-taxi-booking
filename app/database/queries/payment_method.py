import secrets
import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING

from app.database.models import PaymentMethod, User
from app.utils.auth import Auth


if TYPE_CHECKING:
    from app.database.db import Database


class PaymentMethodQueries:
    def __init__(self, db: "Database"):
        self.db = db

    def get_by_id(self, id: int):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM payment_method WHERE id = ?", (id,))
                row = cursor.fetchone()
                return (PaymentMethod(**dict(row)) if row else None, None)
        except sqlite3.Error as e:
            return (None, str(e))
