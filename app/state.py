from app.models import User


class AppState:
    user: User | None = None
