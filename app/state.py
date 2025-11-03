from app.database.models import Booking, PartialBooking, PaymentMethod, User


class AppState:
    user: User | None = None
    booking: PartialBooking = PartialBooking()
