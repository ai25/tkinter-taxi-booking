import random
from dataclasses import dataclass


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

    def send_email(self, template, to):
        match template:
            case "WELCOME":
                subject = "Thank you for signing up!"
                content = "..."
                self._send_email(to, subject, content)
            case "BOOKING_CONFIRMED":
                subject = "Thank you for booking with us!"
                content = "..."
                self._send_email(to, subject, content)

    def _send_email(self, to, subject, content):
        # use an api such as SendGrid to send the email
        pass
