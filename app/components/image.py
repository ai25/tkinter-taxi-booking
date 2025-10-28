import tkinter as tk
from dataclasses import dataclass

from PIL import Image, ImageTk

from app.style import StyleManager


@dataclass
class Resize:
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height


@dataclass
class ImgProps:
    def __init__(self, x=0, y=0, anchor="nw", resize: Resize | None = None):
        self.x = x
        self.y = y
        self.anchor = anchor
        self.resize = resize


class Img(tk.Canvas):
    def __init__(self, parent, src, img_args: ImgProps = ImgProps(), **kwargs):
        super().__init__(parent, **kwargs)
        image = Image.open(src)
        if img_args.resize:
            image.thumbnail((img_args.resize.width, img_args.resize.height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.create_image(img_args.x, img_args.y, image=self.photo, anchor=img_args.anchor)
        StyleManager.apply(self, "image")
        self.configure(**kwargs)
