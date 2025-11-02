from datetime import datetime, timedelta
from types import SimpleNamespace

from faker import Faker

from app.components.button import Button
from app.components.date_picker import DatePicker
from app.components.frame import Frame
from app.components.hr import HorizontalRule
from app.components.text import Text
from app.components.textbox import Textbox
from app.components.time_picker import TimePicker
from app.pages.booking.components.payment_type_radio import PaymentTypeRadio
from app.pages.booking.components.vehicles_radio import VehiclesRadio
from app.style import Theme
from app.utils.validator import Validator


class BookingForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def on_change(self, cb):
        self.date.on_change(lambda e: cb(key="date", value=self.date.get()))
        self.time.on_change(lambda e: cb(key="time", value=self.time.get()))
        self.vehicle.on_change(lambda: cb(key="vehicle", value=self.vehicle.get()))
        self.payment_type.on_change(lambda: cb(key="payment_type", value=self.payment_type.get()))
        self.message.on_change(lambda e: cb(key="message", value=self.message.get()))

    def values(self):
        return SimpleNamespace(
            date=self.date.get(),
            time=self.time.get(),
            vehicle=self.vehicle.get(),
            payment_type=self.payment_type.get(),
            message=self.message.get(),
        )

    def is_valid(self):
        datetime_valid, dt_error = Validator.validate_pickup_date(self.date.get(), self.time.get())
        vehicle_valid, _ = Validator.is_empty(self.vehicle.get())
        payment_type_valid, _ = Validator.is_empty(self.payment_type.get())

        if dt_error:
            self.date_title.configure(text=dt_error, fg=Theme.ERROR)
        else:
            self.date_title.configure(text="Pick Up Date:", fg=Theme.FOREGROUND)
        return datetime_valid and vehicle_valid and payment_type_valid

    def _build_ui(self):
        Text(self, "lg", text="When should we pick you up?").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(self).pack(fill="both", pady=(5, 0))

        date_time = Frame(self)
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

        Text(self, "lg", text="Select your vehicle:").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(self).pack(fill="both", pady=(5, 10))

        self.vehicle = VehiclesRadio(self)
        self.vehicle.frame.pack(anchor="nw")

        Text(self, "lg", text="Select your payment method:").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(self).pack(fill="both", pady=(5, 10))

        self.payment_type = PaymentTypeRadio(self)
        self.payment_type.pack(anchor="nw")

        Text(self, "lg", text="Special instructions:").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(self).pack(fill="both", pady=(5, 10))

        self.message = Textbox(self)
        self.message.pack(anchor="nw", pady=(0, 0))

        self.autofill_button = Button(
            self,
            text="Autofill",
            variant="ghost",
            command=self._autofill,
        )
        self.autofill_button.pack(pady=(0, 40))

    def set_init_date(self):
        dt = datetime.now() + timedelta(days=1)  # tomorrow
        self.date.set(dt)
        self.time.set(dt.hour, dt.minute)

    def _autofill(self):
        faker = Faker()
        self.set_init_date()
        self.vehicle.select("SALOON")
        self.payment_type.select("CARD")
        self.message.set(faker.text(max_nb_chars=120))
