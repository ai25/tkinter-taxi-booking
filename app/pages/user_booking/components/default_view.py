from app.api import MockApi
from app.components.button import Button
from app.components.frame import Frame
from app.components.hr import HorizontalRule
from app.components.modal import Modal
from app.components.text import Text
from app.database.db import Database
from app.database.models import Booking
from app.frame_controller import FrameController
from app.pages.user_booking.components.summary import Summary
from app.state import AppState
from app.style import Theme


class DefaultView(Frame):
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
            if self.booking.payment_type == "CARD":
                MockApi().process_refund(self.booking.payment_method_id)
            FrameController.get().show_frame("UserBookingPage", {"id": self.booking.id})
