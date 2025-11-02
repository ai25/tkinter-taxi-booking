from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.text import Text
from app.state import AppState


class BookingConfirmPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")

        container = Frame(self)
        Text(container, "h1", text="Thank you for booking with us!").pack()
        Text(container, "h3", text=f"Your booking reference is: {AppState.booking.id}").pack(pady=20)
        Button(container, text="View Booking").pack(pady=20)

        bottom = Frame(container)
        Text(bottom, "h3", text="What happens next?").pack(anchor="w")
        Text(bottom, "lg", text=f"A confirmation email has been sent to {AppState.user.email}.").pack(anchor="w")
        Text(bottom, "lg", text="Our driver will arrive 10-15 minutes before your scheduled pickup time.").pack(
            anchor="w"
        )
        bottom.pack(anchor="s", fill="x", expand=True, padx=20)

        container.pack(padx=160, pady=80, fill="both", expand=True)
