import tkinter as tk
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants

import io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from cairosvg import svg2png
from tkcalendar import DateEntry
from app.components.frame import Frame
from app.style import StyleManager, Theme


class TimePicker(Frame):
    def __init__(self, parent=None, icon="", width=50, **kwargs):
        super().__init__(parent)
        self.input_container = Frame(
            self,
            bg=Theme.BACKGROUND,
            highlightbackground=Theme.NEUTRAL_600,
            highlightthickness=1,
        )
        if icon:
            png_data = svg2png(url=icon)
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)))
            self.img = img
            panel = tk.Label(self.input_container, image=img, width=40)
            StyleManager.apply(panel, "input_icon")
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.input_container.pack(fill="both", expand=True)

        self.picker = SpinTimePickerOld(self.input_container)
        self.picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        self.picker.configureAll(
            bg=Theme.BACKGROUND,
            fg=Theme.FOREGROUND,
            font=("Manrope", 12),
            width=3,
        )
        self.picker.configure(bd=0, highlightthickness=0, bg=Theme.BACKGROUND, pady=12, padx=5)
        self.picker.configure_24HrsTime(bd=0, highlightthickness=0)
        self.picker.configure_separator(bg=Theme.BACKGROUND, fg=Theme.FOREGROUND)
        self.picker.configure_minute(bd=0, highlightthickness=0)

        self.picker.pack(fill="both", expand=True, padx=0, pady=0)

    def get(self):
        try:
            time = self.picker.time()
            return f"{time[0]}:{time[1]}"
        except (ValueError, AttributeError):
            return "00:00"

    on_change_callbacks = []

    def on_change(self, cb):
        # Spinbox returns the value before current change is processed
        # We need to:
        # 1. delay the callback 1 cycle
        # 2. use ButtonRelease insted of normal Button event
        def delayed_callback(event):
            self.after(1, lambda: cb(event))

        self.picker._24HrsTime.bind("<ButtonRelease-1>", delayed_callback)
        self.picker._minutes.bind("<ButtonRelease-1>", delayed_callback)
        self.picker._24HrsTime.bind("<KeyRelease>", delayed_callback)
        self.picker._minutes.bind("<KeyRelease>", delayed_callback)
        self.on_change_callbacks.append(cb)
