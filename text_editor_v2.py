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