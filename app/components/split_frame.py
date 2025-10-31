import tkinter as tk

from app.style import Theme


class SplitFrame(tk.Frame):
    left: tk.Frame | tk.Canvas
    right: tk.Frame | tk.Canvas

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=Theme.BACKGROUND)
        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left = tk.Frame(self, bg=Theme.BACKGROUND, highlightthickness=0, bd=0)
        self.right = tk.Canvas(self, highlightthickness=0, bd=0)
