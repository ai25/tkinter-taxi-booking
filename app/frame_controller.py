import tkinter as tk
from typing import Literal

from app.pages import get_page_class
from app.style import Theme


PageName = Literal[
    "MainPage",
    "SignUpPage",
    "LogInPage",
    "BookingPage",
    "BookingConfirmPage",
    "UserBookingsPage",
    "UserBookingPage",
]


class FrameController:
    _instance = None

    @classmethod
    def initialize(cls, parent):
        if cls._instance is None:
            cls._instance = cls(parent)
        return cls._instance

    @classmethod
    def get(cls):
        if cls._instance is None:
            raise RuntimeError("FrameController not initialized")
        return cls._instance

    def __init__(self, parent):
        self.root = tk.Frame(parent, height=1000, width=1400, bg=Theme.BACKGROUND)
        self.root.pack(side="top", fill="both", expand=True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_name: PageName, params=None):
        frame_class = get_page_class(frame_name)

        frame = frame_class(self.root, params) if params is not None else frame_class(self.root)

        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
