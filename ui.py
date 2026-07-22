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
