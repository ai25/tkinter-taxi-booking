import bcrypt
import json
from pathlib import Path


class Auth:
    _SESSION_FILE = Path.cwd() / ".session"

    @classmethod
    def hash_password(cls, txt: str):
        return bcrypt.hashpw(txt.encode("utf-8"), bcrypt.gensalt())

    @classmethod
    def verify_password(cls, password: str, hash: str):
        return bcrypt.checkpw(password.encode("utf-8"), hash)

    @classmethod
    def save_session(cls, user_id: int, token: str = None):
        cls._SESSION_FILE.write_text(json.dumps({"user_id": user_id, "token": token}))

    @classmethod
    def load_session(cls):
        if not cls._SESSION_FILE.exists():
            return None
        return json.loads(cls._SESSION_FILE.read_text())

    @classmethod
    def clear_session(cls):
        cls._SESSION_FILE.unlink(missing_ok=True)
