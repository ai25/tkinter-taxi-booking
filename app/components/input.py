import io
import tkinter as tk

from cairosvg import svg2png
from PIL import Image, ImageTk

from .style import StyleManager, Theme


class Input(tk.Frame):
    def __init__(self, parent, placeholder="", width=None, icon="", **kwargs):
        super().__init__(parent, bg=Theme.BACKGROUND, **kwargs)

        self.placeholder = placeholder
        self.placeholder_active = False

        # Container for border effect
        self.input_container = tk.Frame(
            self, bg=Theme.BACKGROUND, highlightbackground=Theme.NEUTRAL_600, highlightthickness=1
        )

        self.input_container.pack(fill=tk.BOTH, expand=True)

        if icon:
            png_data = svg2png(url=icon)
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)))
            self.img = img
            panel = tk.Label(self.input_container, image=img, width=40)
            StyleManager.apply(panel, "input_icon")
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(
            self.input_container,
        )
        StyleManager.apply(self.entry, "input")
        self.entry.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        if width:
            self.entry.configure(width=width)

        if placeholder:
            self._show_placeholder()

        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _show_placeholder(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=Theme.NEUTRAL_600)
        self.placeholder_active = True

    def _hide_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=Theme.FOREGROUND)
            self.placeholder_active = False

    def _on_focus_in(self, event):
        self.input_container.configure(highlightbackground=Theme.INDIGO_600, highlightthickness=2)
        self._hide_placeholder()

    def _on_focus_out(self, event):
        self.input_container.configure(highlightbackground=Theme.NEUTRAL_600, highlightthickness=1)
        if not self.entry.get() and self.placeholder:
            self._show_placeholder()

    def on_change(self, cb):
        self.entry.bind("<KeyRelease>", cb)

    def get(self):
        """Get the input value (returns empty string if placeholder is shown)"""
        if self.placeholder_active:
            return ""
        return self.entry.get()

    def set(self, text):
        """Set the input value"""
        self._hide_placeholder()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def clear(self):
        """Clear the input"""
        self.entry.delete(0, tk.END)
        if self.placeholder:
            self._show_placeholder()
