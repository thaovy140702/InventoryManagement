import random
import string
from tkinter import ttk
import pandas as pd
import tkinter as tk

def switch_mode(switch, root):
    if switch.instate(["selected"]):
        root.tk.call("set_theme", "dark")
        text = "Switch Light Mode"
    else:
        root.tk.call("set_theme", "light")
        text = "Switch Dark Mode"
    switch.configure(text=text)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    x_cordinate = int((window.winfo_screenwidth() - width) / 2)
    y_cordinate = int((window.winfo_screenheight() - height) / 2)

    window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

def create_treeview(parent, columns):
    treeFrame = ttk.Frame(parent)
    treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

    # Scrollbar
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")

    # Treeview
    treeview = ttk.Treeview(treeFrame, show="headings", selectmode="extended", yscrollcommand=treeScroll.set, columns=columns, height=12)
    treeview.pack(expand=True, fill="both")
    treeScroll.config(command=treeview.yview)

    for col in columns:
        treeview.column(col, anchor="center",width=120)
        treeview.heading(col, text=col)

    return treeview

def generate_random_id(size):
    random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
    return random_id

def load_data(path, treeview):
    df = pd.read_csv(path, sep=';')
    columns = tuple(df.columns)
    data = [columns] + [tuple(x) for x in df.to_records(index=False)]

    for col_name in data[0]:
        treeview.heading(col_name, text=col_name)
    
    for value in data[1:]:
        treeview.insert('', tk.END, values=value)