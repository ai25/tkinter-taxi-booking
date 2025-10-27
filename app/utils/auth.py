import bcrypt


class Auth:
    @classmethod
    def hash_password(cls, txt: str):
        return bcrypt.hashpw(txt.encode("utf-8"), bcrypt.gensalt())

    @classmethod
    def verify_password(cls, password: str, hash: str):
        return bcrypt.checkpw(password.encode("utf-8"), hash)
