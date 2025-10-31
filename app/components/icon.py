import io
import tkinter as tk
from PIL import Image, ImageTk
from cairosvg import svg2png
from app.components.frame import Frame
from app.components.image import Resize
from app.style import StyleManager


class Icon(tk.Label):
    def __init__(self, parent, icon, text="", compound="right", resize: Resize = None, **kwargs):
        super().__init__(parent)

        png_data = svg2png(url=icon)
        img = Image.open(io.BytesIO(png_data))
        if resize:
            img.thumbnail((resize.width, resize.height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.photo = photo
        StyleManager.apply(self, "icon")
        self.configure(image=photo, text=text, compound=compound, **kwargs)
