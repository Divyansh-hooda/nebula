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

        self.activity_bar = ctk.CTkFrame(
            self,
            width=ACTIVITY_BAR_WIDTH,
            fg_color=SURFACE,
            corner_radius=0
        )

        self.activity_bar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.activity_bar.grid_propagate(False)

        # -------------------------
        # Sidebar
        # -------------------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=SIDEBAR_WIDTH,
            fg_color=SURFACE_ALT,
            corner_radius=0
        )

        self.sidebar.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # -------------------------
        # Workspace
        # -------------------------

        self.workspace = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
            corner_radius=0
        )

        self.workspace.grid(
            row=1,
            column=2,
            sticky="nsew"
        )
