from app.database.models import User
from faker import Faker


class Fake:
    def __init__(self) -> None:
        self.fake = Faker("en_GB")

    def user(self, role):
        return User(None, role, self.fake.name(), self.fake.email(), "12345678", self.fake.phone_number(), None)
