import customtkinter as ctk
from ui.theme import *


class ActivityBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            width=ACTIVITY_BAR_WIDTH,
            fg_color=SURFACE,
            corner_radius=0
        )

        self.grid_propagate(False)

        self.build()

    def build(self):

        self.grid_columnconfigure(0, weight=1)

        self.buttons = {}

        items = [
            ("Explorer", "📁"),
            ("Search", "🔍"),
            ("AI", "✨"),
            ("Terminal", "⌨"),
            ("Extensions", "🧩"),
            ("Settings", "⚙"),
        ]

        for row, (name, icon) in enumerate(items):

            btn = ctk.CTkButton(
                self,
                text=icon,
                width=44,
                height=44,
                fg_color="transparent",
                hover_color="#2A3446",
                corner_radius=10,
                font=("SF Pro Display", 20),
                command=lambda n=name: self.select(n)
            )

            btn.grid(
                row=row,
                column=0,
                pady=(10 if row == 0 else 6, 0),
                padx=8
            )

            self.buttons[name] = btn

        self.active = None
        self.select("Explorer")

    def select(self, name):

        if self.active:

            self.buttons[self.active].configure(
                fg_color="transparent"
            )

        self.buttons[name].configure(
            fg_color=ACCENT
        )

        self.active = name