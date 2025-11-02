import io
import tkinter as tk

from cairosvg import svg2png
from PIL import Image, ImageOps, ImageTk

from app.components.image import Resize
from app.style import StyleManager


class Text(tk.Label):
    def __init__(
        self, parent, heading="h1", icon="", resize_icon: Resize = None, compound="left", icon_gap=5, **kwargs
    ):
        super().__init__(parent)
        if icon:
            png_data = svg2png(url=icon)
            img = Image.open(io.BytesIO(png_data))
            resize_icon = resize_icon or Resize(20, 20)
            img.thumbnail((resize_icon.width, resize_icon.height), Image.Resampling.LANCZOS)

            # transparent padding
            if compound == "left":
                img = ImageOps.expand(img, border=(0, 0, icon_gap, 0), fill=(0, 0, 0, 0))
            elif compound == "right":
                img = ImageOps.expand(img, border=(icon_gap, 0, 0, 0), fill=(0, 0, 0, 0))

            photo = ImageTk.PhotoImage(img)
            self.photo = photo
            self.configure(
                image=photo,
                compound=compound,
            )
        StyleManager.apply(self, heading)
        self.configure(**kwargs)
