from datetime import time
from types import SimpleNamespace

from app.components.button import Button
from app.components.date_picker import DatePicker
from app.components.frame import Frame
from app.components.hr import HorizontalRule
from app.components.text import Text
from app.components.time_picker import TimePicker
from app.components.validated_input import ValidatedInput
from app.pages.booking.components.payment_type_radio import PaymentTypeRadio
from app.pages.booking.components.vehicles_radio import VehiclesRadio
from app.state import AppState
from app.style import Theme
from app.utils.faker import Fake
from app.utils.validator import Validator


class PaymentForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()
        # if AppState.booking.pick_up_location:
        #     self.pick_up.set(AppState.booking.pick_up_location, propagate=False)  # we want to avoid infinite loop
        # if AppState.booking.drop_off_location:
        #     self.drop_off.set(AppState.booking.drop_off_location, propagate=False)

    def on_change(self, cb):
        self.name.on_change(cb)
        self.card.on_change(cb)
        self.expiry_month.on_change(cb)
        self.expiry_year.on_change(cb)
        self.security_code.on_change(cb)

    def values(self):
        return None
        # return SimpleNamespace(
        #     date=self.date.get(), time=self.time.get(), vehicle=self.vehicle.get(), payment_type=self.payment_type.get()
        # )

    def is_valid(self):
        return True

    def _build_ui(self):
        Text(self, "lg", text="Payment").pack(anchor="nw", pady=(10, 0))

        HorizontalRule(self).pack(fill="both", pady=5)

        Text(self, "input_label", text="Name on card").pack(anchor="w", pady=5)
        self.name = ValidatedInput(
            self,
            "Enter your name",
            50,
            "app/icons/FaSolidUser.svg",
            validator=lambda e: Validator.is_empty(self.name.get(), "Name"),
        )
        self.name.pack(anchor="nw")

        Text(self, "input_label", text="Card number").pack(anchor="w", pady=5)
        self.card = ValidatedInput(
            self,
            "Enter your card number",
            50,
            "app/icons/FaRegularCreditCard.svg",
            validator=lambda e: Validator.validate_card(
                self.card.get(),
            ),
        )
        self.card.pack(anchor="nw")

        exp_sec = Frame(self)
        expiry_container = Frame(exp_sec, width=20)

        Text(expiry_container, "input_label", text="Expiry date").pack(anchor="w", pady=5)
        self.expiry_month = ValidatedInput(
            expiry_container,
            placeholder="MM",
            icon="app/icons/FaRegularCalendar.svg",
            width=6,
        )
        self.expiry_month.pack(side="left")
        self.expiry_year = ValidatedInput(
            expiry_container,
            placeholder="YY",
            width=6,
            height=80,
        )
        self.expiry_year.pack(side="left", anchor="s")
        expiry_container.pack(side="left", padx=(0, 10))

        security_container = Frame(exp_sec, width=20)
        Text(security_container, "input_label", text="Expiry date").pack(anchor="w", pady=5)
        self.security_code = ValidatedInput(
            security_container,
            placeholder="xxx",
            icon="app/icons/FaSolidAsterisk.svg",
            width=7,
        )
        self.security_code.pack()
        security_container.pack(side="left")

        exp_sec.pack(anchor="nw")
        error_container = Frame(self)
        self.exp_error = Text(error_container, "xs", text="", fg=Theme.ERROR)
        self.exp_error.grid(row=0, column=0)
        self.sec_error = Text(error_container, "xs", text="", fg=Theme.ERROR)
        self.sec_error.grid(row=0, column=1)
        error_container.pack(
            anchor="nw",
        )
        self.expiry_year.on_change(self._validate_card_expiry)
        self.security_code.on_change(self._validate_security_code)

    def _validate_card_expiry(self, event=None):
        self.exp_error.configure(text="")
        _, error = Validator.validate_card_expiry(
            self.expiry_month.get(),
            self.expiry_year.get(),
        )
        if error:
            self.exp_error.configure(text=error)

    def _validate_security_code(self, event=None):
        self.sec_error.configure(text="")
        _, error = Validator.validate_security_code(self.security_code.get())
        if error:
            self.sec_error.configure(text=error)

    def _autofill(self):
        booking = Fake().booking()
        # self.pick_up.set(booking.pick_up_location)
        # self.drop_off.set(booking.drop_off_location)
