import tkinter as tk
from .style import StyleManager, Theme
from PIL import Image, ImageTk

class Img(tk.Canvas):
    def __init__(self, parent, src, **kwargs):
        super().__init__(parent, **kwargs)
        image = Image.open(src)
        self.photo = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.photo, anchor="nw")
        StyleManager.apply(self, "image")
        self.configure(**kwargs)
