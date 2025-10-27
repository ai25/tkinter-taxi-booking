class Validator:
    @classmethod
    def is_empty(cls, value, name="Value"):
        if len(value) < 1:
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
