import tkinter as tk

from .style import Theme


class Card(tk.Frame):
    def __init__(self, parent, height=None):
        super().__init__(parent, bg=Theme.CARD_BG, highlightthickness=0)
        if height:
            self.configure(height=height)
        
        self.content = ttk.Frame(self, style='Card.TFrame')
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
