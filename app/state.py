from app.database.models import User


class AppState:
    user: User | None = None
