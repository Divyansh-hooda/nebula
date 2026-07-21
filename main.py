import tkinter as tk
import os
import config
import database
from ui import Nebula

os.makedirs(config.VAULT_DIR,exist_ok=True)
os.makedirs(config.LOG_DIR,exist_ok=True)
database.initialize()
root=tk.Tk()
app=Nebula(root)
root.mainloop()