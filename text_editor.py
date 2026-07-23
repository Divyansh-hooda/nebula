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
    def create_menu(self):

        self.menu = tk.Menu(
            self
        )

        self.config(
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
        self.file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.new_file
        )

        self.file_menu.add_command(
            label="Open...",
            accelerator="Ctrl+O",
            command=self.open_dialog
        )

        self.file_menu.add_command(
            label="Save",
            accelerator="Ctrl+S",
            command=self.save
        )

        self.file_menu.add_command(
            label="Save As...",
            accelerator="Ctrl+Shift+S",
            command=self.save_as
        )

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Exit",
            command=self.close_editor
        )
        self.edit_menu.add_command(
            label="Undo",
            accelerator="Ctrl+Z",
            command=lambda:
            self.text.event_generate("<<Undo>>")
        )

        self.edit_menu.add_command(
            label="Redo",
            accelerator="Ctrl+Y",
            command=lambda:
            self.text.event_generate("<<Redo>>")
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            command=lambda:
            self.text.event_generate("<<Cut>>")
        )

        self.edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            command=lambda:
            self.text.event_generate("<<Copy>>")
        )

        self.edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            command=lambda:
            self.text.event_generate("<<Paste>>")
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Select All",
            accelerator="Ctrl+A",
            command=lambda:
            self.text.event_generate("<<SelectAll>>")
        )
        self.view_menu.add_command(
            label="Zoom In",
            accelerator="Ctrl++",
            command=self.zoom_in
        )

        self.view_menu.add_command(
            label="Zoom Out",
            accelerator="Ctrl+-",
            command=self.zoom_out
        )

        self.view_menu.add_separator()

        self.view_menu.add_command(
            label="Toggle Word Wrap",
            command=self.toggle_wrap
        )
    def bind_events(self):

        self.bind(
            "<Control-s>",
            lambda e: self.save()
        )

        self.bind(
            "<Control-o>",
            lambda e: self.open_dialog()
        )

        self.bind(
            "<Control-n>",
            lambda e: self.new_file()
        )

        self.bind(
            "<Control-Shift-S>",
            lambda e: self.save_as()
        )

        self.text.bind(
            "<<Modified>>",
            self.text_modified
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_editor
        )
    def new_file(self):

        if not self.confirm_discard():
            return

        self.text.delete(
            "1.0",
            tk.END
        )

        self.file_path = None

        self.modified = False

        self.title(
            "Nebula Text Editor"
        )

        self.update_status()
    def open_dialog(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        self.open_file(path)