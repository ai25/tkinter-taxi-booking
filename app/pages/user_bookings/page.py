from app.components.frame import Frame
from app.components.header import Header
from app.components.text import Text
from app.database.db import Database
from app.pages.user_bookings.components.default_view import DefaultView
from app.pages.user_bookings.components.empty_view import EmptyView
from app.state import AppState
from app.style import Theme


class UserBookingsPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")
        self.error = ""
        if AppState.user.role == "USER":
            Text(self, "h3", text="My Bookings").pack()
            self.bookings, self.error = self.db.booking.get_by_user(AppState.user.id)
        elif AppState.user.role == "DRIVER":
            Text(self, "h3", text="My Bookings").pack()
            self.bookings, self.error = self.db.booking.get_by_driver(AppState.user.id)
        elif AppState.user.role == "ADMIN":
            Text(self, "h3", text="All Bookings").pack()
            self.bookings, self.error = self.db.booking.get_all()

        container = Frame(self)
        Text(container, "lg", text=self.error, fg=Theme.ERROR).pack()

        view = DefaultView(container, self.bookings)
        if len(self.bookings) == 0:
            view = EmptyView(container)

        view.pack(fill="both", expand=True)

        container.pack(fill="both", expand=True)
