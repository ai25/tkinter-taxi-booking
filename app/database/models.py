from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class User:
    id: int | None
    role: str
    full_name: str
    email: str
    password: str
    phone: str | None
    session_token: str | None
    created_at: int  # Unix timestamp


@dataclass
class PaymentMethod:
    card_name: str
    card_number: str
    exp_month: int
    exp_year: int
    security_code: int
    id: int | None = None
    user_id: int | None = None


@dataclass
class Booking:
    pick_up_location: str
    drop_off_location: str
    pick_up_time: int
    vehicle: str
    fare: int
    payment_type: str
    paid: int
    cancelled: int
    user_id: int
    id: int | None = None
    message: str | None = None
    assigned_driver_id: int | None = None

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled == 1

    @property
    def is_completed(self) -> bool:
        return self.pick_up_time < int(datetime.now().timestamp())

    @property
    def is_paid(self) -> bool:
        return self.paid == 1

    @property
    def fare_pounds(self) -> float:
        return self.fare / 100.0

    @property
    def subtotal_pounds(self) -> float:
        return (self.fare - (self.fare * 0.2)) / 100.0

    @property
    def vat_pounds(self) -> float:
        return (self.fare * 0.2) / 100.0


@dataclass
class PartialBooking:
    pick_up_location: str | None = None
    drop_off_location: str | None = None
    pick_up_time: int | None = None
    vehicle: str | None = None
    fare: int | None = None
    payment_type: str | None = None
    paid: int | None = None
    cancelled: int | None = None
    user_id: int | None = None
    id: int | None = None
    message: str | None = None
    assigned_driver_id: int | None = None

    def is_valid(self) -> bool:
        return all(
            [
                self.pick_up_location is not None,
                self.drop_off_location is not None,
                self.pick_up_time is not None,
                self.vehicle is not None,
                self.fare is not None,
                self.payment_type is not None,
                self.paid is not None,
                self.cancelled is not None,
                self.user_id is not None,
            ]
        )

    def update(self, values: dict[str, Any]) -> None:
        for key, value in values.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"PartialBooking has no attribute '{key}'")
