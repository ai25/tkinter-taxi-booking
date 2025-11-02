from datetime import datetime

from app.components.frame import Frame
from app.components.header import Header
from app.components.scrollable_frame import ScrollableFrame
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.pages.user_bookings.components.booking_card import BookingCard
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

        view = NormalView(container, self.bookings)
        if len(self.bookings) == 0:
            view = EmptyView(container)

        view.pack(fill="both", expand=True)

        container.pack(fill="both", expand=True)


class NormalView(Frame):
    def __init__(self, parent, bookings: list[Booking], **kwargs):
        super().__init__(parent, **kwargs)
        container = ScrollableFrame(self)
        bookings_container = Frame(container.interior)

        upcoming = [b for b in bookings if int(datetime.now().timestamp()) <= b.pick_up_time]
        past = [b for b in bookings if int(datetime.now().timestamp()) > b.pick_up_time]

        row = 0

        if upcoming:
            Text(bookings_container, "lg", text="Upcoming").grid(row=row, column=0, sticky="w", pady=(0, 10))
            row += 1
            for booking in upcoming:
                BookingCard(bookings_container, booking).grid(row=row, column=0, sticky="ew", pady=(0, 5))
                row += 1

        if past:
            Text(bookings_container, "lg", text="Past").grid(row=row, column=0, sticky="w", pady=(20, 10))
            row += 1
            for booking in past:
                BookingCard(bookings_container, booking).grid(row=row, column=0, sticky="ew", pady=(0, 5))
                row += 1

        bookings_container.grid_columnconfigure(0, minsize=800)
        bookings_container.pack()
        container.pack(fill="both", expand=True)


class EmptyView(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        Text(self, "lg", text="No bookings found.").pack()
