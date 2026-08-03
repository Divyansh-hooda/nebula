import tkinter as tk
import os
import core.config as config
import core.database as database
from ui.legacy_ui import Nebula
from core.clipboard_manager import ClipboardManager

os.makedirs(config.VAULT_DIR,exist_ok=True)
os.makedirs(config.LOG_DIR,exist_ok=True)
database.initialize()
clipboard = ClipboardManager()
root=tk.Tk()
app=Nebula(root, clipboard)
root.mainloop()