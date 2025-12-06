# https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
import tkinter as tk
from app.components.frame import Frame
from app.style import Theme


# Based on
#   https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class ScrollableFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            bg=Theme.BACKGROUND,
            activebackground=Theme.NEUTRAL_200,
            activerelief="solid",
            troughcolor=Theme.NEUTRAL_200,
        )
        vscrollbar.pack(fill="y", side="right", expand=False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set, bg=Theme.BACKGROUND)
        canvas.pack(side="left", fill="both", expand=True)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_linux_scroll_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_linux_scroll_down(event):
            canvas.yview_scroll(1, "units")

        # Bind scroll events directly to canvas and interior
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_linux_scroll_up)
        canvas.bind("<Button-5>", _on_linux_scroll_down)

        interior.bind("<MouseWheel>", _on_mousewheel)
        interior.bind("<Button-4>", _on_linux_scroll_up)
        interior.bind("<Button-5>", _on_linux_scroll_down)
