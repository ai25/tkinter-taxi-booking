import io
import tkinter as tk

from cairosvg import svg2png
from PIL import Image, ImageTk

from .style import StyleManager

class Button(tk.Button):
    def __init__(self, parent, variant=None, icon=None, **kwargs):
        super().__init__(parent)
        style_tag = "button"
        if variant:
            style_tag = f"button_{variant}"
        if icon:
            self._add_icon(icon)


        StyleManager.apply(self, style_tag)
        self.configure(**kwargs)

    def configure(self,icon=None,**kwargs):
        super().configure(**kwargs)
        if icon:
            self._add_icon(icon)

    def _add_icon(self, icon):
        png_data = svg2png(url=icon)
        self.img = ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)))
        self.configure(image=self.img, compound="left")

