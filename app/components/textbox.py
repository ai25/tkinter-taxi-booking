import tkinter as tk

from app.style import StyleManager


class Textbox(tk.Text):
    def __init__(self, parent, width=80, height=5, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        StyleManager.apply(self, "textbox")

    def get(self):
        return super().get("1.0", "end-1c")

    def on_change(self, cb):
        self.bind("<KeyRelease>", cb)
