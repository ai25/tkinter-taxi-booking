import tkinter as tk
from .style import StyleManager, Theme

class SplitFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=Theme.BACKGROUND)
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left = tk.Frame(self, bg=Theme.BACKGROUND, highlightthickness=0,bd=0)
        self.right = tk.Canvas(self, highlightthickness=0, bd=0)

    def build_left(self, build_fn):
        build_fn(self.left)
        return self

    def build_right(self, build_fn):
        build_fn(self.right)
        return self
