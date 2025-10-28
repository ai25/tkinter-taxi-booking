from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.image import Img, ImgProps
from app.components.logo import Logo
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.database.db import Database
from app.frame_controller import FrameController
from app.pages.log_in.components.log_in_form import LogInForm
from app.state import AppState
from app.style import Theme
from app.utils.auth import Auth


class LogInPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.db = Database()

        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)

        header = Header(self.split_frame.left)
        header.pack(anchor="nw", fill="x")

        Text(self.split_frame.left, "h3", text="Log into your account").pack(pady=20)

        self.form = LogInForm(self.split_frame.left)
        self.form.pack()

        self.split_frame.right = Img(self.split_frame, "app/images/signup.jpg", ImgProps(x=-100, y=-400))
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

        self.login_button = Button(self.split_frame.left, text="Log In", state="disabled", command=self.log_in)
        self.login_button.pack()

        Text(self.split_frame.left, "xs", text="Don't have an account?").pack(pady=(20, 0))
        Button(
            self.split_frame.left,
            "ghost",
            text="Sign Up",
            fg=Theme.INDIGO_600,
            font=("Manrope", 11, "underline"),
            command=lambda: FrameController.get().show_frame("SignUpPage"),
        ).pack()

        self.form.on_change(self.on_form_change)

    def log_in(self):
        values = self.form.values()

        user, error = self.db.user.authenticate(values.email, values.password)
        if user:
            AppState.user = user
            session_token = self.db.user.create_session(user.id)
            Auth.save_session(user.id, session_token)
            FrameController.get().show_frame("MainPage")
        else:
            self.form.show_error(error)

    def on_form_change(self, event=None):
        self.login_button.config(state="normal" if self.form.is_valid() else "disabled")
        self.form.clear_error()
