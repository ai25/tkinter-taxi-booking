from app.components.button import Button
from app.components.frame import Frame
from app.components.image import Img, ImgProps
from app.components.logo import Logo
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.frame_controller import FrameController
from app.models import User
from app.pages.sign_up.components.sign_up_form import SignUpForm
from app.repositories.user_repository import UserRepository
from app.state import AppState
from app.style import Theme
from app.utils.auth import Auth


class SignUpPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)

        Logo(self.split_frame.left).pack(anchor="nw", padx=20, pady=20)

        Text(self.split_frame.left, "h3", text="Create an account").pack(pady=20)

        self.form = SignUpForm(self.split_frame.left)
        self.form.pack()

        self.split_frame.right = Img(self.split_frame, "app/images/signup.jpg", ImgProps(x=-100, y=-400))
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

        self.signup_button = Button(self.split_frame.left, text="Sign Up", state="disabled", command=self.sign_up)
        self.signup_button.pack()
        self.form.on_change(self.update_button_state)
        Text(self.split_frame.left, "xs", text="Already have an account?").pack(pady=(20, 0))
        Button(
            self.split_frame.left,
            "ghost",
            text="Log In",
            fg=Theme.INDIGO_600,
            font=("Manrope", 11, "underline"),
            command=lambda: FrameController.get().show_frame("LogInPage"),
        ).pack()

    def sign_up(self):
        if not self.form.is_valid():
            return
        values = self.form.values()
        password = Auth.hash_password(values.password)
        user = User(None, values.role, values.full_name, values.email, password, values.phone, None)
        user_repo = UserRepository()
        id = user_repo.upsert(user)
        if id:
            AppState.user = user
            FrameController.get().show_frame("MainPage")

    def update_button_state(self, event=None):
        self.signup_button.config(state="normal" if self.form.is_valid() else "disabled")
