class Theme:
    NEUTRAL_50 = "#fafafa"
    NEUTRAL_100 = "#f5f5f5"
    NEUTRAL_200 = "#e5e5e5"
    NEUTRAL_300 = "#d4d4d4"
    NEUTRAL_400 = "#a3a3a3"
    NEUTRAL_500 = "#737373"
    NEUTRAL_600 = "#525252"
    NEUTRAL_700 = "#404040"
    NEUTRAL_800 = "#262626"
    NEUTRAL_900 = "#171717"
    NEUTRAL_950 = "#0a0a0a"
    INDIGO_50 = "#eef2ff"
    INDIGO_100 = "#e0e7ff"
    INDIGO_200 = "#c7d2fe"
    INDIGO_300 = "#a5b4fc"
    INDIGO_400 = "#818cf8"
    INDIGO_500 = "#6366f1"
    INDIGO_600 = "#4f46e5"
    INDIGO_700 = "#4338ca"
    INDIGO_800 = "#3730a3"
    INDIGO_900 = "#312e81"
    INDIGO_950 = "#1e1b4b"
    BACKGROUND = NEUTRAL_50
    FOREGROUND = NEUTRAL_950
    ERROR = "#EF4444"


class StyleManager:
    STYLES = {
        "input": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.FOREGROUND,
            "font": ("Manrope", 12),
            "insertbackground": Theme.FOREGROUND,
            "border": 0,
            "highlightthickness": 0,
        },
        "input_icon": {"bg": Theme.INDIGO_300, "padx": 5},
        "input_label": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.NEUTRAL_800,
            "font": ("Manrope", 12),
        },
        "button": {
            "bg": Theme.INDIGO_600,
            "fg": Theme.NEUTRAL_50,
            "font": ("Manrope", 12),
            "activebackground": Theme.INDIGO_700,
            "activeforeground": Theme.NEUTRAL_50,
            "border": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 10,
        },
        "button_secondary": {
            "bg": Theme.FOREGROUND,
            "fg": Theme.BACKGROUND,
            "font": ("Manrope", 12),
            "activebackground": Theme.NEUTRAL_800,
            "activeforeground": Theme.NEUTRAL_50,
            "border": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 10,
        },
        "button_ghost": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.NEUTRAL_800,
            "font": ("Manrope", 12),
            "activebackground": Theme.BACKGROUND,
            "activeforeground": Theme.NEUTRAL_700,
            "border": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
            "padx": 10,
            "pady": 5,
        },
        "radiobutton": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.FOREGROUND,
            "highlightthickness": 0,
            "font": ("Manrope", 12),
        },
        "show_password_button": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.FOREGROUND,
            "activebackground": Theme.NEUTRAL_200,
            "highlightthickness": 0,
        },
        "frame": {
            "bg": Theme.BACKGROUND,
        },
        "icon": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.FOREGROUND,
            "width": 40,
            "height": 40,
            "font": (
                "Manrope",
                12,
            ),
        },
        "image": {
            "bg": Theme.BACKGROUND,
            "highlightthickness": 0,
        },
        "menu": {
            "bg": Theme.NEUTRAL_50,
            "fg": Theme.FOREGROUND,
            "activebackground": Theme.NEUTRAL_200,
            "font": ("Manrope", 12),
            "relief": "flat",
            "border": 0,
        },
        "h1": {"bg": Theme.BACKGROUND, "fg": Theme.FOREGROUND, "font": ("Manrope", 52, "bold")},
        "h3": {"bg": Theme.BACKGROUND, "fg": Theme.FOREGROUND, "font": ("Manrope", 24)},
        "md": {"bg": Theme.BACKGROUND, "fg": Theme.FOREGROUND, "font": ("Manrope", 14)},
        "sm": {"bg": Theme.BACKGROUND, "fg": Theme.FOREGROUND, "font": ("Manrope", 12)},
        "xs": {"bg": Theme.BACKGROUND, "fg": Theme.FOREGROUND, "font": ("Manrope", 11)},
    }

    @classmethod
    def apply(cls, widget, style_name):
        if style_name not in cls.STYLES:
            raise ValueError(f"Style '{style_name}' not found")

        widget.configure(**cls.STYLES[style_name])

    @classmethod
    def get(cls, style_name):
        return cls.STYLES[style_name].copy()
