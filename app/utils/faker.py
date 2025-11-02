from types import SimpleNamespace

from faker import Faker

from app.database.models import PartialBooking, User
from app.state import AppState


class Fake:
    def __init__(self) -> None:
        self.fake = Faker("en_GB")

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

    def card(self):
        return SimpleNamespace(
            name=self.fake.name(),
            card=self.fake.credit_card_number(),
            expiry_month=self.fake.credit_card_expire().split("/")[0],
            expiry_year=self.fake.credit_card_expire().split("/")[1],
            security_code=self.fake.credit_card_security_code(),
        )
