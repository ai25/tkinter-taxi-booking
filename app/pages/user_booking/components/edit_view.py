from dataclasses import asdict
from datetime import datetime
from app.api import MockApi
from app.components.button import Button
from app.components.date_picker import DatePicker
from app.components.frame import Frame
from app.components.header import Header
from app.components.hr import HorizontalRule
from app.components.scrollable_frame import ScrollableFrame
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.components.textbox import Textbox
from app.components.time_picker import TimePicker
from app.components.validated_input import ValidatedInput
from app.database.db import Database
from app.database.models import Booking, PaymentMethod
from app.frame_controller import FrameController
from app.pages.booking.components.booking_form import BookingForm, VehiclesRadio
from app.pages.booking.components.payment_form import PaymentForm
from app.pages.booking.components.payment_method_radio import PaymentMethodRadio
from app.pages.booking.components.summary import Summary
from app.state import AppState
from app.style import Theme
from app.utils.datetime import format_datetime, timestamp_to_datetime, to_timestamp
from app.utils.validator import Validator
from copy import copy


class EditView(Frame):
    def __init__(self, parent, booking: Booking, switch_view):
        super().__init__(parent)
        self.initial_booking = copy(booking)  # shallow copy so that the inital values don't get modified
        self.booking = copy(booking)  # working state needs to be copied as well

        self.switch_view = switch_view
        self._build_ui()

        self.pick_up.set(booking.pick_up_location)
        self.on_booking_form_change("pick_up", booking.pick_up_location)
        self.pick_up.on_change(lambda e: self.on_booking_form_change("pick_up", self.pick_up.get()))
        self.pick_up.on_focus_out(lambda e: self.update_price())

        self.drop_off.set(booking.drop_off_location)
        self.on_booking_form_change("drop_off", booking.drop_off_location)
        self.drop_off.on_change(lambda e: self.on_booking_form_change("drop_off", self.drop_off.get()))
        self.drop_off.on_focus_out(lambda e: self.update_price())

        dt = datetime.fromtimestamp(float(booking.pick_up_time))
        self.date.set(dt)
        self.time.set(dt.hour, dt.minute)
        self.on_booking_form_change("date", dt)
        self.date.on_change(lambda e: self.on_booking_form_change("date", ""))
        self.time.on_change(lambda e: self.on_booking_form_change("time", ""))

        self.vehicle.select(booking.vehicle)
        self.on_booking_form_change("vehicle", booking.vehicle)
        self.vehicle.on_change(lambda: self.on_booking_form_change("vehicle", self.vehicle.get()))

        self.summary.payment_type.configure(text=booking.payment_type.capitalize())

        self.message.set(booking.message)
        self.on_booking_form_change("message", booking.message)
        self.message.on_change(lambda e: self.on_booking_form_change("message", self.message.get()))

    def _build_ui(self):
        self.split_frame = SplitFrame(self)
        self.split_frame.left = ScrollableFrame(self.split_frame)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=0)
        self.split_frame.columnconfigure(0, minsize=640)
        self.split_frame.columnconfigure(1, minsize=640)

        container = Frame(self.split_frame.left.interior)
        Text(container, "input_label", text="Pick Up").pack(anchor="w")
        self.pick_up = ValidatedInput(
            container,
            "Enter your pick up address",
            53,
            "app/icons/FiMapPin.svg",
            validator=lambda v: Validator.is_empty(v, "Pick up location"),
        )
        self.pick_up.pack(pady=(5, 15), anchor="w")

        Text(container, "input_label", text="Drop Off").pack(anchor="w")
        self.drop_off = ValidatedInput(
            container,
            "Enter your destination",
            53,
            "app/icons/BiSolidMapPin.svg",
            validator=lambda v: Validator.is_empty(v, "Drop off location"),
        )
        self.drop_off.pack(pady=(5, 15), anchor="w")

        date_time = Frame(container)
        date_container = Frame(date_time, width=35)
        self.date_title = Text(date_container, "sm", text="Pick Up Date:")
        self.date_title.pack(anchor="nw")
        self.date = DatePicker(date_container, icon="app/icons/FaRegularCalendar.svg", width=35)
        self.date.pack()
        time_container = Frame(date_time, width=35)

        Text(time_container, "sm", text="Pick Up Time:").pack(anchor="nw")
        self.time = TimePicker(time_container, icon="app/icons/FiClock.svg")
        self.time.pack()
        date_container.pack(side="left")
        time_container.pack(side="left", padx=10)

        date_time.pack(anchor="nw", pady=10)

        Text(container, "lg", text="Select your vehicle:").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(container).pack(fill="both", pady=(5, 10))

        self.vehicle = VehiclesRadio(container)
        self.vehicle.frame.pack(anchor="nw")

        Text(container, "lg", text="Special instructions:").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(container).pack(fill="both", pady=(5, 10))

        self.message = Textbox(container)
        self.message.pack(anchor="nw", pady=(0, 0))

        container.pack(padx=40, pady=0, fill="both")

        self.split_frame.right = Frame(self.split_frame)
        right_container = Frame(self.split_frame.right)

        self.summary = Summary(right_container)
        self.summary.pack(anchor="nw", fill="x")

        bottom = Frame(right_container)
        pricing_container_holder = Frame(bottom)
        self.pricing_container = Frame(pricing_container_holder)
        self.prev_total = Text(self.pricing_container, "sm", text="")
        self.new_total = Text(self.pricing_container, "sm", text="")
        self.difference = Text(self.pricing_container, "lg", text="")
        Text(self.pricing_container, "sm", text="Previous total:").grid(row=0, column=0, sticky="w")
        Text(self.pricing_container, "sm", text="New total:").grid(row=1, column=0, sticky="w")
        Text(self.pricing_container, "lg", text="Difference:").grid(row=2, column=0, sticky="w")

        self.prev_total.grid(row=0, column=1, sticky="e")
        self.new_total.grid(row=1, column=1, sticky="e")
        self.difference.grid(row=2, column=1, sticky="e")
        self.pricing_container.grid_columnconfigure(0, weight=1)

        Text(self.pricing_container, "xs", text="You will be charged/refunded on your original payment method.").grid(
            row=3, column=0, columnspan=2, pady=(10, 0)
        )
        pricing_container_holder.pack(fill="x")

        self.error_text = Text(bottom, "xs", text="", fg=Theme.ERROR)
        self.error_text.pack()

        self.cancel_button = Button(
            bottom, text="Cancel", command=lambda: self.switch_view(False), bg=Theme.ERROR, activebackground=Theme.ERROR
        )
        self.cancel_button.pack(fill="x", side="left", padx=10, expand=True)
        self.submit_button = Button(bottom, text="Save", command=self.submit)
        self.submit_button.pack(fill="x", side="left", expand=True)

        bottom.pack(anchor="s", fill="x", expand=True)
        right_container.pack(fill="both", expand=True, pady=20, padx=10)
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

    def on_booking_form_change(self, key, value):
        match key:
            case "pick_up":
                self.summary.pick_up.configure(text=value)
                self.booking.pick_up_location = value
            case "drop_off":
                self.summary.drop_off.configure(text=value)
                self.booking.drop_off_location = value
            case "date" | "time":
                self.summary.date.configure(text=format_datetime(self.date.get(), self.time.get()))
                self.booking.pick_up_time = to_timestamp(self.date.get(), self.time.get())
            case "vehicle":
                self.summary.vehicle.configure(text=value.capitalize())
                self.booking.vehicle = value
                self.update_price()

            case "message":
                self.summary.message.configure(text=value)
                self.booking.message = value

    def update_price(self):
        if (
            self.booking.pick_up_location == self.initial_booking.pick_up_location
            and self.booking.drop_off_location == self.initial_booking.drop_off_location
            and self.booking.vehicle == self.initial_booking.vehicle
        ):
            self.pricing_container.pack_forget()
            return

        fare = MockApi().get_route_fare(
            self.booking.pick_up_location, self.booking.drop_off_location, self.booking.vehicle
        )
        diff = fare["total"] - self.booking.fare
        self.prev_total.configure(text=f"£{self.booking.fare / 100}")
        self.new_total.configure(text=f"£{fare['total'] / 100}")
        self.difference.configure(text=f"£{diff / 100}")
        self.booking.fare = fare["total"]

        self.pricing_container.pack(anchor="nw", fill="x")

    def submit(self):
        self.error_text.configure(text="")
        db = Database()

        booking_id, err = db.booking.update(self.booking)

        if err:
            print(err)
            self.error_text.configure(text=err)
        else:
            print(booking_id)
            self.switch_view(True)
