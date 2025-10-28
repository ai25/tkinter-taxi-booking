from app.components.button import Button
from app.components.frame import Frame
from app.components.logo import Logo
from app.components.menu import Menu
from app.state import AppState
from app.utils.auth import Auth


class Header(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        Logo(self).pack(anchor="nw", padx=20, pady=20, side="left")

        popup = Menu(self)
        popup.add_command(label="Log out", command=Auth.logout)

        def show_popup():
            x = btn.winfo_rootx()
            y = btn.winfo_rooty() + btn.winfo_height()
            popup.tk_popup(x, y)

        btn = Button(self, variant="ghost", icon="app/icons/BsThreeDotsVertical.svg", command=show_popup)
        if AppState.user:
            btn.pack(pady=10, side="right")
