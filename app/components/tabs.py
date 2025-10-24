from tkinter import ttk


class Tabs(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)

        self.add(frame1, text="Tab 1")
        self.add(frame2, text="Tab 2", state="disabled")

        self.select(0)  # Switch to index
        self.tab(0, text="Renamed")  # Modify tab
        self.forget(1)  # Remove tab
        self.index("current")  # Get active index
        self.tabs()  # List all tab IDs

        def on_tab_change(event):
            idx = self.index("current")

        self.bind("<<NotebookTabChanged>>", on_tab_change)
