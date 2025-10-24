import tkinter as tk
from datetime import datetime

from app.components import Button, Frame, Img, SplitFrame, Text
from app.controllers import FrameController
from app.state import AppState
from app.utils.frame_registry import page


@page("MainPage")
class MainPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        view = LoggedIn(self) if AppState.user else LoggedOut(self)
        view.pack(fill=tk.BOTH, expand=True)


class LoggedIn(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="LoggedIn")
        label.pack(padx=10, pady=10)


class LoggedOut(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)
        header = Text(self.split_frame.left, "h3", text="Logo")
        header.pack(anchor="nw", padx=0, pady=20)

        container = Frame(self.split_frame.left)
        Text(container, text="Hello, Stranger!").pack()
        Text(container, "h3", text="Let's get you started.").pack(pady=10)
        buttons_container = Frame(container, pady=20)
        Button(
            buttons_container,
            text="Login",
            command=lambda: print(datetime.fromtimestamp(int(datetime.now().timestamp()))),
        ).grid(row=0, column=0, padx=10)
        Button(
            buttons_container,
            variant="secondary",
            text="Sign Up",
            command=lambda: FrameController.get().show_frame("SignUpPage"),
        ).grid(row=0, column=1)
        buttons_container.pack()
        container.pack(pady=250)

        self.split_frame.right = Img(self.split_frame, "app/images/blurred_light_bg.jpg")
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")
