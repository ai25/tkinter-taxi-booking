import tkinter as tk

from app.components import SplitFrame, Text, Frame, Button, Img, ValidatedInput
from app.controllers import FrameController
from app.state import AppState

from app.models import User
from app.repositories.user_repository import UserRepository


class SignUpPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)
        header = Text(self.split_frame.left, "h3", text="Logo")
        header.pack(anchor="nw", padx=0, pady=20)
        form = SignUpForm(self.split_frame.left)
        form.pack()

        # container = Frame(self.split_frame.left)
        # Text(container, text="Hello, Stranger!").pack()
        # Text(container, "h3", text="Let's get you started.").pack(pady=10)
        # buttons_container = Frame(container, pady=20)
        # Button(buttons_container, text="Login", command=lambda: FrameController.get().show_frame(SidePage)).grid(
        #     row=0, column=0, padx=10
        # )
        # Button(buttons_container, variant="secondary", text="Sign Up", command=self.sign_up).grid(row=0, column=1)
        # buttons_container.pack()
        # container.pack(pady=250)
        #
        self.split_frame.right = Img(self.split_frame, "app/images/blurred_light_bg.jpg")
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

    def sign_up(self):
        user = User(None, "Alin Imparatelu", "vvv@xd.dx", "1234", "1234", 1)
        user_repo = UserRepository()
        id = user_repo.upsert(user)
        print(id)


def validate_full_name(value):
    if len(value) < 4:
        return False, "Name is too short"
    return True, ""


def validate_email(value):
    if "@" not in value or "." not in value:
        return False, "Invalid email address"
    return True, ""


def validate_password(value):
    if len(value) < 8:
        return False, "Password must be at least 8 characters"
    return True, ""


class SignUpForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        container = Frame(self)
        Text(container, "input_label", text="Full Name").pack(anchor="w")
        self.full_name = ValidatedInput(
            container, "Enter your full name", 50, "app/icons/FaSolidUser.svg", validate_full_name
        )
        self.full_name.pack(pady=(5, 15))
        Text(container, "input_label", text="Email Address").pack(anchor="w")
        self.email = ValidatedInput(
            container, "Enter your email address", 50, "app/icons/SiMaildotru.svg", validate_email
        )
        self.email.pack(pady=(5, 15))
        Text(container, "input_label", text="Phone (optional)").pack(anchor="w")
        self.phone = ValidatedInput(container, "Enter your phone number", 50, "app/icons/SiMaildotru.svg")
        self.phone.pack(pady=(5, 15))

        self.signup_button = Button(container, text="Sign Up", state="disabled")
        self.signup_button.pack()

        container.pack()
        self.full_name.on_change(lambda e: self.update_button_state())
        self.email.on_change(lambda e: self.update_button_state())

    def update_button_state(self):
        self.signup_button.config(state="normal" if self.is_valid() else "disabled")

    def is_valid(self):
        full_name_valid, _ = validate_full_name(self.full_name.get())
        email_valid, _ = validate_email(self.email.get())
        return full_name_valid and email_valid
