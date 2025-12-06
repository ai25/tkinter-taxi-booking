from app.components.frame import Frame
from app.components.hr import HorizontalRule
from app.components.icon import Icon, Resize
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.style import Theme
from app.utils.datetime import format_timestamp


class Summary(Frame):
    def __init__(self, parent, booking: Booking, **kwargs):
        super().__init__(parent, **kwargs)

        pick_up_container = Frame(self)
        Icon(pick_up_container, "app/icons/FiMapPin.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(pick_up_container, "xs", text="Pick up:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        Text(pick_up_container, "sm", text=booking.pick_up_location).grid(
            row=1,
            column=1,
            sticky="nw",
        )
        pick_up_container.pack(anchor="nw")

        drop_off_container = Frame(self)
        Icon(drop_off_container, "app/icons/BiSolidMapPin.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(drop_off_container, "xs", text="Drop off:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        Text(drop_off_container, "sm", text=booking.drop_off_location).grid(
            row=1,
            column=1,
            sticky="nw",
        )
        drop_off_container.pack(anchor="nw")

        HorizontalRule(self).pack(fill="both", pady=(15, 5))

        grid = Frame(self)

        date_container = Frame(grid)
        Icon(date_container, "app/icons/FaRegularCalendar.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(date_container, "xs", text="Pick up time", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.date = Text(date_container, "sm", text=format_timestamp(booking.pick_up_time))
        self.date.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        date_container.grid(row=0, column=0)

        vehicle_container = Frame(grid)
        Icon(vehicle_container, "app/icons/AiOutlineCar.svg", resize=Resize(20, 20), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(vehicle_container, "xs", text="Vehicle:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.vehicle = Text(vehicle_container, "sm", text=booking.vehicle.capitalize())
        self.vehicle.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        vehicle_container.grid(row=0, column=2, padx=10)

        grid.pack(anchor="nw")

        message_container = Frame(self)
        Icon(message_container, "app/icons/FiMessageSquare.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(message_container, "xs", text="Message:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.message = Text(
            message_container,
            "sm",
            text=booking.message if booking.message else "N/A",
            wraplength=550,
            anchor="w",
            justify="left",
        )
        self.message.grid(
            row=1,
            column=1,
            sticky="ew",
        )
        message_container.pack(anchor="nw")

        HorizontalRule(self).pack(fill="both", pady=(15, 5))

        driver_container = Frame(self)
        Icon(driver_container, "app/icons/FaSolidUser.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(driver_container, "xs", text="Driver:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        assigned_driver = Text(
            driver_container,
            "sm",
            text="N/A",
            wraplength=550,
            anchor="w",
            justify="left",
        )
        assigned_driver.grid(
            row=1,
            column=1,
            sticky="ew",
        )
        driver_container.pack(anchor="nw")

        bottom = Frame(self)
        pricing_container = Frame(bottom)
        subtotal = Text(pricing_container, "sm", text=f"£{booking.subtotal_pounds:.2f}")
        vat = Text(pricing_container, "sm", text=f"£{booking.vat_pounds:.2f}") 
        total = Text(pricing_container, "lg", text=f"£{booking.fare_pounds:.2f}") 
        Text(pricing_container, "sm", text="Subtotal:").grid(row=0, column=0, sticky="w")
        Text(pricing_container, "sm", text="VAT (20%):").grid(row=1, column=0, sticky="w")
        Text(pricing_container, "lg", text="Total:").grid(row=2, column=0, sticky="w")

        subtotal.grid(row=0, column=1, sticky="e")
        vat.grid(row=1, column=1, sticky="e")
        total.grid(row=2, column=1, sticky="e")
        pricing_container.grid_columnconfigure(0, weight=1)
        pricing_container.pack(anchor="nw", fill="x")

        bottom.pack(anchor="s", fill="x", expand=True)

        if driver_id := booking.assigned_driver_id:
            driver, _ = Database().user.get_by_id(driver_id)
            if driver:
                assigned_driver.configure(text=driver.full_name)
