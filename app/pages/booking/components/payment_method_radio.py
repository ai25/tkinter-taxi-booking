from app.components.frame import Frame
from app.components.icon import Icon
from app.components.image import Img, ImgProps, Resize
from app.components.text import Text
from app.style import Theme


class PaymentMethodRadio:
    def __init__(self, parent, payment_methods):
        self.selected = None
        self.cards = {}
        self.frame = Frame(parent)
        self.payment_methods = payment_methods
        self._build_ui()

    def _build_ui(self):
        for index, pm in enumerate(self.payment_methods):
            card = Frame(
                self.frame,
                padx=5,
                pady=5,
                highlightthickness=2,
                highlightbackground=Theme.NEUTRAL_300,
            )

            content = Frame(card)
            name = Text(content, "md", text=pm.card_name)
            name.pack(anchor="w")

            number = Text(
                content, "xs", text=f"**** **** **** {pm.card_number[-4:]}", fg=Theme.NEUTRAL_700, wraplength=180
            )
            number.pack(anchor="w", pady=10)
            expiry = Text(content, "xs", text=f"{pm.exp_month}/{pm.exp_year}", fg=Theme.NEUTRAL_700, wraplength=180)
            expiry.pack(anchor="sw", expand=True)

            content.pack(fill="both", expand=True)

            widgets = [card, name, content, number, expiry]

            row, col = divmod(index, 2)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

            key = pm.id
            for widget in widgets:
                widget.bind("<Button-1>", lambda e, k=key: self.select(k))

            self.cards[key] = {"frame": card, "widgets": widgets}
        self.frame.rowconfigure(0, weight=1, minsize=150)
        self.frame.rowconfigure(1, weight=1, minsize=150)
        self.frame.columnconfigure(0, weight=1, minsize=250)
        self.frame.columnconfigure(1, weight=1, minsize=250)

    def select(self, key, propagate=True):
        # Deselect previous
        if self.selected and self.selected in self.cards:
            self.cards[self.selected]["frame"].config(bg=Theme.BACKGROUND, highlightbackground=Theme.NEUTRAL_300)
            for widget in self.cards[self.selected]["widgets"]:
                widget.config(bg=Theme.BACKGROUND)

        # Select new
        self.selected = key
        if self.selected and self.selected in self.cards:
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
