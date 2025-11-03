from datetime import datetime

from app.components.frame import Frame
from app.components.scrollable_frame import ScrollableFrame
from app.components.text import Text
from app.database.models import Booking
from app.pages.user_bookings.components.booking_card import BookingCard


class DefaultView(Frame):
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
