from app.components.frame import Frame
from app.components.text import Text
from app.database.db import Database
from app.style import StyleManager, Theme


class AvailableDriversRadio(Frame):
    def __init__(self, parent, booking, **kwargs):
        super().__init__(parent, **kwargs)
        self.selected = None
        self.cards = {}
        StyleManager.apply(self, "booking_card")
        self.grid_columnconfigure(0, weight=1)
        self.frame = Frame(parent)

        db = Database()

        drivers, _ = db.user.get_by_role("DRIVER")

        for index, driver in enumerate(drivers):
            card = Frame(self.frame, padx=5, pady=5, highlightthickness=2, highlightbackground=Theme.NEUTRAL_300)
            content = Frame(card)
            content.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

            available = True
            assigned_bookings, _ = db.booking.get_by_driver(driver.id)
            available_text = Text(content, "xs", text="Available", fg=Theme.INDIGO_600)
            if len(assigned_bookings) > 0:
                new_start = booking.pick_up_time - (60 * 10)  # -10 min
                new_end = booking.pick_up_time + (60 * 60)  # +1h
                for assigned_booking in assigned_bookings:
                    existing_start = assigned_booking.pick_up_time
                    existing_end = assigned_booking.pick_up_time + (60 * 60)  # +1h
                    if new_start < existing_end and new_end > existing_start:
                        available = False
                        break  # break so we don't keep looping if we know they're unavailable

            if not available:
                available_text.configure(text="Unavailable", fg=Theme.ERROR)

            available_text.pack()

            name = Text(content, "sm", text=driver.full_name)
            name.pack()

            widgets = [content, name, card, available_text]
            key = driver.id

            if available:
                for widget in widgets:
                    widget.bind("<Button-1>", lambda e, k=key: self.select(k))
                    widget.configure(cursor="hand2")
            row, col = divmod(index, 3)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            self.cards[key] = {"frame": card, "widgets": widgets}
        self.frame.pack()

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
