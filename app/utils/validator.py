import datetime

from app.utils.datetime import to_timestamp


class Validator:
    @classmethod
    def is_empty(cls, value, name="Value"):
        if not value or len(value) < 1:
            return False, f"{name} cannot be empty"
        return True, ""

    @classmethod
    def validate_full_name(cls, value):
        if len(value) < 4:
            return False, "Name is too short"
        return True, ""

    @classmethod
    def validate_email(cls, value):
        if "@" not in value or "." not in value:
            return False, "Invalid email address"
        return True, ""

    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            return False, "Password must be at least 8 characters"
        return True, ""

    @classmethod
    def validate_repeat_password(cls, value, password):
        if value != password:
            return False, "Passwords must match"
        return True, ""

    @classmethod
    def validate_pickup_date(cls, date, time):
        dt = to_timestamp(date, time)
        if not dt:
            return False, "Invalid pickup date"

        now = int(datetime.datetime.now().timestamp())
        if now >= dt:
            return False, "Pickup date cannot be in the past"
        return True, ""

    @classmethod
    def validate_card(cls, value):
        if len(value) != 16:
            return False, "Invalid card number"
        if not value.isdigit():
            return False, "Invalid card number"
        return True, ""

    @classmethod
    def validate_card_expiry(cls, month, year):
        current_month = datetime.date.today().month
        current_year = int(str(datetime.date.today().year)[-2:])

        try:
            month_int = int(month)
            year_int = int(year)
        except ValueError:
            return False, "Invalid expiry date"

        if not month.isdigit() or not year.isdigit():
            return False, "Invalid expiry date"

        if not (0 < len(month) < 3):
            return False, "Invalid expiry date"

        if len(year) != 2:
            return False, "Invalid expiry date"

        if not (0 < month_int < 13):
            return False, "Invalid expiry date"

        is_expired = (year_int < current_year) or (year_int == current_year and month_int < current_month)

        if is_expired:
            return False, "Card is expired"
        return True, ""

    @classmethod
    def validate_security_code(cls, value):
        if len(value) != 3:
            return False, "Invalid security code"
        if not value.isdigit():
            return False, "Invalid security code"
        return True, ""
