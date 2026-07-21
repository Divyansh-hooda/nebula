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

    def make_ui(self):
        self.top = tk.Frame(self.root, bg=config.TOPBAR, height = 50)
        self.top.pack(fill="x")
        self.path=tk.Entry(
            self.top,
            font=config.FONT
        )
        self.path.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )
        go=tk.Button(
            self.top,
            text="Go",
            command=self.goto
        )
        go.pack(side="left",padx=5)
        self.tree=ttk.Treeview(
            self.root,
            columns=("size","type"),
            show="headings"
        )
        self.tree.heading("size",text="Size")
        self.tree.heading("type",text="Type")
        self.tree.pack(
            fill="both",
            expand=True
        )
        self.tree.bind("<Double-1>",self.open)
        def goto(self):
            p=self.path.get()
            if os.path.exists(p):
                self.load(p)
            else:
                messagebox.showerror(
                    "Error",
                    "Folder not found"
                )
        def load(self,path):
            self.current=path
            self.path.delete(0,"end")
            self.path.insert(0,path)
            for i in self.tree.get_children():
                self.tree.delete(i)
            try:
                files=os.listdir(path)
            except:
                return
            for file in files:
                full=os.path.join(path,file)
                if os.path.isdir(full):
                    type="folder"
                    size="-"
                else:
                    type="file"
                    size=utils.bytes_to_size(
                        os.path.getsize(full)
                    )
                self.tree.insert(
                    "",
                    "end",
                    values=(file,size,typ)
                )
        def open(self,event):
            item=self.tree.focus()
            if not item:
                return
            vals=self.tree.item(item)["values"]
            name=vals[0]
            full=os.path.join(
                self.current,
                name
            )
            if os.path.isdir(full):
                database.log(
                    "open Folder",
                    full
                )
                self.load(full)
            else:
                os.startfile(full)