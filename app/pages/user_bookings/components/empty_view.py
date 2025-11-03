from app.components.frame import Frame
from app.components.text import Text


class EmptyView(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        Text(self, "lg", text="No bookings found.").pack()
