import io
import tkinter as tk

from cairosvg import svg2png
from PIL import Image, ImageTk

from app.components.button import Button

from app.style import StyleManager, Theme


class Input(tk.Frame):
    def __init__(self, parent, placeholder="", width=None, icon="", type="text", **kwargs):
        super().__init__(parent, bg=Theme.BACKGROUND, **kwargs)

        self.placeholder = placeholder
        self.placeholder_active = False
        self.type = type
        self.show_password = False

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
        if type == "password":
            self.show_password_button = Button(
                self.input_container, icon="app/icons/ImEye.svg", command=self._toggle_show_password
            )
            StyleManager.apply(self.show_password_button, "show_password_button")
            self.show_password_button.pack(side="right", anchor="e", padx=10)

        self.entry.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        if width:
            if type == "password":
                width -= 5
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
        self.should_show_password()

    def _hide_placeholder(self):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=Theme.FOREGROUND)
            self.placeholder_active = False

    def _on_focus_in(self, event):
        self.input_container.configure(highlightbackground=Theme.INDIGO_600, highlightthickness=2)
        self._hide_placeholder()
        self.should_show_password()

    def _on_focus_out(self, event):
        self.input_container.configure(highlightbackground=Theme.NEUTRAL_600, highlightthickness=1)
        if not self.entry.get() and self.placeholder:
            self._show_placeholder()

    def _toggle_show_password(self):
        if self.show_password:
            self.show_password_button.configure(icon="app/icons/ImEye.svg")
            self.show_password = False
        else:
            self.show_password_button.configure(icon="app/icons/ImEyeBlocked.svg")
            self.show_password = True
        self.should_show_password()

    def should_show_password(self):
        if self.placeholder_active:
            self.entry.configure(show="")
            return
        if self.type == "password":
            if self.show_password:
                self.entry.configure(show="")
            else:
                self.entry.configure(show="*")

    on_change_callbacks = []

    def on_change(self, cb):
        self.entry.bind("<KeyRelease>", cb, add="+")
        self.on_change_callbacks.append(cb)

    def get(self):
        """Get the input value (returns empty string if placeholder is shown)"""
        if self.placeholder_active:
            return ""
        return self.entry.get()

    def set(self, text, propagate=True):
        """Set the input value"""
        self._hide_placeholder()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        if propagate:
            for cb in self.on_change_callbacks:
                cb(None)

    def clear(self):
        """Clear the input"""
        self.entry.delete(0, tk.END)
        if self.placeholder:
            self._show_placeholder()
