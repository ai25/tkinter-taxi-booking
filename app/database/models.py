from dataclasses import dataclass


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
class Booking:
    id: int | None
    pick_up_location: str
    drop_off_location: str
    pick_up_time: int  # Unix timestamp
    vehicle: str
    message: str | None
    fare: int  # Pence
    payment_type: str  # CASH | CARD
    paid: int  # 0 or 1 (boolean)
    cancelled: int  # 0 or 1 (boolean)
    assigned_driver_id: int | None
    user_id: int

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled == 1

    @property
    def is_paid(self) -> bool:
        return self.paid == 1

    @property
    def fare_pounds(self) -> float:
        return self.fare / 100.0
