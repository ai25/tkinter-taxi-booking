import tkinter as tk

from app.pages.main.logged_in import LoggedIn
from app.pages.main.logged_out import LoggedOut
from app.state import AppState


class MainPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        view = LoggedIn(self) if AppState.user else LoggedOut(self)
        view.pack(fill=tk.BOTH, expand=True)
