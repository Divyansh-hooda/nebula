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
