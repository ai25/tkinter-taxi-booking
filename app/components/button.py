import tkinter as tk
from .style import StyleManager
import tkinter as tk

class Button(tk.Button):
    def __init__(self, parent, variant=None, **kwargs):
        super().__init__(parent)
        style_tag = "button"
        if variant:
            style_tag = f"button_{variant}"
        StyleManager.apply(self, style_tag)
        self.configure(**kwargs)
