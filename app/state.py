from app.database.models import Booking, PartialBooking, PaymentMethod, User


class ExtendedUser(User):
    payment_methods: list[PaymentMethod] = []


class AppState:
    user: ExtendedUser | None = None
    booking: PartialBooking = PartialBooking()
