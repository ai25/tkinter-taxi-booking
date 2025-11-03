from app.components.frame import Frame
from app.components.hr import HorizontalRule
from app.components.icon import Icon, Resize
from app.components.text import Text
from app.state import AppState
from app.style import Theme


class Summary(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        Text(self, "lg", text="Summary").pack(anchor="nw")

        HorizontalRule(self).pack(fill="both", pady=5)

        pick_up_container = Frame(self)
        Icon(pick_up_container, "app/icons/FiMapPin.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(pick_up_container, "xs", text="Pick up:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.pick_up = Text(pick_up_container, "sm", text=AppState.booking.pick_up_location)
        self.pick_up.grid(
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
        self.drop_off = Text(drop_off_container, "sm", text=AppState.booking.drop_off_location)
        self.drop_off.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        drop_off_container.pack(anchor="nw")

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
        self.date = Text(date_container, "sm", text="N/A")
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
        self.vehicle = Text(vehicle_container, "sm", text="N/A")
        self.vehicle.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        vehicle_container.grid(row=0, column=1, padx=10)

        payment_type_container = Frame(grid)
        Icon(payment_type_container, "app/icons/AiOutlinePound.svg", resize=Resize(20, 20), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(payment_type_container, "xs", text="Payment:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.payment_type = Text(payment_type_container, "sm", text="N/A")
        self.payment_type.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        payment_type_container.grid(row=0, column=2)

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
        self.message = Text(message_container, "sm", text="N/A", wraplength=550, anchor="w", justify="left")
        self.message.grid(
            row=1,
            column=1,
            sticky="ew",
        )
        message_container.pack(anchor="nw")
