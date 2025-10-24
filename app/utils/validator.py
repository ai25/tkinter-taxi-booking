class Validator:
    def validate_full_name(self, value):
        if len(value) < 4:
            return False, "Name is too short"
        return True, ""

    def validate_email(self, value):
        if "@" not in value or "." not in value:
            return False, "Invalid email address"
        return True, ""

    def validate_password(self, value):
        if len(value) < 8:
            return False, "Password must be at least 8 characters"
        return True, ""

    def validate_repeat_password(self, value, password):
        if value != password:
            return False, "Passwords must match"
        return True, ""
