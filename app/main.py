import tkinter as tk

import pyglet

from app.database.db import Database
from app.frame_controller import FrameController
from app.state import AppState
from app.style import Theme
from app.utils.auth import Auth


pyglet.font.add_file("app/fonts/Manrope-Regular.ttf")
pyglet.font.add_file("app/fonts/Manrope-Bold.ttf")


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Circle Taxi")
        self.geometry("1400x1000")
        self.configure(bg=Theme.BACKGROUND)

        session = Auth.load_session()
        db = Database()
        if session and "user_id" in session and "token" in session:
            user = db.user.get_by_session(session["user_id"], session["token"])
            if user:
                AppState.user = user

        FrameController.initialize(self)
        FrameController.get().show_frame("MainPage")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
