import random
from dataclasses import dataclass
from typing import Literal

from app.database.db import Database
from app.database.models import Booking


PRICE_PER_MILE_PENCE = 250  # £2.50
MPV_MULTIPLIER = 1.2
MINIBUS_MULTIPLIER = 1.6


@dataclass
class MockApi:
    def get_route_fare(self, pick_up, drop_off, vehicle):
        distance = self._get_distance(pick_up, drop_off)
        multiplier = 1
        if vehicle == "MPV":
            multiplier = MPV_MULTIPLIER
        elif vehicle == "MINIBUS":
            multiplier = MINIBUS_MULTIPLIER

        subtotal = int(distance * PRICE_PER_MILE_PENCE * multiplier)
        vat = int(subtotal * 0.2)  # 20%
        return {"distance": distance, "subtotal": subtotal, "vat": vat, "total": subtotal + vat}

    def _get_distance(self, pick_up, drop_off):  # noqa: ARG002
        return random.randrange(1, 1000, 1) / 10  # 0.1 -> 100 miles

    def processs_payment(self, payment_details):  # noqa: ARG002
        return random.random() > 0.001  # 0.1% chance of failure

    def send_email(
        self,
        template: Literal[
            "WELCOME",
            "BOOKING_CONFIRMED",
            "BOOKING_CREATED_ADMIN",
            "DRIVER_ASSIGNED",
            "TRIP_EDITED_USER",
            "TRIP_EDITED_DRIVER",
            "TRIP_CANCELLED_USER",
            "TRIP_CANCELLED_DRIVER",
        ],
        to=None,
    ):
        db = Database()
        match template:
            case "WELCOME":
                subject = "Thank you for signing up!"
                content = "..."
                self._send_email(to, subject, content)
            case "BOOKING_CONFIRMED":
                subject = "Thank you for booking with us!"
                content = "..."
                self._send_email(to, subject, content)
            case "BOOKING_CREATED_ADMIN":
                subject = "You have a new booking"
                content = "..."
                admins, _ = db.user.get_by_role("ADMIN")
                for admin in admins:
                    self._send_email(admin.email, subject, content)
            case "DRIVER_ASSIGNED":
                subject = "You have been assigned a new trip"
                content = "..."
                self._send_email(to, subject, content)
            case "TRIP_EDITED_USER":
                subject = "Your trip details have changed"
                content = "..."
                self._send_email(to, subject, content)
            case "TRIP_EDITED_DRIVER":
                subject = "A trip you are assigned to has changed"
                content = "..."
                self._send_email(to, subject, content)
            case "TRIP_CANCELLED_USER":
                subject = "Your booking has been cancelled"
                content = "..."
                self._send_email(to, subject, content)
            case "TRIP_CANCELLED_DRIVER":
                subject = "A trip you are assigned to has been cancelled"
                content = "..."
                self._send_email(to, subject, content)

    def _send_email(self, to, subject, content):
        # use an api such as SendGrid to send the email
        pass

    def process_refund(self, payment_method_id: int):
        pm = Database().payment_method.get_by_id(payment_method_id)
        print("Refunded payment method: ", pm)
