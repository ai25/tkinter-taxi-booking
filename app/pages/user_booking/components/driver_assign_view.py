from app.components.button import Button
from app.components.frame import Frame
from app.components.text import Text
from app.database.db import Database
from app.pages.user_booking.components.available_drivers_radio import AvailableDriversRadio
from app.style import Theme


class DriverAssignView(Frame):
    def __init__(self, parent, booking, switch_view, **kwargs):
        super().__init__(parent, **kwargs)
        self.booking = booking
        self.switch_view = switch_view
        Text(self, "lg", text="Select any available driver:").pack(pady=(0, 20))

        self.selected_driver = AvailableDriversRadio(self, booking)
        self.selected_driver.pack(anchor="nw")
        self.selected_driver.on_change(self.on_driver_change)
        buttons = Frame(self)
        self.cancel = Button(
            buttons, text="Cancel", bg=Theme.ERROR, activebackground=Theme.ERROR, command=self.switch_view
        )
        self.cancel.pack(side="left", padx=10)
        self.submit = Button(buttons, text="Save", state="disabled", command=self.save)
        self.submit.pack()
        buttons.pack(pady=20)

    def on_driver_change(self):
        self.booking.assigned_driver_id = self.selected_driver.get()
        self.submit.configure(state="normal")

    def save(self):
        id, error = Database().booking.update(self.booking)
        if id is not None:
            print("success")
            self.switch_view()
        else:
            print("error", error)
