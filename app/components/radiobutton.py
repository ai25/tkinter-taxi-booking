import tkinter as tk

from app.style import StyleManager


class RadioButton(tk.Radiobutton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        StyleManager.apply(self, "radiobutton")
        self.configure(**kwargs)
