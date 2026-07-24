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
        self.edit_menu.add_command(
            label="Undo",
            accelerator="⌘Z",
            command=lambda:
            self.text.event_generate(
                "<<Undo>>"
            )
        )

        self.edit_menu.add_command(
            label="Redo",
            accelerator="⇧⌘Z",
            command=lambda:
            self.text.event_generate(
                "<<Redo>>"
            )
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Cut",
            accelerator="⌘X",
            command=lambda:
            self.text.event_generate(
                "<<Cut>>"
            )
        )

        self.edit_menu.add_command(
            label="Copy",
            accelerator="⌘C",
            command=lambda:
            self.text.event_generate(
                "<<Copy>>"
            )
        )

        self.edit_menu.add_command(
            label="Paste",
            accelerator="⌘V",
            command=lambda:
            self.text.event_generate(
                "<<Paste>>"
            )
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Select All",
            accelerator="⌘A",
            command=self.select_all
        )
        self.view_menu.add_command(
            label="Zoom In",
            accelerator="⌘+",
            command=self.zoom_in
        )

        self.view_menu.add_command(
            label="Zoom Out",
            accelerator="⌘-",
            command=self.zoom_out
        )

        self.view_menu.add_separator()

        self.view_menu.add_command(
            label="Toggle Word Wrap",
            command=self.toggle_wrap
        )
    def bind_events(
        self
    ):

        self.bind(
            "<Command-n>",
            lambda e: self.new_file()
        )

        self.bind(
            "<Command-o>",
            lambda e: self.open_dialog()
        )

        self.bind(
            "<Command-s>",
            lambda e: self.save()
        )

        self.bind(
            "<Command-Shift-S>",
            lambda e: self.save_as()
        )

        self.bind(
            "<Command-w>",
            lambda e: self.close_editor()
        )

        self.bind(
            "<Command-a>",
            lambda e: self.select_all()
        )

        self.bind(
            "<Command-z>",
            lambda e: self.text.event_generate(
                "<<Undo>>"
            )
        )

        self.bind(
            "<Command-Shift-z>",
            lambda e: self.text.event_generate(
                "<<Redo>>"
            )
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_editor
        )
    def new_file(
        self
    ):

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

        self.update_line_numbers()

        self.focus_editor()
    def open_dialog(
        self
    ):

        path = filedialog.askopenfilename()

        if not path:

            return

        self.open_file(
            path
        )
    def open_file(
        self,
        path
    ):

        if not self.confirm_discard():

            return

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            self.text.delete(
                "1.0",
                tk.END
            )

            self.text.insert(
                "1.0",
                content
            )

            self.file_path = path

            self.modified = False

            self.text.edit_modified(
                False
            )

            self.title(
                f"Nebula Text Editor — {os.path.basename(path)}"
            )

            self.update_line_numbers()

            self.update_status()

            self.focus_editor()

        except Exception as e:

            messagebox.showerror(
                "Open File",
                str(e)
            )
    def save(
        self
    ):

        if self.file_path is None:

            return self.save_as()

        try:

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(

                    self.text.get(
                        "1.0",
                        "end-1c"
                    )

                )

            self.modified = False

            self.text.edit_modified(
                False
            )

            self.update_status()

        except Exception as e:

            messagebox.showerror(
                "Save",
                str(e)
            )
    def save_as(
        self
    ):

        path = filedialog.asksaveasfilename(

            defaultextension=".txt"

        )

        if not path:

            return

        self.file_path = path

        self.save()

        self.title(

            f"Nebula Text Editor — {os.path.basename(path)}"

        )