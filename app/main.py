import tkinter as tk

import pyglet

from app.components import Theme
from app.controllers import FrameController
from app.pages import MainPage


pyglet.font.add_file("app/fonts/Manrope-Regular.ttf")
pyglet.font.add_file("app/fonts/Manrope-Bold.ttf")


class HeaderSection:
    def __init__(self, parent, text):
        self.frame = tk.Frame(parent)
        self.text = text
        self._build()

    def _build(self):
        logo = tk.Label(self.frame, text=self.text, font=("Manrope", 20), bg=Theme.BACKGROUND)
        logo.pack(anchor="w")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


def validate_email(value):
    if "@" not in value or "." not in value:
        return False, "Invalid email address"
    return True, ""


def validate_password(value):
    if len(value) < 8:
        return False, "Password must be at least 8 characters"
    return True, ""


class SidePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the Side Page")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: FrameController.show_frame(self, CompletionScreen),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class CompletionScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = tk.Button(
            self, text="Return to menu", command=lambda: FrameController.show_frame(self, MainPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


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
