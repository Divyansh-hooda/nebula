import customtkinter as ctk

from ui.theme import *


class NebulaApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Nebula")

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.minsize(1200, 700)

        self.configure(fg_color=BACKGROUND)

        self.create_layout()

    def create_layout(self):

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.titlebar = ctk.CTkFrame(
            self,
            height=TITLEBAR_HEIGHT,
            fg_color=SURFACE,
            corner_radius=0
        )

        self.titlebar.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="nsew"
        )

        self.titlebar.grid_propagate(False)
