import customtkinter as ctk
from ui.theme import *


class TitleBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            height=TITLEBAR_HEIGHT,
            fg_color=SURFACE,
            corner_radius=0
        )

        self.grid_propagate(False)

        self.build()

    def build(self):

        self.grid_columnconfigure(1, weight=1)

        # Logo
        self.logo = ctk.CTkLabel(
            self,
            text="🌌",
            font=("SF Pro Display", 18)
        )

        self.logo.grid(
            row=0,
            column=0,
            padx=(12, 6)
        )

        # Title
        self.title = ctk.CTkLabel(
            self,
            text="Project Nebula",
            font=("SF Pro Display", 15, "bold")
        )

        self.title.grid(
            row=0,
            column=1,
            sticky="w"
        )