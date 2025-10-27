from app.components.button import Button
from app.components.frame import Frame
from app.components.image import Img, ImgProps
from app.components.logo import Logo
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.database import Database
from app.frame_controller import FrameController
from app.models import User
from app.pages.log_in.components.log_in_form import LogInForm
from app.state import AppState
from app.style import Theme
from app.utils.auth import Auth


class LogInPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)

        Logo(self.split_frame.left).pack(anchor="nw", padx=20, pady=20)

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
        try:
            with Database().get_connection() as conn:
                cursor = conn.execute("SELECT * FROM user WHERE email = ?", (values.email,))
                row = cursor.fetchone()
                print(row)
                print(row[4])
                if row and Auth.verify_password(values.password, row[4]):
                    print("SUccess!")
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    AppState.user = user
                    # FrameController.get().show_frame("MainPage")
                else:
                    self.form.show_error("Incorrect email or password")
        except:
            self.form.show_error("Something went wrong. Please try again later.")

    def on_form_change(self, event=None):
        self.login_button.config(state="normal" if self.form.is_valid() else "disabled")
        self.form.clear_error()
