# this file is to do a final test of text_editor.py
import tkinter as tk

root = tk.Tk()
root.geometry("600x400")

text = tk.Text(root)
text.pack(fill="both", expand=True)

root.mainloop()