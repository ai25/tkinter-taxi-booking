import tkinter as tk
from .input import Input
from app.style import StyleManager, Theme


class ValidatedInput(Input):
    def __init__(
        self, parent, placeholder="", width=None, icon="", validator=None, validate_event="<FocusOut>", **kwargs
    ):
        super().__init__(parent, placeholder, width, icon, **kwargs)
        self.validator = validator
        self.error_label = None

        self.entry.bind(validate_event, self._validate, add="+")

    def _validate(self, event=None):
        if not self.validator:
            return

        value = self.get()
        is_valid, error_msg = self.validator(value)

        if not is_valid:
            self._show_error(error_msg)
            self.input_container.configure(highlightbackground=Theme.ERROR, highlightthickness=2)
        else:
            self._hide_error()
            if not self.placeholder_active:
                self.input_container.configure(highlightbackground=Theme.NEUTRAL_600, highlightthickness=2)

    def _show_error(self, message):
        if not self.error_label:
            self.error_label = tk.Label(
                self,
                text=message,
                bg=Theme.BACKGROUND,
                fg=Theme.ERROR,
            )
            self.error_label.pack(anchor="w", pady=(3, 0))
        else:
            self.error_label.configure(text=message)

    def _hide_error(self):
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
