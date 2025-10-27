from tkinter import ttk

from app.style import Theme


class Tabs(ttk.Notebook):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        style = ttk.Style()

        # Configure tab appearance
        style.configure(
            "TNotebook.Tab",
            background=Theme.NEUTRAL_200,
            foreground=Theme.FOREGROUND,
            padding=[10, 5],
            font=("Manrope", 12),
            borderwidth=0,
        )

        # Tab appearance when selected
        style.map(
            "TNotebook.Tab",
            background=[("selected", Theme.BACKGROUND)],
            foreground=[("selected", Theme.FOREGROUND)],
            expand=[("selected", [1, 1, 1, 0])],  # expand tab when selected
        )

        # Configure notebook background
        style.configure(
            "TNotebook",
            background=Theme.NEUTRAL_200,
            borderwidth=0,
        )

        # Configure the pane (content area)
        style.configure("TFrame", background=Theme.BACKGROUND)
        self.pack(fill="both", expand=True)

        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)

        self.add(frame1, text="Tab 1")
        self.add(frame2, text="Tab 2", state="disabled")

        self.select(0)  # Switch to index
        self.tab(0, text="Renamed")  # Modify tab
        # self.forget(1)  # Remove tab
        self.index("current")  # Get active index
        self.tabs()  # List all tab IDs

        def on_tab_change(event):
            idx = self.index("current")

        self.bind("<<NotebookTabChanged>>", on_tab_change)
