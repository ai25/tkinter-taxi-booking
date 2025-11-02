import sqlite3
from typing import TYPE_CHECKING

from app.database.models import Booking, PartialBooking


if TYPE_CHECKING:
    from app.database.db import Database


class BookingQueries:
    def __init__(self, db: "Database"):
        self.db = db

    def get_by_id(self, booking_id: int):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM booking WHERE id = ?", (booking_id,))
                row = cursor.fetchone()
                return (Booking(**dict(row)), None) if row else (None, "Booking not found")
        except sqlite3.Error as e:
            return (None, str(e))

    def get_by_user(self, user_id: int):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM booking WHERE user_id = ? ORDER BY pick_up_time DESC", (user_id,))
                return ([Booking(**dict(row)) for row in cursor.fetchall()], None)
        except sqlite3.Error as e:
            return (None, str(e))

    def get_by_driver(self, driver_id: int):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM booking WHERE assigned_driver_id = ? ORDER BY pick_up_time DESC", (driver_id,)
                )
                return ([Booking(**dict(row)) for row in cursor.fetchall()], None)
        except sqlite3.Error as e:
            return (None, str(e))

    def get_all(self):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM booking ORDER BY pick_up_time DESC")
                return ([Booking(**dict(row)) for row in cursor.fetchall()], None)
        except sqlite3.Error as e:
            return (None, str(e))

    def create(self, booking: Booking | PartialBooking):
        try:
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO booking(pick_up_location, drop_off_location, pick_up_time, 
                    vehicle, message, payment_type, paid, fare, user_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        booking.pick_up_location,
                        booking.drop_off_location,
                        booking.pick_up_time,
                        booking.vehicle,
                        booking.message,
                        booking.payment_type,
                        booking.paid or 0,
                        booking.fare,
                        booking.user_id,
                    ),
                )
                conn.commit()
                return (cursor.lastrowid, "")
        except sqlite3.Error as e:
            return (None, str(e))
