from datetime import datetime

from app.database import Database
from app.models import User


class UserRepository:
    def get_by_id(self, id) -> User | None:
        with Database().get_connection() as conn:
            cursor = conn.execute("SELECT * FROM user WHERE id = ?", id)
            row = cursor.fetchone()
            return User(*row) if row else None

    def upsert(self, user: User) -> int | None:
        with Database().get_connection() as conn:
            if user.id is None:
                # Insert
                now = int(datetime.now().timestamp())
                user.created_at = now

                cursor = conn.execute(
                    "INSERT INTO user(role, full_name, email, password, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (user.role, user.full_name, user.email, user.password, user.phone, user.created_at),
                )
                conn.commit()
                user.id = cursor.lastrowid
                return user.id

            # Update
            conn.execute(
                "UPDATE user SET full_name=?, email=?, password=?, phone=? WHERE id=?",
                (user.full_name, user.email, user.password, user.phone, user.id),
            )
            conn.commit()
            return user.id
