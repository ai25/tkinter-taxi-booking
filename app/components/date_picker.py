import io
import tkinter as tk
from tkinter import ttk

from cairosvg import svg2png
from PIL import Image, ImageTk
from tkcalendar import DateEntry

from app.components.frame import Frame
from app.style import StyleManager, Theme


class DatePicker(Frame):
    def __init__(self, parent=None, icon="", width=50, **kwargs):
        super().__init__(parent, **kwargs)

        style = ttk.Style()
        style.configure(
            "my.DateEntry",
            fieldbackground=Theme.BACKGROUND,
            foreground=Theme.FOREGROUND,
            borderwidth=0,
            relief="flat",
            padding=(10, 12),
        )
        self.input_container = Frame(
            self,
            bg=Theme.BACKGROUND,
            highlightbackground=Theme.NEUTRAL_600,
            highlightthickness=1,
            width=50,
        )
        if icon:
            png_data = svg2png(url=icon)
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)))
            self.img = img
            panel = tk.Label(self.input_container, image=img, width=40)
            StyleManager.apply(panel, "input_icon")
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.input_container.pack(fill="both", expand=True)

        self.picker = DateEntry(
            self.input_container, locale="en_GB", style="my.DateEntry", width=width, font=("Manrope", 12)
        )

        self.picker.pack(fill="both", expand=True, padx=0, pady=0)

    def get(self):
        return self.picker.get_date()

    def set(self, date, propagate=True):
        self.picker.set_date(date)
        if propagate:
            for cb in self._on_change_callbacks:
                cb(None)

    _on_change_callbacks = []

    def on_change(self, cb):
        self.picker.bind("<KeyRelease>", cb)
        self._on_change_callbacks.append(cb)
