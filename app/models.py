from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    full_name: str
    email: str
    password: str
    phone: str | None
    created_at: int  # Unix timestamp


@dataclass
class Driver:
    id: int | None
    full_name: str
    email: str
    password: str
    phone: str | None
    created_at: int


@dataclass
class Admin:
    id: int | None
    full_name: str
    email: str
    password: str
    created_at: int


@dataclass
class Booking:
    id: int | None
    pick_up_location: str
    drop_off_location: str
    pick_up_time: int  # Unix timestamp
    vehicle: str
    passengers: int
    message: str | None
    fare: int  # Pence
    cancelled: int  # 0 or 1 (boolean)
    assigned_driver_id: int | None
    user_id: int

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled == 1

    @property
    def fare_pounds(self) -> float:
        return self.fare / 100.0
