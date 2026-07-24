import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
class TextEditor(
    tk.Toplevel
):

    def __init__(
        self,
        master=None,
        file_path=None
    ):

        super().__init__(
            master
        )

        self.file_path = file_path

        self.modified = False

        self.wrap = False

        self.font_size = 13

        self.editor_font = font.Font(
            family="Menlo",
            size=self.font_size
        )

        self.title(
            "Nebula Text Editor"
        )

        self.geometry(
            "1100x700"
        )

        self.minsize(
            800,
            500
        )
        self.create_widgets()

        self.create_menu()

        self.bind_events()

        if file_path:

            self.open_file(
                file_path
            )

        self.after(
            100,
            self.focus_editor
        )
    def focus_editor(
        self
    ):

        self.text.focus_force()

        self.text.mark_set(
            "insert",
            "end-1c"
        )

        self.text.see(
            "insert"
        )
    def create_widgets(
        self
    ):

        self.main_frame = ttk.Frame(
            self
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.main_frame.rowconfigure(
            0,
            weight=1
        )

        self.main_frame.columnconfigure(
            1,
            weight=1
        )
        self.line_numbers = tk.Text(
            self.main_frame,
            width=5,
            padx=5,
            takefocus=0,
            border=0,
            background="#202020",
            foreground="#808080",
            state="disabled",
            wrap="none"
        )

        self.line_numbers.grid(
            row=0,
            column=0,
            sticky="ns"
        )