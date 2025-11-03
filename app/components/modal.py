from tkinter import Toplevel

from app.components.button import Button
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

        Text(modal, "sm", text="Are you sure?").pack()
        Button(modal, text="Yes", command=yes).pack(side="left")
        Button(modal, text="No", command=modal.destroy).pack(side="right")

        parent.wait_window(modal)
        return result["confirmed"]
