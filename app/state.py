from app.database.models import Booking, PartialBooking, User


class AppState:
    user: User | None = None
    booking: PartialBooking = PartialBooking()
