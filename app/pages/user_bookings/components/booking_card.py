from app.components.frame import Frame
from app.components.icon import Icon
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.frame_controller import FrameController
from app.style import StyleManager, Theme
from app.utils.datetime import format_timestamp


class BookingCard(Frame):
    def __init__(self, parent, booking: Booking, **kwargs):
        super().__init__(parent, **kwargs)
        StyleManager.apply(self, "booking_card")
        self.grid_columnconfigure(0, weight=1)

        content = Frame(self)
        content.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)

        id = Text(content, "md", text=f"ID: {booking.id}")
        id.grid(row=0, column=0, sticky="w", pady=(0, 10))

        cancelled = Text(content, "md", text="", fg=Theme.ERROR)
        cancelled.grid(row=0, column=3, sticky="e")

        pick_up = Text(content, "md", text=booking.pick_up_location, icon="app/icons/FiMapPin.svg")
        pick_up.grid(row=1, column=0, sticky="w")

        drop_off = Text(content, "md", text=booking.drop_off_location, icon="app/icons/BiSolidMapPin.svg")
        drop_off.grid(row=2, column=0, sticky="w", ipady=10)

        info_container = Frame(content, bg=content["bg"])
        date = Text(
            info_container, "md", text=format_timestamp(booking.pick_up_time), icon="app/icons/FaRegularCalendar.svg"
        )
        date.pack(side="left", anchor="w")

        vehicle = Text(info_container, "md", text=booking.vehicle.capitalize(), icon="app/icons/AiOutlineCar.svg")
        vehicle.pack(side="left", anchor="w", padx=10)

        assigned_driver = Text(info_container, "md", text="Not assigned", icon="app/icons/FaSolidUser.svg")
        assigned_driver.pack(side="left", anchor="w")

        info_container.grid(row=3, column=0, sticky="w")

        icon = Icon(self, "app/icons/FaSolidChevronRight.svg")
        icon.grid(row=0, column=1, sticky="e")

        if booking.is_cancelled:
            cancelled.configure(text="Cancelled")

        if driver_id := booking.assigned_driver_id:
            driver, _ = Database().user.get_by_id(driver_id)
            if driver:
                assigned_driver.configure(text=driver.full_name)

        widgets = [
            self,
            content,
            id,
            cancelled,
            pick_up,
            drop_off,
            info_container,
            date,
            vehicle,
            assigned_driver,
            icon,
        ]

        for widget in widgets:
            widget.bind("<Button-1>", lambda e: FrameController.get().show_frame("UserBookingPage", {"id": booking.id}))
            widget.configure(cursor="hand2")
