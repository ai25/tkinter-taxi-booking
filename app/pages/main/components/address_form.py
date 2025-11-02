from types import SimpleNamespace

from app.components.button import Button
from app.components.frame import Frame
from app.components.text import Text
from app.components.validated_input import ValidatedInput
from app.state import AppState
from app.utils.faker import Fake
from app.utils.validator import Validator


class AddressForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()
        if AppState.booking.pick_up_location:
            self.pick_up.set(AppState.booking.pick_up_location, propagate=False)  # we want to avoid infinite loop
        if AppState.booking.drop_off_location:
            self.drop_off.set(AppState.booking.drop_off_location, propagate=False)

    def on_change(self, cb):
        self.pick_up.on_change(cb)
        self.drop_off.on_change(cb)

    def values(self):
        return SimpleNamespace(email=self.pick_up.get(), password=self.drop_off.get())

    def is_valid(self):
        pick_up_valid, _ = Validator.is_empty(self.pick_up.get())
        drop_off_valid, _ = Validator.is_empty(self.drop_off.get())
        return pick_up_valid and drop_off_valid

    def _build_ui(self):
        container = Frame(self)

        Text(container, "input_label", text="Pick Up").pack(anchor="w")
        self.pick_up = ValidatedInput(
            container,
            "Enter your pick up address",
            50,
            "app/icons/FiMapPin.svg",
            validator=lambda v: Validator.is_empty(v, "Pick up location"),
        )
        self.pick_up.pack(pady=(5, 15))

        self.pick_up.on_change(lambda e: AppState.booking.update({"pick_up_location": self.pick_up.get()}))

        Text(container, "input_label", text="Drop Off").pack(anchor="w")
        self.drop_off = ValidatedInput(
            container,
            "Enter your destination",
            50,
            "app/icons/BiSolidMapPin.svg",
            validator=lambda v: Validator.is_empty(v, "Drop off location"),
        )
        self.drop_off.pack(pady=(5, 15))

        self.drop_off.on_change(lambda e: AppState.booking.update({"drop_off_location": self.drop_off.get()}))

        self.autofill_button = Button(
            container,
            text="Autofill",
            variant="ghost",
            command=self._autofill,
        )
        self.autofill_button.pack(pady=(0, 10))

        container.pack()

    def _autofill(self):
        booking = Fake().booking()
        self.pick_up.set(booking.pick_up_location)
        self.drop_off.set(booking.drop_off_location)
