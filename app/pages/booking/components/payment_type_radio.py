from app.components.frame import Frame
from app.components.icon import Icon
from app.components.image import Img, ImgProps, Resize
from app.components.text import Text
from app.style import Theme


PAYMENT_TYPES = {
    "CASH": {"name": "Cash", "icon": "app/icons/BsCash.svg"},
    "CARD": {"name": "Card", "icon": "app/icons/FaRegularCreditCard.svg"},
}


class PaymentTypeRadio(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected = None
        self.cards = {}
        self._build_ui()

    def _build_ui(self):
        for key, properties in PAYMENT_TYPES.items():
            frame = Frame(self, padx=5, pady=5, highlightthickness=2, highlightbackground=Theme.NEUTRAL_300)
            icon = Icon(frame, properties["icon"])
            icon.pack(side="left")
            text = Text(frame, "sm", text=properties["name"])
            text.pack(side="left")

            widgets = [frame, icon, text]

            frame.pack(side="left", padx=5, pady=5)

            for widget in widgets:
                widget.bind("<Button-1>", lambda e, k=key: self.select(k))

            self.cards[key] = {"frame": frame, "widgets": widgets}

    def select(self, key, propagate=True):
        # Deselect previous
        if self.selected and self.selected in self.cards:
            self.cards[self.selected]["frame"].config(bg=Theme.BACKGROUND, highlightbackground=Theme.NEUTRAL_300)
            for widget in self.cards[self.selected]["widgets"]:
                widget.config(bg=Theme.BACKGROUND)

        # Select new
        self.selected = key
        self.cards[key]["frame"].config(bg=Theme.INDIGO_200, highlightbackground=Theme.INDIGO_300)
        for widget in self.cards[self.selected]["widgets"]:
            widget.config(bg=Theme.INDIGO_200)

        if propagate:
            for cb in self.on_change_callbacks:
                cb()

    def get(self):
        return self.selected

    on_change_callbacks = []

    def on_change(self, cb):
        self.on_change_callbacks.append(cb)
