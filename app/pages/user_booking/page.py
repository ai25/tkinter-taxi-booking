from app.components.frame import Frame
from app.components.header import Header
from app.components.text import Text
from app.database.db import Database
from app.pages.user_booking.components.default_view import DefaultView
from app.pages.user_booking.components.driver_assign_view import DriverAssignView
from app.pages.user_booking.components.edit_view import EditView
from app.style import Theme


class UserBookingPage(Frame):
    def __init__(self, parent, params):
        super().__init__(parent)
        print(params["id"])
        self.db = Database()
        self.booking, self.error = self.db.booking.get_by_id(params["id"])
        print(self.booking)
        self._build_ui()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")

        self.container = Frame(self)
        Text(self.container, "lg", text=self.error, fg=Theme.ERROR).pack()

        self.view = DefaultView(self.container, self.booking, lambda: self.switch_view("EDIT"))
        self.switch_view("DEFAULT")

        self.container.pack(fill="both", expand=True)

    def switch_view(self, view="DEFAULT", success=False):
        match view:
            case "DEFAULT":
                self.view.pack_forget()
                self.view = DefaultView(
                    self.container, self.booking, lambda view: self.switch_view(view), success=success
                )
                self.view.pack(fill="both", expand=True, pady=(0, 80), padx=340)
            case "EDIT":
                self.view.pack_forget()
                self.view = EditView(self.container, self.booking, lambda s: self.switch_view("DEFAULT", success=s))
                self.view.pack(fill="both", expand=True)
            case "ASSIGN_DRIVER":
                self.view.pack_forget()
                self.view = DriverAssignView(self.container, self.booking, lambda: self.switch_view("DEFAULT"))
                self.view.pack(fill="both", expand=True)
