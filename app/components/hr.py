from app.components.frame import Frame
from app.style import Theme


class HorizontalRule(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=1, bg=Theme.NEUTRAL_300, **kwargs)
