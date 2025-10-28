import tkinter as tk

from app.style import StyleManager, Theme


class Menu(tk.Menu):
    def __init__(self, parent, tearoff=0, **kwargs):
        super().__init__(parent, tearoff=tearoff)
        StyleManager.apply(self, "menu")
        self.configure(**kwargs)

    def show_popup(self, x, y):
        self.tk_popup(x, y)

    def add_button(self, **kwargs):
        self.add_command(
            background=Theme.BACKGROUND, foreground=Theme.FOREGROUND, activebackground=Theme.NEUTRAL_200, **kwargs
        )
