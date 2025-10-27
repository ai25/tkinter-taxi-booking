import secrets
import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING

from app.database.models import User
from app.utils.auth import Auth


if TYPE_CHECKING:
    from app.database.db import Database


class UserQueries:
    def __init__(self, db: "Database"):
        self.db = db

    def get_by_id(self, user_id: int):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                return (User(**dict(row)) if row else None, None)
        except sqlite3.Error as e:
            return (None, str(e))

    def get_by_email(self, email: str):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM user WHERE email = ?", (email,))
                row = cursor.fetchone()
                return (User(**dict(row)) if row else None, None)
        except sqlite3.Error as e:
            return (None, str(e))

    def upsert(self, user: User):
        try:
            with self.db.get_connection() as conn:
                if user.id is None:
                    now = int(datetime.now().timestamp())
                    cursor = conn.execute(
                        "INSERT INTO user(role, full_name, email, password, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (user.role, user.full_name, user.email, user.password, user.phone, now),
                    )
                    conn.commit()
                    return (cursor.lastrowid, None)

                conn.execute(
                    "UPDATE user SET full_name=?, email=?, password=?, phone=? WHERE id=?",
                    (user.full_name, user.email, user.password, user.phone, user.id),
                )
                conn.commit()
                return (user.id, None)
        except sqlite3.IntegrityError:
            return (None, "User already exists")
        except sqlite3.Error as e:
            return (None, str(e))

    def authenticate(self, email: str, password: str):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM user WHERE email = ?", (email,))
                row = cursor.fetchone()

                if row and Auth.verify_password(password, row[4]):
                    return (User(**dict(row)), None)

                return None, "Incorrect email or password"
        except sqlite3.Error as e:
            print(f"Unexpected error: {e}")
            return (None, "Something went wrong. Please try again later")

    def create_session(self, user_id: int):
        try:
            with self.db.get_connection() as conn:
                session_token = secrets.token_urlsafe(32)
                conn.execute("UPDATE user SET session_token = ? WHERE id = ?", (session_token, user_id))
                conn.commit()
                return session_token

        except sqlite3.Error as e:
            print(f"Failed to create token: {e}")
            raise

    def get_by_session(self, user_id: int, session_token: str) -> User | None:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM user WHERE id = ? AND session_token = ?", (user_id, session_token))
                row = cursor.fetchone()
                return User(**dict(row)) if row else None

        except sqlite3.Error as e:
            print(f"Could not get user by session: {e}")
            return None
