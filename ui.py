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
