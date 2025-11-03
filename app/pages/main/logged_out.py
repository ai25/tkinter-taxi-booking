from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.image import Img, ImgProps
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.frame_controller import FrameController


class LoggedOut(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)
        header = Header(self.split_frame.left)
        header.pack(anchor="nw", fill="x")

        container = Frame(self.split_frame.left)
        Text(container, text="Hello, Stranger!").pack()
        Text(container, "h3", text="Let's get you started.").pack(pady=10)
        buttons_container = Frame(container, pady=20)
        Button(
            buttons_container,
            text="Log In",
            command=lambda: FrameController.get().show_frame("LogInPage"),
        ).grid(row=0, column=0, padx=10)
        Button(
            buttons_container,
            variant="secondary",
            text="Sign Up",
            command=lambda: FrameController.get().show_frame("SignUpPage"),
        ).grid(row=0, column=1)
        buttons_container.pack()
        container.pack(pady=250)

        self.split_frame.right = Img(self.split_frame, "app/images/home1.jpg", ImgProps(x=-200, anchor="nw"))
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")
