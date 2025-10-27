import tkinter as tk
from app.components.frame import Frame


class LoggedIn(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="LoggedIn")
        label.pack(padx=10, pady=10)
