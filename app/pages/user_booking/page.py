from dataclasses import asdict
from datetime import datetime
from tkinter import Toplevel
from app.api import MockApi
from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.hr import HorizontalRule
from app.components.icon import Icon, Resize
from app.components.scrollable_frame import ScrollableFrame
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.frame_controller import FrameController
from app.pages.booking.components.booking_form import BookingForm
from app.pages.booking.components.payment_form import PaymentForm
from app.pages.user_booking.components.available_drivers_radio import AvailableDriversRadio
from app.pages.user_booking.components.edit_view import EditView
from app.state import AppState
from app.style import StyleManager, Theme
from app.utils.datetime import format_datetime, format_timestamp, timestamp_to_datetime, to_timestamp


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

        self.view = NormalView(self.container, self.booking, lambda: self.switch_view("EDIT"))
        self.switch_view("DEFAULT")

        self.container.pack(fill="both", expand=True)

    def switch_view(self, view="DEFAULT", success=False):
        match view:
            case "DEFAULT":
                self.view.pack_forget()
                self.view = NormalView(
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


class NormalView(Frame):
    def __init__(self, parent, booking: Booking, switch_view, success=False, **kwargs):
        super().__init__(parent, **kwargs)

        self.modal = Modal()
        self.booking = booking
        if success:
            frame = Frame(self, bg=Theme.INDIGO_200, pady=5)
            Text(frame, "sm", text="Successfully updated booking!", bg=Theme.INDIGO_200, fg=Theme.INDIGO_800).pack()
            frame.pack(fill="x")

        container = Frame(self, highlightbackground=Theme.NEUTRAL_200, highlightthickness=2, padx=30, pady=30)
        top = Frame(container)
        top.grid_columnconfigure(0, weight=1)
        Text(top, "lg", text="Booking Details").grid(row=0, column=0, sticky="w")

        if not booking.assigned_driver_id and AppState.user.role == "ADMIN":
            Button(top, text="Assign Driver", variant="secondary", command=lambda: switch_view("ASSIGN_DRIVER")).grid(
                row=0, column=1
            )
        if not booking.is_cancelled and not booking.is_completed:
            Button(top, text="Edit", command=lambda: switch_view("EDIT")).grid(row=0, column=2, padx=10)
            Button(top, text="Cancel", bg=Theme.ERROR, activebackground=Theme.ERROR, command=self.confirm_cancel).grid(
                row=0, column=3
            )

        Text(top, "xs", fg=Theme.NEUTRAL_700, text=f"ID: {booking.id}").grid(row=1, column=0, sticky="w")

        if booking.is_cancelled:
            Text(top, "sm", text="Cancelled", fg=Theme.ERROR).grid(row=2, column=0, sticky="w")
        if booking.is_completed and not booking.is_cancelled:
            Text(top, "sm", text="Completed", fg=Theme.INDIGO_600).grid(row=2, column=0, sticky="w")

        top.pack(anchor="w", fill="x")
        HorizontalRule(container).pack(fill="both", pady=(15, 5))

        Summary(container, booking).pack(fill="both", expand=True)

        container.pack(fill="both", expand=True)

    def confirm_cancel(self):
        should_cancel = self.modal.confirm_action(self)
        if should_cancel:
            self.booking.cancelled = 1
            Database().booking.update(self.booking)
            FrameController.get().show_frame("UserBookingPage", {"id": self.booking.id})


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


from app.database.models import Booking


class Summary(Frame):
    def __init__(self, parent, booking: Booking, **kwargs):
        super().__init__(parent, **kwargs)

        pick_up_container = Frame(self)
        Icon(pick_up_container, "app/icons/FiMapPin.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(pick_up_container, "xs", text="Pick up:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        Text(pick_up_container, "sm", text=booking.pick_up_location).grid(
            row=1,
            column=1,
            sticky="nw",
        )
        pick_up_container.pack(anchor="nw")

        drop_off_container = Frame(self)
        Icon(drop_off_container, "app/icons/BiSolidMapPin.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(drop_off_container, "xs", text="Drop off:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        Text(drop_off_container, "sm", text=booking.drop_off_location).grid(
            row=1,
            column=1,
            sticky="nw",
        )
        drop_off_container.pack(anchor="nw")

        HorizontalRule(self).pack(fill="both", pady=(15, 5))

        grid = Frame(self)

        date_container = Frame(grid)
        Icon(date_container, "app/icons/FaRegularCalendar.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(date_container, "xs", text="Pick up time", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.date = Text(date_container, "sm", text=format_timestamp(booking.pick_up_time))
        self.date.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        date_container.grid(row=0, column=0)

        vehicle_container = Frame(grid)
        Icon(vehicle_container, "app/icons/AiOutlineCar.svg", resize=Resize(20, 20), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(vehicle_container, "xs", text="Vehicle:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.vehicle = Text(vehicle_container, "sm", text=booking.vehicle.capitalize())
        self.vehicle.grid(
            row=1,
            column=1,
            sticky="nw",
        )
        vehicle_container.grid(row=0, column=2, padx=10)

        grid.pack(anchor="nw")

        message_container = Frame(self)
        Icon(message_container, "app/icons/FiMessageSquare.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(message_container, "xs", text="Message:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        self.message = Text(
            message_container,
            "sm",
            text=booking.message if booking.message else "N/A",
            wraplength=550,
            anchor="w",
            justify="left",
        )
        self.message.grid(
            row=1,
            column=1,
            sticky="ew",
        )
        message_container.pack(anchor="nw")

        HorizontalRule(self).pack(fill="both", pady=(15, 5))

        driver_container = Frame(self)
        Icon(driver_container, "app/icons/FaSolidUser.svg", resize=Resize(18, 18), width=30).grid(
            row=0, column=0, sticky="nw"
        )
        Text(driver_container, "xs", text="Driver:", fg=Theme.NEUTRAL_700).grid(
            row=0,
            column=1,
            sticky="w",
        )
        assigned_driver = Text(
            driver_container,
            "sm",
            text="N/A",
            wraplength=550,
            anchor="w",
            justify="left",
        )
        assigned_driver.grid(
            row=1,
            column=1,
            sticky="ew",
        )
        driver_container.pack(anchor="nw")

        bottom = Frame(self)
        pricing_container = Frame(bottom)
        subtotal = Text(pricing_container, "sm", text=f"£{booking.subtotal_pounds}")
        vat = Text(pricing_container, "sm", text=f"£{booking.vat_pounds}")
        total = Text(pricing_container, "lg", text=f"£{booking.fare_pounds}")
        Text(pricing_container, "sm", text="Subtotal:").grid(row=0, column=0, sticky="w")
        Text(pricing_container, "sm", text="VAT (20%):").grid(row=1, column=0, sticky="w")
        Text(pricing_container, "lg", text="Total:").grid(row=2, column=0, sticky="w")

        subtotal.grid(row=0, column=1, sticky="e")
        vat.grid(row=1, column=1, sticky="e")
        total.grid(row=2, column=1, sticky="e")
        pricing_container.grid_columnconfigure(0, weight=1)
        pricing_container.pack(anchor="nw", fill="x")

        bottom.pack(anchor="s", fill="x", expand=True)

        if driver_id := booking.assigned_driver_id:
            driver, _ = Database().user.get_by_id(driver_id)
            if driver:
                assigned_driver.configure(text=driver.full_name)
