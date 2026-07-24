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
        self.text = tk.Text(
            self.main_frame,
            undo=True,
            wrap="none",
            font=self.editor_font,
            borderwidth=0,
            highlightthickness=0,
            insertwidth=2
        )

        self.text.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.v_scroll = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.on_vertical_scroll
        )

        self.v_scroll.grid(
            row=0,
            column=2,
            sticky="ns"
        )

        self.h_scroll = ttk.Scrollbar(
            self.main_frame,
            orient="horizontal",
            command=self.text.xview
        )

        self.h_scroll.grid(
            row=1,
            column=1,
            sticky="ew"
        )
        self.text.configure(
            yscrollcommand=self.on_text_scroll,
            xscrollcommand=self.h_scroll.set
        )
        self.status = ttk.Label(
            self,
            anchor="w"
        )

        self.status.pack(
            fill="x"
        )

        self.update_status()
    def on_vertical_scroll(
        self,
        *args
    ):

        self.text.yview(
            *args
        )

        self.line_numbers.yview(
            *args
        )

    def on_text_scroll(
        self,
        first,
        last
    ):

        self.v_scroll.set(
            first,
            last
        )

        self.line_numbers.yview_moveto(
            first
        )
    def create_menu(
        self
    ):

        self.menu = tk.Menu(
            self
        )

        self.configure(
            menu=self.menu
        )

        self.file_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        self.edit_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        self.view_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        self.menu.add_cascade(
            label="File",
            menu=self.file_menu
        )

        self.menu.add_cascade(
            label="Edit",
            menu=self.edit_menu
        )

        self.menu.add_cascade(
            label="View",
            menu=self.view_menu
        )