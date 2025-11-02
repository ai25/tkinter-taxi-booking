from app.api import MockApi
from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.icon import Icon
from app.components.scrollable_frame import ScrollableFrame
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.frame_controller import FrameController
from app.pages.booking.components.booking_form import BookingForm
from app.pages.booking.components.payment_form import PaymentForm
from app.pages.booking.components.summary import Summary
from app.state import AppState
from app.style import StyleManager, Theme
from app.utils.datetime import format_datetime, format_timestamp, timestamp_to_datetime, to_timestamp


class UserBookingPage(Frame):
    def __init__(self, parent, params):
        super().__init__(parent)
        print(params["id"])
        self.db = Database()
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")
        self.error = ""
        if AppState.user.role == "USER":
            self.bookings, self.error = self.db.booking.get_by_user(AppState.user.id)
        elif AppState.user.role == "DRIVER":
            self.bookings, self.error = self.db.booking.get_by_driver(AppState.user.id)
        elif AppState.user.role == "ADMIN":
            self.bookings, self.error = self.db.booking.get_all()

        container = Frame(self)
        Text(container, "lg", text=self.error, fg=Theme.ERROR).pack()

        # view = NormalView(container, self.bookings)
        # if len(self.bookings) == 0:
        #     view = EmptyView(container)

        # view.pack(fill="both", expand=True)

        container.pack(fill="both", expand=True)
