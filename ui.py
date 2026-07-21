import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

import config
import database
import utils

class Nebula:
    def __init__(self, root):
        self.root=root
        self.root.title(config.APP_NAME)
        self.root.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )
        self.root.configure(bg=config.BACKGROUND)
        self.current=os.path.expanduser("~")
        self.make_ui()
        self.load(self.current)

