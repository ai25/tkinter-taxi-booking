import io
import tkinter as tk

from cairosvg import svg2png
from PIL import Image, ImageTk

from app.frame_controller import FrameController

from app.style import StyleManager


class Logo(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, width=150, height=50, **kwargs)

        png_data = svg2png(url="app/images/logo.svg")
        img = Image.open(io.BytesIO(png_data))
        img.thumbnail((150, 50), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(img)

        self.create_image(0, 0, image=self.img, anchor="nw")
        StyleManager.apply(self, "image")

        self.bind("<Button-1>", lambda e: FrameController.get().show_frame("MainPage"))
        self.configure(cursor="hand2")
