import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import shutil
import os
import sys
import subprocess
import config
import database
import utils

class Nebula:
    def __init__(self, root, clipboard):
        self.root = root
        self.clipboard = clipboard
        self.root.title(config.APP_NAME)
        self.root.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )
        self.root.configure(bg=config.BACKGROUND)
        self.history = []
        self.current = os.path.expanduser("~")
        self.make_ui()
        self.load(self.current)
    def make_ui(self):
        self.root.bind(
            "<Control-c>",
            lambda e: self.copy_item()
        )

        self.root.bind(
            "<Control-x>",
            lambda e: self.cut_item()
        )

        self.root.bind(
            "<Control-v>",
            lambda e: self.paste_item()
        )

        self.root.bind(
            "<F5>",
            lambda e: self.load(
                self.current,
                False
            )
        )
        top = tk.Frame(
            self.root,
            bg=config.TOPBAR,
            height=50
        )
        top.pack(fill="x")
        tk.Button(
            top,
            text="← Back",
            command=self.go_back
        ).pack(side="left", padx=4, pady=5)
        tk.Button(
            top,
            text="🏠 Home",
            command=self.go_home
        ).pack(side="left", padx=4)
        tk.Button(
            top,
            text="⟳ Refresh",
            command=lambda: self.load(self.current, False)
        ).pack(side="left", padx=4)
        self.path = tk.Entry(top)
        self.path.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )
        tk.Button(
            top,
            text="Go",
            command=self.goto
        ).pack(side="left", padx=5)
        self.tree = ttk.Treeview(
            self.root,
            columns=("name", "size", "type"),
            show="headings"
        )
        self.tree.heading("name", text="Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("type", text="Type")
        self.tree.column("name", width=650)
        self.tree.column("size", width=120)
        self.tree.column("type", width=120)
        self.tree.pack(
            fill="both",
            expand=True
        )
        self.tree.bind("<Double-1>", self.open_selected)
        self.tree.bind("<Button-3>", self.show_menu)

        self.menu = tk.Menu(
            self.root,
            tearoff=False
        )

        self.menu.add_command(
            label="Open",
            command=self.menu_open
        )

        self.menu.add_separator()

        self.menu.add_command(
            label="New Folder",
            command=self.new_folder
        )

        self.menu.add_command(
            label="Rename",
            command=self.rename_item
        )

        self.menu.add_command(
            label="Delete",
            command=self.delete_item
        )

        self.menu.add_separator()

        self.menu.add_command(
            label="Refresh",
            command=lambda: self.load(self.current, False)
        )
    def goto(self):
        path = self.path.get()
        if os.path.isdir(path):
            self.load(path)
        else:
            messagebox.showerror(
                "Error",
                "Folder not found."
            )
    def go_home(self):
        self.load(os.path.expanduser("~"))
    def go_back(self):
        if len(self.history) < 2:
            return
        self.history.pop()
        previous = self.history.pop()
        self.load(previous)
    def load(self, folder, remember=True):
        if not os.path.isdir(folder):
            return
        if remember:
            self.history.append(folder)
        self.current = folder
        self.path.delete(0, tk.END)
        self.path.insert(0, folder)
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            files = sorted(os.listdir(folder))
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
            return
        for name in files:
            full = os.path.join(folder, name)
            if os.path.isdir(full):
                ftype = "Folder"
                size = "-"
            else:
                ftype = "File"
                try:
                    size = utils.bytes_to_size(
                        os.path.getsize(full)
                    )
                except Exception:
                    size = "?"
            self.tree.insert(
                "",
                tk.END,
                values=(name, size, ftype)
            )
    def open_selected(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item)["values"]
        if not values:
            return
        name = values[0]
        full = os.path.join(
            self.current,
            name
        )
        if os.path.isdir(full):
            database.log(
                "Open Folder",
                full
            )
            self.load(full)
            return
        database.log(
            "Open File",
            full
        )
        self.open_file(full)
    def open_file(self, path):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
    def selected_path(self):
        item = self.tree.focus()
        if not item:
            return None
        values = self.tree.item(item)["values"]
        if not values:
            return None
        return os.path.join(
            self.current,
            values[0]
        )
    def show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tree.focus(item)
        self.menu.post(
            event.x_root,
            event.y_root
        )
    def menu_open(self):
        path = self.selected_path()
        if not path:
            return
        if os.path.isdir(path):
            self.load(path)
        else:
            self.open_file(path)
    def new_folder(self):
        name = simpledialog.askstring(
            "New Folder",
            "Folder name:"
        )
        if not name:
            return
        path = os.path.join(
            self.current,
            name
        )
        try:
            os.mkdir(path)
            database.log(
                "Create Folder",
                path
            )
            self.load(self.current, False)
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
    def rename_item(self):

        path = self.selected_path()

        if not path:
            return

        old = os.path.basename(path)

        new = simpledialog.askstring(
            "Rename",
            "New Name:",
            initialvalue=old
        )

        if not new:
            return

        new_path = os.path.join(
            self.current,
            new
        )

        try:

            os.rename(
                path,
                new_path
            )

            database.log(
                "Rename",
                new_path
            )

            self.load(self.current, False)

        except Exception as e:

            messagebox.showerror(
                "Rename Failed",
                str(e)
            )


    def delete_item(self):

        path = self.selected_path()

        if not path:
            return

        ok = messagebox.askyesno(
            "Delete",
            f"Delete\n\n{os.path.basename(path)} ?"
        )

        if not ok:
            return

        try:

            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

            database.log(
                "Delete",
                path
            )

            self.load(self.current, False)

        except Exception as e:

            messagebox.showerror(
                "Delete Failed",
                str(e)
            )