import tkinter as tk
from types import SimpleNamespace

from app.components.button import Button
from app.components.frame import Frame
from app.components.radiobutton import RadioButton
from app.components.text import Text
from app.components.validated_input import ValidatedInput
from app.utils.faker import Fake
from app.utils.validator import Validator


class SignUpForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def on_change(self, cb):
        self.full_name.on_change(cb)
        self.email.on_change(cb)
        self.phone.on_change(cb)
        self.password.on_change(cb)
        self.repeat_password.on_change(cb)

    def values(self):
        return SimpleNamespace(
            role=self.selected_role.get(),
            full_name=self.full_name.get(),
            email=self.email.get(),
            password=self.password.get(),
            phone=self.phone.get(),
        )

    def is_valid(self):
        full_name_valid, _ = Validator.validate_full_name(self.full_name.get())
        email_valid, _ = Validator.validate_email(self.email.get())
        password_valid, _ = Validator.validate_password(self.password.get())
        repeat_password_valid, _ = Validator.validate_repeat_password(self.repeat_password.get(), self.password.get())
        return full_name_valid and email_valid and password_valid and repeat_password_valid

    def _build_ui(self):
        container = Frame(self)

        radio = Frame(container)
        radio.pack(pady=10)

        self.selected_role = tk.StringVar(value="USER")
        for role in ["USER", "DRIVER", "ADMIN"]:
            RadioButton(radio, text=role.capitalize(), variable=self.selected_role, value=role).pack(
                side="left", padx=5
            )

        Text(container, "input_label", text="Full Name").pack(anchor="w")
        self.full_name = ValidatedInput(
            container, "Enter your full name", 50, "app/icons/FaSolidUser.svg", Validator.validate_full_name
        )
        self.full_name.pack(pady=(5, 15))

        Text(container, "input_label", text="Email Address").pack(anchor="w")
        self.email = ValidatedInput(
            container, "Enter your email address", 50, "app/icons/SiMaildotru.svg", Validator.validate_email
        )
        self.email.pack(pady=(5, 15))

        Text(container, "input_label", text="Phone (optional)").pack(anchor="w")
        self.phone = ValidatedInput(container, "Enter your phone number", 50, "app/icons/FaSolidPhone.svg")
        self.phone.pack(pady=(5, 15))

        Text(container, "input_label", text="Password").pack(anchor="w")
        self.password = ValidatedInput(
            container,
            "Enter your password",
            50,
            "app/icons/FaSolidAsterisk.svg",
            Validator.validate_password,
            type="password",
        )
        self.password.pack(pady=(5, 15))

        Text(container, "input_label", text="Repeat Password").pack(anchor="w")
        self.repeat_password = ValidatedInput(
            container,
            "Enter your password again",
            50,
            "app/icons/FaSolidAsterisk.svg",
            lambda value: Validator.validate_repeat_password(value, self.password.get()),
            type="password",
        )
        self.repeat_password.pack(pady=(5, 15))

        container.pack()

        self.autofill_button = Button(
            container,
            text="Autofill",
            variant="ghost",
            command=self._autofill,
        )
        self.autofill_button.pack(pady=(0, 10))

    def _autofill(self):
        user = Fake().user("USER")
        self.full_name.set(user.full_name)
        self.email.set(user.email)
        self.phone.set(user.phone)
        self.password.set(user.password)
        self.password.should_show_password()
        self.repeat_password.set(user.password)
        self.repeat_password.should_show_password()
        # self.master.master.master.update_button_state()  # type: ignore
