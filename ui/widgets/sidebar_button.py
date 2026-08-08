import customtkinter as ctk
from ui.theme import *


class SidebarButton(ctk.CTkButton):

    def __init__(self, master, text, icon="", command=None):

        super().__init__(

            master,

            text=f"{icon}  {text}",

            anchor="w",

            height=40,

            corner_radius=10,

            fg_color="transparent",

            hover_color="#2A3446",

            text_color=TEXT,

            font=("SF Pro Display", 14),

            command=command
        )