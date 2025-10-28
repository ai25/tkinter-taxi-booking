from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.icon import Icon
from app.components.image import Img, ImgProps
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.components.vehicles_radio import VehiclesRadio
from app.frame_controller import FrameController
from app.state import AppState


class BookingPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")

        self.split_frame = SplitFrame(self)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=10)

        container = Frame(self.split_frame.left)

        Button(
            container,
            variant="ghost",
            text="Back",
            icon="app/icons/IoArrowBack.svg",
            command=lambda: FrameController.get().show_frame("MainPage"),
        ).pack(anchor="nw")

        Text(container, "h3", text="Your Booking").pack(anchor="nw", pady=20)

        pick_up_container = Frame(container)
        Icon(pick_up_container, "app/icons/FiMapPin.svg").pack(side="left")
        Text(pick_up_container, "md", text=AppState.booking.pick_up_location).pack(pady=10)
        pick_up_container.pack(anchor="nw")

        drop_off_container = Frame(container)
        Icon(drop_off_container, "app/icons/BiSolidMapPin.svg").pack(side="left")
        Text(drop_off_container, "md", text=AppState.booking.drop_off_location).pack(pady=10)
        drop_off_container.pack(anchor="nw")

        radio = VehiclesRadio(container)

        radio.frame.pack(pady=20, anchor="nw")

        container.pack(padx=40, pady=0, fill="both")

        self.split_frame.right = Img(self.split_frame, "app/images/home1.jpg", ImgProps(x=-200, anchor="nw"))
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")
