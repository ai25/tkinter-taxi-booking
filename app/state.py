from app.database.models import PartialBooking, User


class AppState:
    user: User | None = None
    booking: PartialBooking = PartialBooking()
