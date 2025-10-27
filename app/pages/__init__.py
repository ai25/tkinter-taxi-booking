import tkinter as tk
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.pages.log_in.page import LogInPage
    from app.pages.main.page import MainPage
    from app.pages.sign_up.page import SignUpPage

_registry: dict[str, type[tk.Frame]] = {}


def get_page_class(name: str) -> type[tk.Frame]:
    if not _registry:
        _load_pages()
    return _registry[name]


def _load_pages():
    from app.pages.log_in.page import LogInPage
    from app.pages.main.page import MainPage
    from app.pages.sign_up.page import SignUpPage

    _registry["MainPage"] = MainPage
    _registry["SignUpPage"] = SignUpPage
    _registry["LogInPage"] = LogInPage
