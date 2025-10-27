from types import SimpleNamespace

from app.components.frame import Frame
from app.components.text import Text
from app.components.validated_input import ValidatedInput
from app.style import Theme
from app.utils.validator import Validator


class LogInForm(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def on_change(self, cb):
        self.email.on_change(cb)
        self.password.on_change(cb)

    def values(self):
        return SimpleNamespace(email=self.email.get(), password=self.password.get())

    def is_valid(self):
        email_valid, _ = Validator.is_empty(self.email.get())
        password_valid, _ = Validator.is_empty(self.password.get())
        return email_valid and password_valid

    def _build_ui(self):
        container = Frame(self)

        self.error_text = Text(container, "xs", text="Hello", fg=Theme.ERROR)
        self.error_text.pack()

        Text(container, "input_label", text="Email Address").pack(anchor="w")
        self.email = ValidatedInput(
            container,
            "Enter your email address",
            50,
            "app/icons/SiMaildotru.svg",
            validator=lambda v: Validator.is_empty(v, "Email address"),
        )
        self.email.pack(pady=(5, 15))

        Text(container, "input_label", text="Password").pack(anchor="w")
        self.password = ValidatedInput(
            container,
            "Enter your password",
            50,
            "app/icons/FaSolidAsterisk.svg",
            type="password",
            validator=lambda v: Validator.is_empty(v, "Password"),
        )
        self.password.pack(pady=(5, 15))

        container.pack()

    def show_error(self, error=""):
        self.error_text.configure(text=error)

    def clear_error(self):
        self.error_text.configure(text="")

        #
        # self.autofill_button = Button(
        #     container,
        #     text="Autofill",
        #     variant="ghost",
        #     command=self._autofill,
        # )
        # self.autofill_button.pack(pady=(0, 10))

    # def _autofill(self):
    #     user = Fake().user("USER")
    #     self.full_name.set(user.full_name)
    #     self.email.set(user.email)
    #     self.phone.set(user.phone)
    #     self.password.set(user.password)
    #     self.password.should_show_password()
    #     self.repeat_password.set(user.password)
    #     self.repeat_password.should_show_password()
    #     # self.master.master.master.update_button_state()  # type: ignore
