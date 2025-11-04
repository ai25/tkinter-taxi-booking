from tkinter import Toplevel

from app.components.button import Button
from app.components.frame import Frame
from app.components.text import Text
from app.style import Theme


class Modal:
    def __init__(self, **kwargs):
        pass

    def confirm_action(self, parent):
        modal = Toplevel(bg=Theme.BACKGROUND)
        modal.transient(parent)  # Set parent
        modal.geometry("300x200")
        modal.grab_set()

        # Centre on screen
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (modal.winfo_width() // 2)
        y = (modal.winfo_screenheight() // 2) - (modal.winfo_height() // 2)
        modal.geometry(f"+{x}+{y}")

        result = {"confirmed": False}

        def yes():
            result["confirmed"] = True
            modal.destroy()

        Text(modal, "sm", text="Are you sure?").pack(expand=True)
        buttons = Frame(modal)
        Button(buttons, text="No", command=modal.destroy, bg=Theme.ERROR, activebackground=Theme.ERROR).grid(
            row=0, column=0
        )
        Button(buttons, text="Yes", command=yes).grid(row=0, column=1, padx=10)
        buttons.pack(fill="y", expand=True)

        parent.wait_window(modal)
        return result["confirmed"]
