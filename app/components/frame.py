import tkinter as tk
from .style import StyleManager

class Frame(tk.Frame):
    def __init__(self,parent, **kwargs):
        super().__init__(parent)
        StyleManager.apply(self, "frame")
        self.configure(**kwargs)
