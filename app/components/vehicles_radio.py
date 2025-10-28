import tkinter as tk

from app.components.frame import Frame
from app.components.icon import Icon
from app.components.image import Img, ImgProps, Resize
from app.components.text import Text
from app.style import Theme

VEHICLES = {
    "SALOON": {
        "name": "Saloon",
        "description": "Standard saloon car with comfortable seating for four.",
        "passengers": 4,
        "luggage": 2,
        "image": "app/images/saloon.webp",
        "image_width": 130,
        "image_height": 80,
    },
    "MPV": {
        "name": "MPV",
        "description": "Large vehicle suitable for small groups and families.",
        "passengers": 8,
        "luggage": 8,
        "image": "app/images/MPV.webp",
        "image_width": 130,
        "image_height": 130,
    },
    "MINIBUS": {
        "name": "Minibus",
        "description": "Spacious minibus ideal for large groups and events.",
        "passengers": 16,
        "luggage": 10,
        "image": "app/images/minibus.avif",
        "image_width": 120,
        "image_height": 100,
    },
}


class VehiclesRadio:
    def __init__(self, parent):
        self.selected = None
        self.cards = {}
        self.frame = tk.Frame(parent)
        self._build_ui()

    def _build_ui(self):
        for index, (key, properties) in enumerate(VEHICLES.items()):
            print(len(VEHICLES) - 1)
            card = Frame(self.frame, padx=5, pady=5)

            img = Img(
                card,
                properties["image"],
                ImgProps(resize=Resize(properties["image_width"], properties["image_height"])),
                width=properties["image_width"],
                height=properties["image_height"],
            )
            img.pack(side="left", anchor="w")

            content = Frame(card)
            name = Text(content, "md", text=properties["name"])
            name.pack()

            description = Text(content, "xs", text=properties["description"], fg=Theme.NEUTRAL_700, wraplength=180)
            description.pack()

            icons = Frame(content)
            passengers = Icon(
                icons, "app/icons/BsPeople.svg", text=properties["passengers"], padx=6, resize=Resize(20, 20)
            )
            passengers.pack(side="left")

            luggage = Icon(icons, "app/icons/TbLuggage.svg", text=properties["luggage"], padx=3, resize=Resize(20, 20))
            luggage.pack(side="left")
            icons.pack()

            content.pack(side="left", anchor="ne")

            widgets = [card, img, name, content, description, icons, passengers, luggage]

            row, col = divmod(index, 2)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

            for widget in widgets:
                # default argument 'k' prevents late binding issue causing all values of 'key' to evaluate as 'MINIBUS'
                widget.bind("<Button-1>", lambda e, k=key: self.select(k))

            self.cards[key] = {"frame": card, "widgets": widgets}
        self.frame.rowconfigure(0, weight=1, minsize=150)
        self.frame.rowconfigure(1, weight=1, minsize=150)

    def select(self, key):
        # Deselect previous
        if self.selected and self.selected in self.cards:
            self.cards[self.selected]["frame"].config(bg=Theme.NEUTRAL_200)
            for widget in self.cards[self.selected]["widgets"]:
                widget.config(bg=Theme.BACKGROUND)

        # Select new
        self.selected = key
        self.cards[key]["frame"].config(bg=Theme.NEUTRAL_200)
        for widget in self.cards[self.selected]["widgets"]:
            widget.config(bg=Theme.NEUTRAL_200)

    def get(self):
        return self.selected
