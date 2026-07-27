import os
import keyword
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter import simpledialog
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
            font=self.editor_font,
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
            insertwidth=2,
            inactiveselectbackground="#3c3c3c",
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
        self.create_find_bar()
        self.status = ttk.Label(
            self,
            anchor="w"
        )

        self.status.pack(
            fill="x"
        )

        self.update_status()
        self.configure_syntax_tags()
        self.blink_cursor()
    def configure_syntax_tags(
        self
    ):

        self.text.tag_configure(
            "keyword",
            foreground="#569CD6"
        )

        self.text.tag_configure(
            "string",
            foreground="#CE9178"
        )

        self.text.tag_configure(
            "comment",
            foreground="#6A9955"
        )

        self.text.tag_configure(
            "number",
            foreground="#B5CEA8"
        )

        self.text.tag_configure(
            "function",
            foreground="#DCDCAA"
        )
    def create_find_bar(
        self
    ):

        self.find_frame = ttk.Frame(
            self
        )

        self.find_var = tk.StringVar()

        self.replace_var = tk.StringVar()

        ttk.Label(
            self.find_frame,
            text="Find:"
        ).pack(
            side="left",
            padx=(8,2)
        )

        self.find_entry = ttk.Entry(
            self.find_frame,
            textvariable=self.find_var,
            width=25
        )

        self.find_entry.pack(
            side="left",
            padx=2
        )

        ttk.Label(
            self.find_frame,
            text="Replace:"
        ).pack(
            side="left",
            padx=(8,2)
        )

        self.replace_entry = ttk.Entry(
            self.find_frame,
            textvariable=self.replace_var,
            width=25
        )

        self.replace_entry.pack(
            side="left",
            padx=2
        )

        self.match_label = ttk.Label(
            self.find_frame,
            text="0 Matches"
        )

        self.match_label.pack(
            side="left",
            padx=10
        )

        ttk.Button(
            self.find_frame,
            text="Previous",
            command=self.find_previous
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            self.find_frame,
            text="Next",
            command=self.find_next
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            self.find_frame,
            text="Replace",
            command=self.replace_current
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            self.find_frame,
            text="Replace All",
            command=self.replace_all
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            self.find_frame,
            text="✕",
            width=3,
            command=self.hide_find_bar
        ).pack(
            side="right",
            padx=5
        )
        self.find_entry.bind(
            "<KeyRelease>",
            self.update_search
        )
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
        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Find",
            accelerator="⌘F",
            command=self.find_text
        )

        self.edit_menu.add_command(
            label="Replace",
            accelerator="⌥⌘F",
            command=self.replace_text
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
        self.text.bind(
            "<<Modified>>",
            self.text_modified
        )

        self.text.bind(
            "<KeyRelease>",
            self.update_status
        )

        self.text.bind(
            "<ButtonRelease-1>",
            self.update_status
        )

        self.text.bind(
            "<KeyRelease>",
            self.update_line_numbers,
            add="+"
        )
        self.text.bind(
            "<KeyRelease>",
            self.highlight_current_line,
            add="+"
        )

        self.text.bind(
            "<ButtonRelease-1>",
            self.highlight_current_line,
            add="+"
        )

        self.text.bind(
            "<FocusIn>",
            self.highlight_current_line
        )
        self.bind(
            "<Command-f>",
            lambda e: self.show_find_bar()
        )

        self.bind(
            "<Command-Option-f>",
            lambda e: self.replace_text()
        )
        self.find_entry.bind(
            "<Return>",
            lambda e: self.find_next()
        )

        self.find_entry.bind(
            "<Escape>",
            lambda e: self.hide_find_bar()
        )

        self.replace_entry.bind(
            "<Return>",
            lambda e: self.replace_current()
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
    def close_editor(
        self
    ):

        if not self.confirm_discard():

            return

        self.destroy()
    def select_all(
        self
    ):

        self.text.tag_add(
            "sel",
            "1.0",
            "end"
        )

        self.text.mark_set(
            "insert",
            "1.0"
        )

        self.text.see(
            "insert"
        )
        self.highlight_current_line()

        return "break"
    def confirm_discard(
        self
    ):

        if not self.modified:

            return True

        answer = messagebox.askyesnocancel(

            "Unsaved Changes",

            "Do you want to save your changes?"

        )

        if answer is None:

            return False

        if answer:

            self.save()

            if self.modified:

                return False

        return True
    def update_status(
        self,
        event=None
    ):

        cursor = self.text.index(
            "insert"
        )

        line, column = cursor.split(
            "."
        )

        if self.file_path:

            name = os.path.basename(
                self.file_path
            )

        else:

            name = "Untitled"

        text = (
            f"{name}    "
            f"Ln {line}    "
            f"Col {int(column)+1}"
        )

        if self.modified:

            text += "    Modified"

        self.status.config(
            text=text
        )
    def text_modified(
        self,
        event=None
    ):

        if self.text.edit_modified():

            self.modified = True

            self.text.edit_modified(
                False
            )

            self.update_status()

            self.update_line_numbers()
    def update_line_numbers(
        self,
        event=None
    ):

        self.line_numbers.config(
            state="normal"
        )

        self.line_numbers.delete(
            "1.0",
            tk.END
        )

        lines = int(

            self.text.index(
                "end-1c"
            ).split(".")[0]

        )

        content = "\n".join(

            str(i)

            for i in range(
                1,
                lines + 1
            )

        )

        self.line_numbers.insert(
            "1.0",
            content
        )

        self.line_numbers.config(
            state="disabled"
        )
    def zoom_in(
        self
    ):

        self.font_size += 1

        self.editor_font.configure(

            size=self.font_size

        )

    def zoom_out(
        self
    ):

        if self.font_size <= 7:

            return

        self.font_size -= 1

        self.editor_font.configure(

            size=self.font_size

        )
    def toggle_wrap(
        self
    ):

        self.wrap = not self.wrap

        if self.wrap:

            self.text.config(
                wrap="word"
            )

            self.h_scroll.grid_remove()

        else:

            self.text.config(
                wrap="none"
            )

            self.h_scroll.grid()

    def find_text(
        self
    ):

        word = simpledialog.askstring(
            "Find",
            "Find:"
        )

        if not word:

            return

        self.text.tag_remove(
            "search",
            "1.0",
            "end"
        )

        start = "1.0"

        while True:

            pos = self.text.search(
                word,
                start,
                stopindex="end"
            )

            if not pos:

                break

            end = f"{pos}+{len(word)}c"

            self.text.tag_add(
                "search",
                pos,
                end
            )

            start = end

        self.text.tag_config(
            "search",
            background="#d18616",
            foreground="black"
        )

    def replace_text(
        self
    ):

        old = simpledialog.askstring(
            "Replace",
            "Find:"
        )

        if old is None:

            return

        new = simpledialog.askstring(
            "Replace",
            "Replace with:"
        )

        if new is None:

            return

        text = self.text.get(
            "1.0",
            "end-1c"
        )

        text = text.replace(
            old,
            new
        )

        self.text.delete(
            "1.0",
            "end"
        )

        self.text.insert(
            "1.0",
            text
        )

        self.modified = True

        self.update_status()

        self.update_line_numbers()
    def highlight_current_line(
        self,
        event=None
    ):

        self.text.tag_remove(
            "current_line",
            "1.0",
            "end"
        )

        self.text.tag_add(
            "current_line",
            "insert linestart",
            "insert lineend+1c"
        )

        self.text.tag_configure(
            "current_line",
            background="#2b2b2b"
        )
    def blink_cursor(
        self
    ):

        self.text.config(

            insertbackground="#ffffff",

            insertwidth=2,

            insertontime=600,

            insertofftime=400

        )
    def show_find_bar(
        self
    ):

        self.find_frame.pack(
            fill="x",
            before=self.status
        )

        self.find_entry.focus_set()

        self.find_entry.select_range(
            0,
            tk.END
        )

    def hide_find_bar(
        self
    ):

        self.text.tag_remove(
            "search",
            "1.0",
            tk.END
        )

        self.find_frame.pack_forget()

        self.text.focus_set()
    def update_search(
        self,
        event=None
    ):

        self.text.tag_remove(
            "search",
            "1.0",
            tk.END
        )

        word = self.find_var.get()

        if not word:

            self.match_label.config(
                text="0 Matches"
            )

            return

        start = "1.0"

        count = 0

        while True:

            pos = self.text.search(
                word,
                start,
                stopindex=tk.END
            )

            if not pos:

                break

            end = f"{pos}+{len(word)}c"

            self.text.tag_add(
                "search",
                pos,
                end
            )

            start = end

            count += 1

        self.text.tag_configure(
            "search",
            background="#d18616",
            foreground="black"
        )

        self.match_label.config(
            text=f"{count} Match(es)"
        )
    def find_next(
        self
    ):

        word = self.find_var.get()

        if not word:

            return

        start = self.text.index(
            "insert+1c"
        )

        pos = self.text.search(
            word,
            start,
            stopindex=tk.END
        )

        if not pos:

            pos = self.text.search(
                word,
                "1.0",
                stopindex=tk.END
            )

            if not pos:

                return

        end = f"{pos}+{len(word)}c"

        self.text.tag_remove(
            "sel",
            "1.0",
            tk.END
        )

        self.text.tag_add(
            "sel",
            pos,
            end
        )

        self.text.mark_set(
            "insert",
            end
        )

        self.text.see(
            pos
        )

        self.update_status()
    def find_previous(
        self
    ):

        word = self.find_var.get()

        if not word:

            return

        current = self.text.index(
            "insert"
        )

        pos = "1.0"

        last = None

        while True:

            found = self.text.search(
                word,
                pos,
                stopindex=current
            )

            if not found:

                break

            last = found

            pos = f"{found}+1c"

        if last is None:

            return

        end = f"{last}+{len(word)}c"

        self.text.tag_remove(
            "sel",
            "1.0",
            tk.END
        )

        self.text.tag_add(
            "sel",
            last,
            end
        )

        self.text.mark_set(
            "insert",
            end
        )

        self.text.see(
            last
        )

        self.update_status()
    def replace_current(
        self
    ):

        if not self.text.tag_ranges(
            "sel"
        ):

            return

        selected = self.text.get(
            "sel.first",
            "sel.last"
        )

        if selected != self.find_var.get():

            return

        self.text.delete(
            "sel.first",
            "sel.last"
        )

        self.text.insert(
            "insert",
            self.replace_var.get()
        )

        self.modified = True

        self.update_search()

        self.update_status()
    def replace_all(
        self
    ):

        find = self.find_var.get()

        if not find:

            return

        replace = self.replace_var.get()

        content = self.text.get(
            "1.0",
            "end-1c"
        )

        content = content.replace(
            find,
            replace
        )

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            "1.0",
            content
        )

        self.modified = True

        self.update_line_numbers()

        self.update_search()

        self.update_status()