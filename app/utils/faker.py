from app.database.models import Booking, PartialBooking, User
from faker import Faker

from app.state import AppState


class Fake:
    def __init__(self) -> None:
        self.fake = Faker("en_GB")
        print()

    def user(self, role):
        return User(None, role, self.fake.name(), self.fake.email(), "12345678", self.fake.phone_number(), None, None)

    def booking(self):
        return PartialBooking(
            self.fake.address().replace("\n", ", "),
            self.fake.address().replace("\n", ", "),
            int(self.fake.date_time_this_month(before_now=False).timestamp()),
            "SALOON",
            None,
            None,
            0,
            0,
            AppState.user.id,
            None,
            None,
        )
