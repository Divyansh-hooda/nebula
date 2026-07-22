import os
import sys
import time
import shutil
import subprocess
import tkinter as tk
import threading
from queue import Queue
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import config
import database
import utils
class Nebula:
    def __init__(self, root, clipboard):
        self.root = root
        self.clipboard = clipboard
        self.current = os.path.expanduser("~")
        self.history = []
        self.selected = None
        self.favorites = database.get_bookmarks()
        self.favorite_buttons = []
        self.recent_folders = []
        self.max_recent = 10
        self.load_queue = Queue()
        self.loading = False
        self.root.title(config.APP_NAME)
        self.root.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )
        self.root.configure(
            bg=config.BACKGROUND
        )
        self.make_ui()
        database.create_bookmark_table()
        self.load(self.current)
        self.refresh_favorites()
        self.refresh_favorites()
    def make_ui(self):
        self.top = tk.Frame(
            self.root,
            bg=config.TOPBAR,
            height=45
        )
        self.top.pack(
            fill="x"
        )
        self.back_btn = tk.Button(
            self.top,
            text="←",
            width=4,
            command=self.go_back
        )
        self.back_btn.pack(
            side="left",
            padx=4,
            pady=5
        )
        self.home_btn = tk.Button(
            self.top,
            text="🏠",
            width=4,
            command=self.go_home
        )
        self.home_btn.pack(
            side="left"
        )
        self.refresh_btn = tk.Button(
            self.top,
            text="⟳",
            width=4,
            command=lambda: self.load(
                self.current,
                False
            )
        )
        self.refresh_btn.pack(
            side="left",
            padx=4
        )
        self.path = tk.Entry(self.top, font=config.FONT)
        self.path.pack(side="left", fill="x", expand=True, padx=8)

        self.go_btn = tk.Button(self.top, text="Go", command=self.goto)
        self.go_btn.pack(side="left", padx=5)

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            self.top,
            textvariable=self.search_var,
            width=30
        )

        self.search_entry.pack(side="right", padx=10)

        self.search_var.trace_add(
            "write",
            self.live_search
        )
        self.go_btn.pack(
            side="left",
            padx=5
        )
        self.body = tk.Frame(
            self.root,
            bg=config.BACKGROUND
        )
        self.body.pack(
            fill="both",
            expand=True
        )
        self.sidebar = tk.Frame(
            self.body,
            bg=config.SIDEBAR,
            width=220
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        title = tk.Label(
            self.sidebar,
            text="Project Nebula",
            bg=config.SIDEBAR,
            fg="white",
            font=config.BIG_FONT
        )
        title.pack(
            pady=15
        )
        tk.Label(
            self.sidebar,
            text="Favorites",
            bg=config.SIDEBAR,
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))

        self.favorite_frame = tk.Frame(
            self.sidebar,
            bg=config.SIDEBAR
        )

        self.favorite_frame.pack(
            fill="x",
            padx=5
        )
        tk.Label(
            self.sidebar,
            text="Recent",
            bg=config.SIDEBAR,
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=(15, 5))

        self.recent_frame = tk.Frame(
            self.sidebar,
            bg=config.SIDEBAR
        )

        self.recent_frame.pack(
            fill="x",
            padx=5
        )

        self.recent_buttons = []
        self.home_side = tk.Button(
            self.sidebar,
            text="🏠 Home",
            anchor="w",
            command=self.go_home
        )
        self.home_side.pack(
            fill="x",
            padx=8,
            pady=2
        )
        self.desktop_side = tk.Button(
            self.sidebar,
            text="🖥 Desktop",
            anchor="w",
            command=lambda:
            self.load(
                os.path.join(os.path.expanduser("~"),"Desktop")
            )
        )
        self.desktop_side.pack(
            fill="x",
            padx=8,
            pady=2
        )
        self.documents_side = tk.Button(
            self.sidebar,
            text="📄 Documents",
            anchor="w",
            command=lambda:
            self.load(
                os.path.join(
                    os.path.expanduser("~"),
                    "Documents"
                )
            )
        )
        self.documents_side.pack(
            fill="x",
            padx=8,
            pady=2
        )
        self.downloads_side = tk.Button(
            self.sidebar,
            text="⬇ Downloads",
            anchor="w",
            command=lambda:
            self.load(
                os.path.join(
                    os.path.expanduser("~"),
                    "Downloads"
                )
            )
        )
        self.downloads_side.pack(
            fill="x",
            padx=8,
            pady=2
        )
        self.center = tk.Frame(
            self.body
        )
        self.center.pack(
            side="left",
            fill="both",
            expand=True
        )
        self.tree = ttk.Treeview(
            self.center,
            columns=(
                "name",
                "size",
                "type"
            ),
            show="headings"
        )
        self.tree.heading(
            "name",
            text="Name"
        )
        self.tree.heading(
            "size",
            text="Size"
        )
        self.tree.heading(
            "type",
            text="Type"
        )
        self.tree.column(
            "name",
            width=500
        )
        self.tree.column(
            "size",
            width=120
        )
        self.tree.column(
            "type",
            width=120
        )
        self.tree.pack(
            fill="both",
            expand=True
        )
        self.tree.bind(
            "<Double-1>",
            self.open_selected
        )
        self.tree.bind(
            "<Button-3>",
            self.show_menu
        )
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
        self.menu.add_separator()
        self.menu.add_command(
            label="Copy",
            command=self.copy_item
        )
        self.menu.add_command(
            label="Cut",
            command=self.cut_item
        )
        self.menu.add_command(
            label="Paste",
            command=self.paste_item
        )
        self.menu.add_separator()
        self.menu.add_command(
            label="Delete",
            command=self.delete_item
        )

        self.menu.add_separator()

        self.menu.add_command(
            label="Properties",
            command=self.properties
        )

        self.menu.add_command(
            label="Add to Favorites",
            command=self.add_favorite
        )
        self.menu.add_command(
            label="Remove Favorite",
            command=self.remove_favorite
        )
        self.menu.add_command(
            label="Remove Favorite",
            command=self.remove_favorite
        )
        self.menu.add_separator()

        self.menu.add_command(
            label="Refresh",
            command=lambda: self.load(
                self.current,
                False
            )
        )
        self.status = tk.Frame(
            self.root,
            bd=1,
            relief="sunken"
        )

        self.status.pack(fill="x")

        self.status_left = tk.Label(
            self.status,
            text="Ready",
            anchor="w"
        )

        self.status_left.pack(
            side="left",
            padx=5
        )

        self.status_right = tk.Label(
            self.status,
            text="0 Items",
            anchor="e"
        )

        self.status_right.pack(
            side="right",
            padx=5
        )
        self.root.bind(
            "<Control-c>",
            lambda e:
            self.copy_item()
        )
        self.root.bind(
            "<Control-x>",
            lambda e:
            self.cut_item()
        )
        self.root.bind(
            "<Control-v>",
            lambda e:
            self.paste_item()
        )
        self.root.bind(
            "<F5>",
            lambda e:
            self.load(
                self.current,
                False
            )
        )
        self.root.bind("<Delete>", lambda e: self.delete_item())
        self.root.bind("<F2>", lambda e: self.rename_item())
        self.root.bind("<Return>", lambda e: self.open_selected())
        self.root.bind("<Control-n>", lambda e: self.new_folder())
        self.root.bind("<Alt-Return>", lambda e: self.properties())
    def goto(self):
        path = self.path.get().strip()
        if not path:
            return
        if os.path.isdir(path):
            self.load(path)
        else:
            messagebox.showerror(
                "Error",
                "Folder does not exist."
            )
    def go_home(self):
        self.load(
            os.path.expanduser("~")
        )
    def go_back(self):
        if len(self.history) <= 1:
            return
        self.history.pop()
        previous = self.history.pop()
        self.load(previous)
    def load(self, folder, remember=True):
        if self.loading:
            return
        self.loading = True
        self.status_left.config(text="Loading...")
        thread = threading.Thread(
            target=self.load_worker,
            args=(folder, remember),
            daemon=True
        )
        thread.start()
        self.root.after(100, self.check_queue)
    def load_worker(self, folder, remember=True):
        if not os.path.exists(folder):
            return
        if remember:
            self.history.append(folder)
        self.current = folder
        self.add_recent(folder)
        self.path.delete(
            0,
            tk.END
        )
        self.path.insert(
            0,
            folder
        )
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            files = sorted(
                os.listdir(folder),
                key=str.lower
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )
            return
        folders = []
        normal_files = []
        for name in files:
            full = os.path.join(
                folder,
                name
            )
            if os.path.isdir(full):
                folders.append(full)
            else:
                normal_files.append(full)
        for full in folders + normal_files:
            name = os.path.basename(full)
            if os.path.isdir(full):
                size = "-"
                typ = "Folder"
            else:
                typ = "File"
                try:
                    size = utils.bytes_to_size(
                        os.path.getsize(full)
                    )
                except:
                    size = "?"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    name,
                    size,
                    typ
                )
            )
        self.load_queue.put({
            "folder": folder,
            "count": len(files)
        })
    def check_queue(self):
        try:
            data = self.load_queue.get_nowait()
        except:
            self.root.after(100, self.check_queue)
            return

        self.status_left.config(text=data["folder"])
        self.status_right.config(text=f'{data["count"]} item(s)')
        self.loading = False
    def selected_path(self):
        item = self.tree.focus()
        if not item:
            return None
        values = self.tree.item(
            item
        )["values"]
        if not values:
            return None
        return os.path.join(
            self.current,
            values[0]
        )
    def open_selected(
        self,
        event=None
    ):
        path = self.selected_path()
        if not path:
            return
        if os.path.isdir(path):
            database.log(
                "Open Folder",
                path
            )
            self.load(path)
            return
        database.log(
            "Open File",
            path
        )
        self.open_file(path)
    def menu_open(self):
        self.open_selected()
    def open_file(
        self,
        path
    ):
        try:
            if sys.platform.startswith(
                "win"
            ):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(
                    ["open", path],
                    check=False
                )
            else:
                subprocess.run(
                    ["xdg-open", path],
                    check=False
                )
        except Exception as e:
            messagebox.showerror(
                "Open Error",
                str(e)
            )
    def show_menu(
        self,
        event
    ):
        row = self.tree.identify_row(
            event.y
        )
        if row:
            self.tree.selection_set(row)
            self.tree.focus(row)
        self.menu.tk_popup(
            event.x_root,
            event.y_root
        )
    def new_folder(self):
        name = simpledialog.askstring("New Folder", "Folder name:")
        if not name:
            return
        path = os.path.join(self.current, name)
        try:
            os.mkdir(path)
            database.log("Create Folder", path)
            self.load(self.current, False)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def rename_item(self):
        path = self.selected_path()
        if not path:
            return
        old_name = os.path.basename(path)
        new_name = simpledialog.askstring("Rename", "New name:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        new_path = os.path.join(self.current, new_name)
        try:
            os.rename(path, new_path)
            database.log("Rename", f"{old_name} -> {new_name}")
            self.load(self.current, False)
        except Exception as e:
            messagebox.showerror("Rename Failed", str(e))
    def delete_item(self):
        path = self.selected_path()
        if not path:
            return
        confirm = messagebox.askyesno("Delete", f"Delete '{os.path.basename(path)}'?")
        if not confirm:
            return
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            database.log("Delete", path)
            self.load(self.current, False)
        except Exception as e:
            messagebox.showerror("Delete Failed", str(e))
    def copy_item(self):
        path = self.selected_path()
        if not path:
            return
        self.clipboard.copy(path)
        database.log("Copy", path)
        self.status_left.config(
            text=f"Copied: {os.path.basename(path)}"
        )
    def cut_item(self):
        path = self.selected_path()
        if not path:
            return
        self.clipboard.cut(path)
        database.log("Cut", path)
        self.status_left.config(
            text=f"Cut: {os.path.basename(path)}"
        )
    def paste_item(self):
        success, result = self.clipboard.paste(self.current)
        if success:
            database.log("Paste", result)
            self.load(self.current, False)
            self.status_left.config(
                text="Paste completed"
            )
        else:
            messagebox.showerror("Paste", result)
    def live_search(self, *args):
        query = self.search_var.get().lower().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            files = sorted(os.listdir(self.current), key=str.lower)
        except:
            return
        for name in files:
            if query not in name.lower():
                continue
            full = os.path.join(self.current, name)
            if os.path.isdir(full):
                size = "-"
                typ = "Folder"
            else:
                typ = "File"
                try:
                    size = utils.bytes_to_size(os.path.getsize(full))
                except:
                    size = "?"
            self.tree.insert("", "end", values=(name, size, typ))
