from app.api import MockApi
from app.components.button import Button
from app.components.frame import Frame
from app.components.header import Header
from app.components.scrollable_frame import ScrollableFrame
from app.components.split_frame import SplitFrame
from app.components.text import Text
from app.database.db import Database
from app.database.models import PaymentMethod
from app.frame_controller import FrameController
from app.pages.booking.components.booking_form import BookingForm
from app.pages.booking.components.payment_form import PaymentForm
from app.pages.booking.components.payment_method_radio import PaymentMethodRadio
from app.pages.booking.components.summary import Summary
from app.state import AppState
from app.style import Theme
from app.utils.datetime import format_datetime, timestamp_to_datetime, to_timestamp


class BookingPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.payment_methods = Database().user.get_payment_methods(AppState.user.id)
        self._build_ui()

        if pick_up_time := AppState.booking.pick_up_time:
            dt = timestamp_to_datetime(pick_up_time)
            self.booking_form.time.set(dt.hour, dt.minute)
            self.booking_form.date.set(dt)
            self.on_booking_form_change("date", pick_up_time)
        if vehicle := AppState.booking.vehicle:
            self.booking_form.vehicle.select(vehicle)
            self.on_booking_form_change("vehicle", vehicle)
        if payment_type := AppState.booking.payment_type:
            self.on_payment_type_change(payment_type)
            self.on_booking_form_change("payment_type", payment_type)
        else:
            if len(self.payment_methods) > 0:
                self.on_payment_type_change("CARD")
                self.on_booking_form_change("payment_type", "CARD")

        if message := AppState.booking.message:
            self.booking_form.message.set(message)
            self.on_booking_form_change("message", message)

        self.booking_form.on_change(self.on_booking_form_change)
        self.payment_form.on_change(self.on_payment_form_change)
        if not vehicle:
            self.booking_form.vehicle.select("SALOON")
            self.on_booking_form_change("vehicle", "SALOON")

        if not pick_up_time:
            self.booking_form.set_init_date()
            self.on_booking_form_change("date", "")

        self.update_price()

    def _build_ui(self):
        header = Header(self)
        header.pack(anchor="nw", fill="x")

        self.split_frame = SplitFrame(self)
        self.split_frame.left = ScrollableFrame(self.split_frame)

        self.split_frame.left.grid(row=0, column=0, sticky="nsew", padx=0)
        self.split_frame.columnconfigure(0, minsize=640)
        self.split_frame.columnconfigure(1, minsize=640)

        container = Frame(self.split_frame.left.interior)

        Button(
            container,
            variant="ghost",
            text="Back",
            icon="app/icons/IoArrowBack.svg",
            command=lambda: FrameController.get().show_frame("MainPage"),
        ).pack(anchor="nw")

        self.booking_form = BookingForm(container)
        self.booking_form.pack()

        container.pack(padx=40, pady=0, fill="both")

        self.split_frame.right = Frame(self.split_frame)
        right_container = Frame(self.split_frame.right)

        self.summary = Summary(right_container)
        self.summary.pack(anchor="nw", fill="x")

        payment_form_container = Frame(right_container)
        self.payment_form = PaymentForm(payment_form_container)
        self.payment_methods_selector = PaymentMethodsSelector(
            payment_form_container, self.payment_methods, self.toggle_show_payment_form, self.on_payment_form_change
        )
        payment_form_container.pack(anchor="nw", fill="x")

        bottom = Frame(right_container)
        self.pricing_container = Frame(bottom)
        self.subtotal = Text(self.pricing_container, "sm", text="")
        self.vat = Text(self.pricing_container, "sm", text="")
        self.total = Text(self.pricing_container, "lg", text="")
        Text(self.pricing_container, "sm", text="Subtotal:").grid(row=0, column=0, sticky="w")
        Text(self.pricing_container, "sm", text="VAT:").grid(row=1, column=0, sticky="w")
        Text(self.pricing_container, "lg", text="Total:").grid(row=2, column=0, sticky="w")

        self.subtotal.grid(row=0, column=1, sticky="e")
        self.vat.grid(row=1, column=1, sticky="e")
        self.total.grid(row=2, column=1, sticky="e")
        self.pricing_container.grid_columnconfigure(0, weight=1)
        self.pricing_container.pack(anchor="nw", fill="x")

        self.error_text = Text(bottom, "xs", text="", fg=Theme.ERROR)
        self.error_text.pack()

        self.submit_button = Button(bottom, text="Submit", state="disabled", command=self.submit)
        self.submit_button.pack(fill="x", expand=True)

        bottom.pack(anchor="s", fill="x", expand=True)
        right_container.pack(fill="both", expand=True, pady=20, padx=10)
        self.split_frame.right.grid(row=0, column=1, sticky="nsew")

    def toggle_show_payment_form(self, event=None):
        self.payment_methods_selector.pack_forget()
        self.payment_methods_selector.selected_payment_method.select(None)
        self.payment_form.pack(anchor="nw", fill="x")

    def on_booking_form_change(self, key, value):
        match key:
            case "date" | "time":
                self.summary.date.configure(
                    text=format_datetime(self.booking_form.date.get(), self.booking_form.time.get())
                )
                AppState.booking.update(
                    {
                        "pick_up_time": to_timestamp(
                            self.booking_form.date.get(),
                            self.booking_form.time.get(),
                        )
                    }
                )
            case "vehicle":
                self.summary.vehicle.configure(text=value.capitalize())
                AppState.booking.update({"vehicle": value})
                self.update_price()

            case "payment_type":
                self.on_payment_type_change(value)
            case "message":
                AppState.booking.update({"message": value})
                self.summary.message.configure(text=value)
        self.check_can_submit()

    def on_payment_type_change(self, pt):
        if not pt:
            return
        self.summary.payment_type.configure(text=pt.capitalize())
        AppState.booking.update({"payment_type": pt})
        self.booking_form.payment_type.select(pt, propagate=False)
        if pt == "CARD":
            if len(self.payment_methods) > 0:
                self.payment_methods_selector.pack(fill="x")
            else:
                self.payment_form.pack(anchor="nw", fill="x")
                self.payment_methods_selector.pack_forget()
        else:
            self.payment_methods_selector.pack_forget()
            self.payment_form.pack_forget()
        pass

    def on_payment_form_change(self, event=None):
        self.check_can_submit()

    def update_price(self):
        fare = MockApi().get_route_fare(
            AppState.booking.pick_up_location, AppState.booking.drop_off_location, AppState.booking.vehicle or "SALOON"
        )
        self.subtotal.configure(text=f"£{fare['subtotal'] / 100}")
        self.vat.configure(text=f"£{fare['vat'] / 100}")
        self.total.configure(text=f"£{fare['total'] / 100}")
        AppState.booking.update({"fare": fare["total"]})

    def check_can_submit(self):
        booking_form_valid = self.booking_form.is_valid()
        payment_form_valid = self.payment_form.is_valid()
        match self.booking_form.payment_type.get():
            case "CARD":
                if booking_form_valid and (
                    payment_form_valid or self.payment_methods_selector.selected_payment_method.get()
                ):
                    self.submit_button.configure(state="normal")
                else:
                    self.submit_button.configure(state="disabled")
            case "CASH":
                if booking_form_valid:
                    self.submit_button.configure(state="normal")
                else:
                    self.submit_button.configure(state="disabled")

    def submit(self):
        self.error_text.configure(text="")
        AppState.booking.update({"user_id": AppState.user.id})
        db = Database()
        if AppState.booking.payment_type == "CARD":
            pm_dict = {pm.id: pm for pm in self.payment_methods}
            new_payment_method = False
            if pm_id := self.payment_methods_selector.selected_payment_method.get():
                pm = pm_dict[pm_id]
            else:
                pm = self.payment_form.values()
                new_payment_method = True
            payment_successful = MockApi().processs_payment(pm)
            if not payment_successful:
                self.error_text.configure(text="Payment failed. Please try a different card")
                return

            if new_payment_method:
                payment_method_id = db.user.save_payment_method(
                    PaymentMethod(pm.name, pm.card, int(pm.expiry_month), int(pm.expiry_year), int(pm.security_code)),
                    AppState.user.id,
                )
                print("payment_method_id", payment_method_id)
            AppState.booking.update({"paid": 1, "payment_method_id": payment_method_id})

            MockApi().send_email("BOOKING_CONFIRM", AppState.user.email)

        booking_id, err = db.booking.create(AppState.booking)

        if err:
            print(err)
            self.error_text.configure(text=err)
        else:
            print(booking_id)
            AppState.booking.update({"id": booking_id})
            FrameController.get().show_frame("BookingConfirmPage")


class PaymentMethodsSelector(Frame):
    def __init__(self, parent, payment_methods: list[PaymentMethod], cb, on_change, **kwargs):
        super().__init__(parent, **kwargs)
        Text(self, "md", text="Your saved cards:").pack()
        self.selected_payment_method = PaymentMethodRadio(self, payment_methods)
        self.selected_payment_method.frame.pack(fill="x")
        self.selected_payment_method.on_change(on_change)
        Button(self, variant="ghost", text="Use a different payment method", command=cb).pack()
