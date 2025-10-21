import tkinter as tk
from .style import StyleManager

class Text(tk.Label):
    def __init__(self, parent, heading="h1", **kwargs):
        super().__init__(parent)
        StyleManager.apply(self, heading)
        self.configure(**kwargs)
