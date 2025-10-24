from types import SimpleNamespace

from app.components import Button, Frame, Img, SplitFrame, Text, ValidatedInput
from app.controllers import FrameController
from app.models import User
from app.repositories.user_repository import UserRepository
from app.state import AppState
from app.utils.faker import Fake
from app.utils.frame_registry import page
from app.utils.validator import Validator


@page("SignUpPage")
class SignUpPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)
        header = Text(self.split_frame.left, "h3", text="Logo")
        header.pack(anchor="nw", padx=0, pady=20)
        self.form = SignUpForm(self.split_frame.left)
        self.form.pack()

        self.split_frame.right = Img(self.split_frame, "app/images/blurred_light_bg.jpg")
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

        self.signup_button = Button(self.split_frame.left, text="Sign Up", state="disabled", command=self.sign_up)
        self.signup_button.pack()
        self.form.on_change(self.update_button_state)

    def sign_up(self):
        if not self.form.is_valid():
            return
        values = self.form.values()
        user = User(None, "USER", values.full_name, values.email, values.password, values.phone, None)
        user_repo = UserRepository()
        id = user_repo.upsert(user)
        if id:
            AppState.user = user
            FrameController.get().show_frame("MainPage")

    def update_button_state(self, event=None):
        self.signup_button.config(state="normal" if self.form.is_valid() else "disabled")


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
            full_name=self.full_name.get(), email=self.email.get(), password=self.password.get(), phone=self.phone.get()
        )

    def is_valid(self):
        full_name_valid, _ = Validator().validate_full_name(self.full_name.get())
        email_valid, _ = Validator().validate_email(self.email.get())
        return full_name_valid and email_valid

    def _build_ui(self):
        container = Frame(self)

        Text(container, "input_label", text="Full Name").pack(anchor="w")
        self.full_name = ValidatedInput(
            container, "Enter your full name", 50, "app/icons/FaSolidUser.svg", Validator().validate_full_name
        )
        self.full_name.pack(pady=(5, 15))

        Text(container, "input_label", text="Email Address").pack(anchor="w")
        self.email = ValidatedInput(
            container, "Enter your email address", 50, "app/icons/SiMaildotru.svg", Validator().validate_email
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
            Validator().validate_password,
            type="password",
            validate_event="<KeyRelease>",
        )
        self.password.pack(pady=(5, 15))

        Text(container, "input_label", text="Repeat Password").pack(anchor="w")
        self.repeat_password = ValidatedInput(
            container,
            "Enter your password again",
            50,
            "app/icons/FaSolidAsterisk.svg",
            lambda value: Validator().validate_repeat_password(value, self.password.get()),
            type="password",
            validate_event="<KeyRelease>",
        )
        self.repeat_password.pack(pady=(5, 15))

        container.pack()

        self.autofill_button = Button(
            container,
            text="Autofill",
            variant="ghost",
            command=self._autofill,
        )
        self.autofill_button.pack()

    def _autofill(self):
        user = Fake().user("USER")
        self.full_name.set(user.full_name)
        self.email.set(user.email)
        self.phone.set(user.phone)
        self.password.set(user.password)
        self.password.should_show_password()
        self.repeat_password.set(user.password)
        self.repeat_password.should_show_password()
        self.master.master.master.update_button_state()  # type: ignore
