import tkinter as tk
from .input import Input
from .style import StyleManager, Theme

class ValidatedInput(Input):
    def __init__(self, parent, placeholder="", validator=None):
        super().__init__(parent, placeholder)
        self.validator = validator
        self.error_label = None

        self.entry.bind('<KeyRelease>', self._validate)

    def _validate(self, event=None):
        if not self.validator:
            return

        value = self.get()
        is_valid, error_msg = self.validator(value)

        if not is_valid and value:  # Only show error if there's input
            self._show_error(error_msg)
            self.input_container.configure(
                highlightbackground='#EF4444',  
                highlightthickness=2
            )
        else:
            self._hide_error()
            if not self.placeholder_active:
                self.input_container.configure(
                    highlightbackground=Theme.ACCENT,
                    highlightthickness=2
                )

    def _show_error(self, message):
        if not self.error_label:
            self.error_label = tk.Label(
                self,
                text=message,
                bg=Theme.BACKGROUND,
                fg='#EF4444',
            )
            self.error_label.pack(anchor='w', pady=(3, 0))
        else:
            self.error_label.configure(text=message)

    def _hide_error(self):
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None

