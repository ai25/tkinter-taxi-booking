from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.scrollable_frame import ScrollableFrame
from app.components.split_frame import SplitFrame
from app.frame_controller import FrameController
from app.pages.booking.components.booking_form import BookingForm
from app.pages.booking.components.payment_form import PaymentForm
from app.pages.booking.components.summary import Summary
from app.state import AppState
from app.utils.datetime import format_datetime, to_timestamp


class BookingPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")

        self.split_frame = SplitFrame(self)
        self.split_frame.left = ScrollableFrame(self.split_frame)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=0)
        self.split_frame.columnconfigure(0, minsize=640)
        self.split_frame.columnconfigure(1, minsize=640)

        container = Frame(self.split_frame.left.interior)

        Button(
            container,
            variant="ghost",
            text="Back",
            icon="app/icons/IoArrowBack.svg",
            command=lambda: FrameController.get().show_frame("MainPage"),
        ).pack(anchor="nw")

        self.booking_form = BookingForm(container)
        self.booking_form.pack()
        self.booking_form.on_change(self.on_booking_form_change)

        container.pack(padx=40, pady=0, fill="both")

        self.split_frame.right = Frame(self.split_frame)
        right_container = Frame(self.split_frame.right)

        self.summary = Summary(right_container)
        self.summary.pack(anchor="nw", fill="x")

        payment_form_container = Frame(right_container)
        self.payment_form = PaymentForm(payment_form_container)
        payment_form_container.pack(anchor="nw", fill="x")

        bottom = Frame(right_container)

        submit_button = Button(bottom, text="Submit")
        submit_button.pack(fill="x", expand=True)

        bottom.pack(anchor="s", fill="x", expand=True)
        right_container.pack(fill="both", expand=True, pady=20, padx=10)
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

    def on_booking_form_change(self, key, value):
        match key:
            case "date" | "time":
                self.summary.date.configure(
                    text=format_datetime(self.booking_form.date.get(), self.booking_form.time.get())
                )
                AppState.booking.update(
                    {
                        "pick_up_time": to_timestamp(
                            self.booking_form.date.get(),
                            self.booking_form.time.get(),
                        )
                    }
                )

            case "vehicle":
                self.summary.vehicle.configure(text=value.capitalize())
                AppState.booking.update({"vehicle": value})
            case "payment_type":
                self.summary.payment_type.configure(text=value.capitalize())
                AppState.booking.update({"payment_type": value})
                if value == "CARD":
                    self.payment_form.pack(anchor="nw", fill="x")
                else:
                    self.payment_form.pack_forget()
            case "message":
                AppState.booking.update({"message": value})
                self.summary.message.configure(text=value.capitalize())
        self.check_can_submit()

    def check_can_submit(self):
        pass
