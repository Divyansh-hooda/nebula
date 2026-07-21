import tkinter as tk
import os
import config
import database
from ui import Nebula
from clipboard_manager import ClipboardManager

os.makedirs(config.VAULT_DIR,exist_ok=True)
os.makedirs(config.LOG_DIR,exist_ok=True)
database.initialize()
clipboard = ClipboardManager()
root=tk.Tk()
app=Nebula(root, clipboard)
root.mainloop()