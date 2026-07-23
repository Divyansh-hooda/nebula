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

                data = file.read()

            self.text.delete(
                "1.0",
                tk.END
            )

            self.text.insert(
                "1.0",
                data
            )

            self.file_path = path

            self.modified = False

            self.text.edit_modified(False)

            self.title(
                f"Nebula Text Editor - {os.path.basename(path)}"
            )

            self.update_status()

        except Exception as e:

            messagebox.showerror(
                "Open File",
                str(e)
            )
    def save(self):

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
                        tk.END + "-1c"
                    )
                )

            self.modified = False

            self.text.edit_modified(False)

            self.update_status()

        except Exception as e:

            messagebox.showerror(
                "Save",
                str(e)
            )
    def save_as(self):

        path = filedialog.asksaveasfilename()

        if not path:
            return

        self.file_path = path

        self.save()

        self.title(
            f"Nebula Text Editor - {os.path.basename(path)}"
        )
    def confirm_discard(self):

        if not self.modified:
            return True

        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Do you want to save changes?"
        )

        if answer is None:
            return False

        if answer:
            self.save()

            if self.modified:
                return False

        return True

    def close_editor(self):

        if not self.confirm_discard():
            return

        self.destroy()
    def text_modified(
        self,
        event=None
    ):

        if self.text.edit_modified():

            self.modified = True

            self.text.edit_modified(False)

            self.update_status()
    def update_status(self):

        cursor = self.text.index(
            tk.INSERT
        )

        line, column = cursor.split(".")

        if self.file_path:

            filename = os.path.basename(
                self.file_path
            )

        else:

            filename = "Untitled"

        status = (
            f"{filename}    "
            f"Line {line}    "
            f"Column {int(column)+1}"
        )

        if self.modified:

            status += "    Modified"

        self.status.config(
            text=status
        )
    def zoom_in(self):

        self.font_size += 1

        self.editor_font.configure(
            size=self.font_size
        )

    def zoom_out(self):

        if self.font_size <= 6:
            return

        self.font_size -= 1

        self.editor_font.configure(
            size=self.font_size
        )
    def toggle_wrap(self):

        self.wrap = not self.wrap

        if self.wrap:

            self.text.config(
                wrap="word"
            )

            self.h_scroll.pack_forget()

        else:

            self.text.config(
                wrap="none"
            )

            self.h_scroll.pack(
                side="bottom",
                fill="x"
            )