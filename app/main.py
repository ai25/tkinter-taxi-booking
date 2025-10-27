import tkinter as tk

import pyglet

from app.style import Theme
from app.frame_controller import FrameController


pyglet.font.add_file("app/fonts/Manrope-Regular.ttf")
pyglet.font.add_file("app/fonts/Manrope-Bold.ttf")


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Yet Another Taxi App")
        self.geometry("1400x1000")
        self.configure(bg=Theme.BACKGROUND)

        FrameController.initialize(self)
        FrameController.get().show_frame("MainPage")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
