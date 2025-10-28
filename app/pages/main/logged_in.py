from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.image import Img, ImgProps
from app.components.logo import Logo
from app.components.menu import Menu
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.frame_controller import FrameController
from app.pages.main.components.address_form import AddressForm
from app.state import AppState
from app.utils.auth import Auth


class LoggedIn(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()
        # if the user got here by pressing back, it means the form is valid so we need to enable the button
        self._on_form_change()

    def _build_ui(self):
        self.split_frame = SplitFrame(self)

        header = Header(self.split_frame.left)
        header.pack(anchor="nw", fill="x")

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)

        container = Frame(self.split_frame.left)

        name = AppState.user.full_name
        Text(container, text=f"Hi, {name}!").pack()
        Text(container, "h3", text="Ready for your next trip?").pack(pady=10)

        self.form = AddressForm(container)
        self.form.pack()
        self.form.on_change(self._on_form_change)

        self.get_quote_button = Button(
            container,
            text="Get Quote",
            state="disabled",
            command=lambda: FrameController.get().show_frame("BookingPage"),
        )
        self.get_quote_button.pack(pady=10)
        container.pack(pady=60)

        self.split_frame.right = Img(self.split_frame, "app/images/home1.jpg", ImgProps(x=-200, anchor="nw"))
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

    def _on_form_change(self, event=None):
        self.get_quote_button.config(state="normal" if self.form.is_valid() else "disabled")
