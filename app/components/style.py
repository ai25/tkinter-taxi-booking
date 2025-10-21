class Theme:
    BACKGROUND = "#F1F5F9"
    CARD_BG = "#1E293B"
    ACCENT = "#3B82F6"
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = TEXT_PRIMARY
    bistre = "#442E28"
    orange_crayola = "#f3722c"
    carrot_orange = "#f8961e"
    coral = "#f9844a"
    saffron = "#f9c74f"
    pistachio = "#90be6d"
    zomp = "#43aa8b"
    dark_cyan = "#4d908e"
    paynes_gray = "#577590"
    cerulean = "#277da1"
    CARD_BG = saffron

class StyleManager:
    STYLES = {
        'input': {
            'bg': Theme.BACKGROUND,
            'fg': Theme.TEXT_PRIMARY,
            'font': ('Manrope', 12),
            'insertbackground': Theme.TEXT_PRIMARY,
            'border': 0,
            'highlightthickness': 0
        },
        'input_icon': {
            'bg': Theme.ACCENT,
        },
        'button': {
            'bg': Theme.saffron,
            'fg': Theme.TEXT_PRIMARY,
            'font': ('Manrope', 12),
            'activebackground': Theme.carrot_orange,
            'activeforeground': Theme.TEXT_PRIMARY,
            'border': 0,
            'cursor': 'hand2',
            "padx": 20,
            "pady": 10
        },
        'button_secondary': {
            'bg': Theme.TEXT_PRIMARY,
            'fg': Theme.BACKGROUND,
            'font': ('Manrope', 12),
            'activebackground': Theme.carrot_orange,
            'activeforeground': Theme.TEXT_PRIMARY,
            'border': 0,
            'cursor': 'hand2',
            "padx": 20,
            "pady": 10
        },
        
        "frame": {
            "bg": Theme.BACKGROUND,
        },

        "image": {
            "bg": Theme.BACKGROUND,
        },
        "h1": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.TEXT_PRIMARY,
            "font": ("Manrope", 52, "bold")
        },
        "h3": {
            "bg": Theme.BACKGROUND,
            "fg": Theme.TEXT_PRIMARY,
            "font": ("Manrope", 24)
        }
    }
    
    @classmethod
    def apply(cls, widget, style_name):
        if style_name not in cls.STYLES:
            raise ValueError(f"Style '{style_name}' not found")
        
        widget.configure(**cls.STYLES[style_name])
    
    @classmethod
    def get(cls, style_name):
        return cls.STYLES[style_name].copy()

