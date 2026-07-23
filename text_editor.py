import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
class TextEditor(tk.Toplevel):

    def __init__(
        self,
        master=None,
        file_path=None
    ):

        super().__init__(master)

        self.title("Nebula Text Editor")

        self.geometry("1100x700")

        self.minsize(
            800,
            500
        )

        self.file_path = file_path

        self.modified = False

        self.wrap = False

        self.font_size = 12

        self.editor_font = font.Font(
            family="Consolas",
            size=self.font_size
        )

        self.create_widgets()

        self.create_menu()

        self.bind_events()

        if file_path:
            self.open_file(file_path)
    def create_widgets(self):

        self.main = ttk.Frame(self)

        self.main.pack(
            fill="both",
            expand=True
        )

        self.text = tk.Text(
            self.main,
            undo=True,
            wrap="none",
            font=self.editor_font
        )

        self.v_scroll = ttk.Scrollbar(
            self.main,
            orient="vertical",
            command=self.text.yview
        )

        self.h_scroll = ttk.Scrollbar(
            self.main,
            orient="horizontal",
            command=self.text.xview
        )

        self.text.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )

        self.v_scroll.pack(
            side="right",
            fill="y"
        )

        self.h_scroll.pack(
            side="bottom",
            fill="x"
        )

        self.text.pack(
            fill="both",
            expand=True
        )

        self.status = ttk.Label(
            self,
            anchor="w"
        )

        self.status.pack(
            fill="x"
        )

        self.update_status()