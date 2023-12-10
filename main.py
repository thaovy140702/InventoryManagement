import tkinter as tk
from tkinter import ttk
import tkinter.font 
import pandas as pd
from tkinter import simpledialog
from uiconfig import center_window, generate_random_id, create_treeview, load_data, switch_mode
from PIL import Image, ImageTk
from inventory import Inventory
from product import Product
from tkinter import filedialog
import os
from datetime import datetime
from tkinter import messagebox
from tkinter import StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from tkinter import PhotoImage



def add_inventory():
    # Open a dialog window for adding a new item
    new_item_window = simpledialog.Toplevel(root)
    new_item_window.title("Add New Inventory")
    new_item_window.configure(bg="white")
    new_item_window.resizable(False, False)
    center_window(new_item_window)

    # Create labels and entry widgets for input
    label_name = ttk.Label(new_item_window, text="Inventory Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    entry_name = ttk.Entry(new_item_window)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    label_price = ttk.Label(new_item_window, text="Address:         ")
    label_price.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_address = ttk.Entry(new_item_window)
    entry_address.grid(row=1, column=1, padx=5, pady=5)

    # Function to handle adding the new item
    def save_item():
        # Get values from entry widgets
        item_name = entry_name.get()
        address = entry_address.get()
        random_id = generate_random_id(4)

        file_path = './data/inventory.csv'
        df = pd.read_csv(file_path, delimiter=';')

        new_inventory = Inventory(name=item_name, address=address)

        new_row = {
            "Id": random_id,
            "Inventory Name": new_inventory.name,
            "Address": new_inventory.address,
            "Created_at": new_inventory.created_at,
            "Updated_at": new_inventory.updated_at
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(file_path, sep=';', index=False)

        # Insert the new values into the treeview
        values = [random_id, new_inventory.name, new_inventory.address, new_inventory.created_at, new_inventory.updated_at]
        inventory_treeview.insert('', tk.END, values=values)
        new_item_window.destroy()

    save_button = ttk.Button(new_item_window, text="Save", style="Accent.TButton", command=save_item)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)


def add_product():
    new_item_window = simpledialog.Toplevel(root)
    new_item_window.title("Add New Product")
    new_item_window.configure(bg="white")
    new_item_window.resizable(False, False)
    center_window(new_item_window)

    file_path = './data/inventory.csv'
    df = pd.read_csv(file_path, delimiter=';')

    def upload_image(label):
        global path
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
            # Compute the relative path
            relative_path = os.path.relpath(file_path, base_path)

            image = Image.open(file_path)
            image = image.resize((35, 35), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            path = relative_path

            label.config(image=photo)
            label.image = photo
        

    # Create labels and entry widgets for input
    label_name = ttk.Label(new_item_window, text="Product Name:")
    label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    entry_name = ttk.Entry(new_item_window)
    entry_name.grid(row=0, column=1, padx=5, pady=5)
    entry_name.configure(width=27)

    label_price = ttk.Label(new_item_window, text="Unit price: ")
    label_price.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    spin_price = ttk.Spinbox(new_item_window, from_=0, to=100)
    spin_price.configure(width=27)
    spin_price.grid(row=1, column=1, padx=5, pady=5)

    label_quantity = ttk.Label(new_item_window, text="Quantity: ")
    label_quantity.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    spin_quantity = ttk.Spinbox(new_item_window, from_=0, to=100)
    spin_quantity.configure(width=27)
    spin_quantity.grid(row=2, column=1, padx=5, pady=5)

    label_category = ttk.Label(new_item_window, text="Category: ")
    label_category.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    entry_category = ttk.Entry(new_item_window)
    entry_category.grid(row=3, column=1, padx=5, pady=5)
    entry_category.configure(width=27)

    label_inventory = ttk.Label(new_item_window, text="Inventory: ")
    label_inventory.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    inventory_list = list(df['Inventory Name'])
    combobox_inventory = ttk.Combobox(new_item_window, values=inventory_list)
    combobox_inventory.current(0)
    combobox_inventory.grid(row=4, column=1, padx=5, pady=10,  sticky="ew")

    label_upload = ttk.Label(new_item_window, text="Image: ")
    label_upload.grid(row=5, column=0, padx=5, pady=5, sticky="e")

    image_label = tk.Label(new_item_window)
    image_label.grid(row=5, column=1, padx=5, pady=5, sticky="e")

    upload_button = ttk.Button(new_item_window, text="Choose image", command=lambda:upload_image(image_label))
    upload_button.grid(row=5, column=1, padx=5, pady=10, sticky="w")

    # Function to handle adding the new item
    def save_item():
        # Get values from entry widgets
        item_name = entry_name.get()
        random_id = generate_random_id(5)
        price = spin_price.get()
        quantity = spin_quantity.get()
        category = entry_category.get()
        inventory = combobox_inventory.get()

        df = pd.read_csv('./data/inventory.csv', delimiter=';')
        filtered_df = df[df['Inventory Name'] == inventory]
        inventory_id = filtered_df.iloc[0]['Id']
        
        file_path = './data/items.csv'
        df = pd.read_csv(file_path, delimiter=';')

        new_product = Product(product_name=item_name, unit_price=price,quantity=quantity, category=category, inventory=inventory_id)

        new_row = {
            "Id": random_id,
            "Product Name": new_product.name,
            "Unit Price": new_product.price,
            "Quantity": new_product.quantity,
            "Created_at": new_product.created_at,
            "Updated_at": new_product.updated_at,
            "Category": new_product.category,
            "Inventory": new_product.inventory,
            "Image": path
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(file_path, sep=';', index=False)

        product_treeview.image_list = []

        img = Image.open(path).resize((40, 40), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Insert the new values into the treeview
        product_treeview.image_list.append(img)
        values = [random_id, new_product.name, new_product.price, new_product.quantity, new_product.created_at, new_product.updated_at, new_product.category, new_product.inventory]
        product_treeview.insert('', tk.END, values=values, image=img)
        new_item_window.destroy()


    save_button = ttk.Button(new_item_window, text="Save", style="Accent.TButton", command=save_item)
    save_button.grid(row=7, column=0, columnspan=2, pady=10)

def edit_inventory():
    selected_item = inventory_treeview.selection()
    if selected_item:
        # Get the values of the selected item
        item_values = inventory_treeview.item(selected_item, 'values')
        
        # Open a dialog window for editing the selected item
        edit_window = simpledialog.Toplevel(root)
        edit_window.title("Edit Inventory")
        edit_window.configure(bg="white")
        edit_window.resizable(False, False)
        center_window(edit_window)

        # Create labels and entry widgets for input
        label_name = ttk.Label(edit_window, text="Inventory Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        entry_name = ttk.Entry(edit_window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        entry_name.insert(0, item_values[1])  # Populate with current value

        label_address = ttk.Label(edit_window, text="Address:")
        label_address.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_address = ttk.Entry(edit_window)
        entry_address.grid(row=1, column=1, padx=5, pady=5)
        entry_address.insert(0, item_values[2])  # Populate with current value

        # Function to handle editing the item
        def save_item():
            # Get values from entry widgets
            new_name = entry_name.get()
            new_address = entry_address.get()

            # Update the data in the CSV file
            file_path = './data/inventory.csv'
            df = pd.read_csv(file_path, delimiter=';')
            df.loc[df['Id'] == item_values[0], 'Inventory Name'] = new_name
            df.loc[df['Id'] == item_values[0], 'Address'] = new_address
            df.to_csv(file_path, sep=';', index=False)

            # Update the treeview with the new values
            inventory_treeview.item(selected_item, values=(item_values[0], new_name, new_address, item_values[3], item_values[4]))
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", style="Accent.TButton", command=save_item)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

def delete_inventory():
    selected_item = inventory_treeview.selection()
    if selected_item:
        # Get the ID of the selected inventory
        inventory_id = inventory_treeview.item(selected_item, 'values')[0]
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this inventory?")

        if confirmation:
            # Remove the selected inventory from the CSV file
            file_path = './data/inventory.csv'
            df = pd.read_csv(file_path, delimiter=';')
            df = df[df['Id'] != inventory_id]
            df.to_csv(file_path, sep=';', index=False)

            # Remove related products from the products CSV file
            product_file_path = './data/items.csv'
            product_df = pd.read_csv(product_file_path, delimiter=';')
            product_df = product_df[product_df['Inventory'] != inventory_id]
            product_df.to_csv(product_file_path, sep=';', index=False)

            # Update the treeview
            inventory_treeview.delete(selected_item)

def edit_product():
    selected_item = product_treeview.selection()

    if selected_item:

        def upload_image(label):
            global path
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

            if file_path:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
                # Compute the relative path
                relative_path = os.path.relpath(file_path, base_path)

                image = Image.open(file_path)
                image = image.resize((35, 35), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                path = relative_path

                label.config(image=photo)
                label.image = photo
        
        # Get the values of the selected item
        item_values = product_treeview.item(selected_item, 'values')
        id = item_values[0]
        
        # Open a dialog window for editing the selected item
        edit_window = simpledialog.Toplevel(root)
        edit_window.title("Edit Product")
        edit_window.configure(bg="white")
        edit_window.resizable(False, False)
        center_window(edit_window)

        file_path = './data/inventory.csv'
        df_inventory = pd.read_csv(file_path, delimiter=';')
        df_items = pd.read_csv('./data/items.csv', delimiter=';')

        current_row = df_items[df_items['Id'] == id].values.tolist()

        
        # Create labels and entry widgets for input
        
        label_name = ttk.Label(edit_window, text="Product Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        entry_name = ttk.Entry(edit_window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        entry_name.configure(width=27)
        entry_name.insert(0, item_values[1])

        label_price = ttk.Label(edit_window, text="Unit price: ")
        label_price.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_price = ttk.Entry(edit_window)
        entry_price.grid(row=1, column=1, padx=5, pady=5)
        entry_price.configure(width=27)
        entry_price.insert(0, item_values[2])

        label_quantity = ttk.Label(edit_window, text="Quantity: ")
        label_quantity.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        spin_quantity = ttk.Spinbox(edit_window, from_=0, to=100)
        spin_quantity.grid(row=2, column=1, padx=5, pady=5)
        spin_quantity.configure(width=27)
        spin_quantity.insert(0, item_values[3])

        label_category = ttk.Label(edit_window, text="Category: ")
        label_category.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        entry_category = ttk.Entry(edit_window)
        entry_category.grid(row=3, column=1, padx=5, pady=5)
        entry_category.configure(width=27)
        entry_category.insert(0, current_row[0][6])

        label_inventory = ttk.Label(edit_window, text="Inventory: ")
        label_inventory.grid(row=4, column=0, padx=5, pady=5, sticky="e")


        filtered_df = df_items[df_items['Id'] == id]
        get_inventory_current_id = filtered_df.iloc[0]['Inventory']

        filtered_df = df_inventory[df_inventory['Id'] == get_inventory_current_id]
        inventory_name = filtered_df.iloc[0]['Inventory Name']
        
        inventory_list = list(df_inventory['Inventory Name'])
        combobox_inventory = ttk.Combobox(edit_window, values=inventory_list)
        combobox_inventory.set(inventory_name)
        combobox_inventory.grid(row=4, column=1, padx=5, pady=10,  sticky="ew")

        label_upload = ttk.Label(edit_window, text="Image: ")
        label_upload.grid(row=5, column=0, padx=5, pady=5, sticky="e")

        image_label = tk.Label(edit_window)
        image_label.grid(row=5, column=2, padx=5, pady=5, sticky="e")

        upload_button = ttk.Button(edit_window, text="Choose image", command=lambda:upload_image(image_label))
        upload_button.grid(row=5, column=1, padx=5, pady=10, sticky="w")


        # Function to handle editing the item
        def save_item():
            # Get values from entry widgets
            item_name = entry_name.get()
            price = entry_price.get()
            quantity = spin_quantity.get()
            category = entry_category.get()
            inventory = combobox_inventory.get()
            created_at = current_row[0][5]
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # Update the data in the CSV file
            file_path = './data/items.csv'
            df = pd.read_csv(file_path, delimiter=';')

            filtered_df = df_inventory[df_inventory['Inventory Name'] == inventory]
            inventory_id = filtered_df.iloc[0]['Id']    

            df.loc[df['Id'] == id, 'Product Name'] = item_name
            df.loc[df['Id'] == id, 'Unit Price'] = price
            df.loc[df['Id'] == id, 'Quantity'] = quantity
            df.loc[df['Id'] == id, 'Created_at'] = created_at
            df.loc[df['Id'] == id, 'Updated_at'] = updated_at
            df.loc[df['Id'] == id, 'Category'] = category
            df.loc[df['Id'] == id, 'Inventory'] = inventory_id
            df.loc[df['Id'] == id, 'Image'] = path

            df.to_csv(file_path, sep=';', index=False)

            product_treeview.image_list = []
            img = Image.open(path).resize((40, 40), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            product_treeview.image_list.append(img)
            # Update the treeview with the new values
            product_treeview.item(selected_item, values=(id, item_name, price, quantity, created_at, updated_at), image=img)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save", style="Accent.TButton", command=save_item)
        save_button.grid(row=7, column=0, columnspan=2, pady=10)

def delete_product():
    selected_item = product_treeview.selection()
    if selected_item:
        # Get the ID of the selected product
        product_id = product_treeview.item(selected_item, 'values')[0]
        
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")

        if confirmation:
            # Remove the selected product from the CSV file
            file_path = './data/items.csv'
            df = pd.read_csv(file_path, delimiter=';')
            df = df[df['Id'] != product_id]
            df.to_csv(file_path, sep=';', index=False)

            # Update the treeview
            product_treeview.delete(selected_item)

def search_record(treeview, file_path):
    lookup_record = entry.get().lower()
    for record in treeview.get_children():
        treeview.delete(record)
    search_data = pd.read_csv(file_path, sep=';')
    filtered_rows = search_data[search_data.apply(lambda row: row.astype(str).str.lower().str.contains(lookup_record).any(), axis=1)]
    row_tuples = [tuple(row) for row in filtered_rows.to_records(index=False)]

    if treeview == product_treeview:
        product_treeview.image_list = []
        for row in row_tuples:
            img = Image.open(row[-1]).resize((40, 40), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            product_treeview.image_list.append(img)
            values = [row[0], row[1], row[2], row[3], row[4], row[5]]
            product_treeview.insert('', index=tk.END, values=values, image=img)

    if treeview == inventory_treeview:
        for row in row_tuples:
            treeview.insert('', tk.END, values=row)

def on_tab_changed(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:
        combobox_category.grid_forget()
        combobox_inventory.grid_forget()
        combobox_inventory_static.grid_forget()
        entry.grid(row=1, column=3, sticky="w", padx=5, pady=10, columnspan=1)
        search_button.grid(row=1,column=3, sticky='e', pady = 10, columnspan=1)
        search_button_2.grid_forget()
    elif current_tab == 1:
        combobox_category.grid(row=1, column=2, padx=5, pady=10, sticky="w", columnspan=1)
        combobox_inventory.grid(row=1, column=1, padx=5, pady=10, sticky="w", columnspan=1)
        search_button_2.grid(row=1,column=3, sticky='e', pady = 10, columnspan=1)
        entry.grid(row=1, column=3, sticky="w", padx=5, pady=10, columnspan=1)
        search_button.grid_forget()
        combobox_inventory_static.grid_forget()
    elif current_tab == 2:
        combobox_inventory_static.grid(row=1, column=3, padx=5, pady=10, sticky="w", columnspan=1)
        entry.grid_forget()
        search_button.grid_forget()
        search_button_2.grid_forget()
        combobox_category.grid_forget()
        combobox_inventory.grid_forget()
# UI    
root = tk.Tk()
# pixels_per_inch = root.winfo_fpixels('1i')
root.title("Inventory Management Application")
root.iconbitmap('./data/images/favicon.ico')
root.option_add("*tearOff", False)

# Create a style
style = ttk.Style(root)

# Make the app responsive
default_font = ("Helvetica")
root.option_add("*Font", default_font)
root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")
style.configure("Combobox", fieldbackground= "orange", background= "white")
# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(sticky="nsew", rowspan=3)
paned.columnconfigure(index=0, weight=1)
paned.rowconfigure(index=0, weight=1)
paned.rowconfigure(index=1, weight=5)

pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)
pane_1.grid(row=0,sticky="nsew", rowspan=1)

pane_1.columnconfigure(index=0, weight=1)
pane_1.rowconfigure(index=0, weight=1)
pane_1.rowconfigure(index=1, weight=1)

# Create a font for the label
font = ("Segoe UI", 20, "bold") 
label = ttk.Label(pane_1, text="Inventory Management", font= font)
label.grid(row=0, column=0, pady=5, columnspan=4, sticky="n")

search_var = StringVar()
text = "Switch Dark Mode"
icon_image = PhotoImage(file="./data/images/search.png")
entry = ttk.Entry(pane_1, textvariable=search_var)
entry.configure(width=20)
entry.grid(row=1, column=3, sticky="w", padx=5, pady=10, columnspan=1)
search_button = ttk.Button(pane_1, image= icon_image, style="Accent.TButton", width=5, command=lambda:search_record(inventory_treeview,'./data/inventory.csv'))
search_button.grid(row=1,column=3, sticky='e', pady = 10, columnspan=1)
search_button_2 = ttk.Button(pane_1, image= icon_image, style="Accent.TButton", width=5, command=lambda:search_record(product_treeview,'./data/items.csv'))
search_button_2.grid(row=1,column=3, sticky='e', pady = 10, columnspan=1)

selected_inventory = tk.StringVar()

df_inventory = pd.read_csv('./data/inventory.csv', sep=';')

inventory_list = list(df_inventory['Inventory Name'])

combobox_inventory = ttk.Combobox(pane_1, values=inventory_list, textvariable=selected_inventory)
combobox_inventory.current(0)
combobox_inventory.grid(row=1, column=0, padx=5, pady=10,  sticky="w", columnspan=1)

combobox_category = ttk.Combobox(pane_1)
combobox_category.grid(row=1, column=1, padx=5, pady=10,  sticky="w", columnspan=1)

combobox_inventory_static = ttk.Combobox(pane_1, values=inventory_list)
combobox_inventory_static.current(0)
combobox_inventory_static.grid(row=1, column=2, padx=5, pady=10,  sticky="w", columnspan=1)

switch = ttk.Checkbutton(pane_1, text=text, style="Switch.TCheckbutton", command=lambda: switch_mode(switch, root))
switch.grid(row=1, column=4, sticky="e", padx=5)

combobox_inventory_static.bind("<<ComboboxSelected>>", lambda event: update_chart())

def update_category_combobox():
    selected_inventory_name = selected_inventory.get()
    if selected_inventory_name:
        df_inventory = pd.read_csv('./data/inventory.csv', delimiter=';')
        inventory_id = df_inventory[df_inventory['Inventory Name'] == selected_inventory_name].iloc[0]['Id']
        df_products = pd.read_csv('./data/items.csv', delimiter=';')
        categories = df_products[df_products['Inventory'] == inventory_id]['Category'].unique()
        
        combobox_category['values'] = list(categories)
        combobox_category.set(categories[0] if len(categories) > 0 else "")
    else:
        combobox_category.set("")

combobox_inventory.bind("<<ComboboxSelected>>", lambda event: update_category_combobox())
combobox_category.bind("<<ComboboxSelected>>", lambda event: update_product_treeview())


def update_product_treeview():
    selected_inventory_name = selected_inventory.get()
    selected_category = combobox_category.get()
    if selected_inventory_name and selected_category:
        # Get the products corresponding to the selected inventory and category
        df_inventory = pd.read_csv('./data/inventory.csv', delimiter=';')
        inventory_id = df_inventory[df_inventory['Inventory Name'] == selected_inventory_name].iloc[0]['Id']
        df_products = pd.read_csv('./data/items.csv', delimiter=';')
        filtered_df = df_products[(df_products['Inventory'] == inventory_id) & (df_products['Category'] == selected_category)]
        # Clear previous items in the product_treeview
        for item in product_treeview.get_children():
            product_treeview.delete(item)

        product_treeview.image_list = []

        for _, row in filtered_df.iterrows():
            img = Image.open(row['Image']).resize((40, 40), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            product_treeview.image_list.append(img)
            values = [row['Id'], row['Product Name'], row['Unit Price'], row['Quantity'], row['Created_at'], row['Updated_at']]
            product_treeview.insert('', index=tk.END, values=values, image=img)

def export_to_pdf(treeview, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    columns = treeview["columns"]
    data = [columns] + [treeview.item(item, 'values') for item in treeview.get_children()]
    table = Table(data, colWidths=90)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('GRID', (0, 0), (-1, -1), 1, 'black')
    ])

    table.setStyle(style)
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

def export_inventory_to_pdf():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filename:
        export_to_pdf(inventory_treeview, filename)

def export_product_to_pdf():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filename:
        export_to_pdf(product_treeview, filename)


# Pane #2
pane_2 = ttk.Frame(paned)
paned.add(pane_2, weight=2)
pane_2.grid(row=1,sticky="nsew", rowspan=1)

# Notebook
notebook = ttk.Notebook(pane_2)

# Tab #1
tab_1 = ttk.Frame(notebook)
notebook.add(tab_1, text="Inventories")
 
inventory_treeview = create_treeview(tab_1, ["Id", "Inventory Name", "Address","Created_at","Updated_at"])
inventory_treeview.column('Id', width=10, anchor='center')

load_data('./data/inventory.csv', inventory_treeview)

add_button = ttk.Button(tab_1, text="Add", style="Accent.TButton", command=add_inventory)
add_button.pack(side=tk.LEFT, padx=5, pady=5)

edit_button = ttk.Button(tab_1, text="Edit", style="Accent.TButton", command=edit_inventory)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = ttk.Button(tab_1, text="Delete", style="Accent.TButton", command=delete_inventory)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

export_button = ttk.Button(tab_1, text="Export PDF", style="Accent.TButton", command=export_inventory_to_pdf)
export_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Tab #2
tab_2 = ttk.Frame(notebook)
notebook.add(tab_2, text="Items")

treeFrame = ttk.Frame(tab_2)
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

columns = ['Id','Item Name','Unit Price','Quantity', 'Created_at', 'Updated_at']

# Create a style for product_treeview
product_treeview_style = ttk.Style()
product_treeview_style.configure("Custom.Treeview", rowheight= 40)

product_treeview = ttk.Treeview(treeFrame, column=columns, selectmode='extended', yscrollcommand=treeScroll.set, height=7, style="Custom.Treeview")
product_treeview.pack(expand=True, fill="both")
treeScroll.config(command=product_treeview.yview)

# Setup column heading
for col in columns:
    product_treeview.heading(col, text=col, anchor='center')

# Setup column
for col in columns:
    product_treeview.column(col, anchor='center', width=120)

# load data to product table
df = pd.read_csv('./data/items.csv', sep=';') 

columns = tuple(df.columns)
data = [columns] + [tuple(x) for x in df.to_records(index=False)]

image_list = []

values_without_image = [value[:data[0].index('Image')] + value[data[0].index('Image') + 1:] for value in data[1:]]
for value, image_path in zip(values_without_image, df['Image']):
    _img = Image.open(image_path).resize((40, 40), Image.LANCZOS)
    _img = ImageTk.PhotoImage(_img)
    image_list.append(_img)
    product_treeview.insert('', index=tk.END, value=value, image=_img)

export_button_2 = ttk.Button(tab_2, text="Export PDF", style="Accent.TButton", command=export_product_to_pdf)
export_button_2.pack(side=tk.RIGHT, padx=5, pady=5)

add_button_2 = ttk.Button(tab_2, text="Add", style="Accent.TButton", command=add_product)
add_button_2.pack(side=tk.LEFT, padx=5, pady=5)

edit_button_2 = ttk.Button(tab_2, text="Edit", style="Accent.TButton", command=edit_product)
edit_button_2.pack(side=tk.LEFT, padx=5, pady=5)

delete_button_2 = ttk.Button(tab_2, text="Delete", style="Accent.TButton", command=delete_product)
delete_button_2.pack(side=tk.LEFT, padx=5, pady=5)

# Tab #3
tab_3 = ttk.Frame(notebook)
notebook.add(tab_3, text="Statistical")

chart_canvas = None
chart_fig = None

def update_chart():
    global chart_canvas, chart_fig

    selected_inventory_name = combobox_inventory_static.get()

    if selected_inventory_name:
        df_inventory = pd.read_csv('./data/inventory.csv', delimiter=';')
        inventory_id = df_inventory[df_inventory['Inventory Name'] == selected_inventory_name].iloc[0]['Id']
        df_products = pd.read_csv('./data/items.csv', delimiter=';')
        
        filtered_df = df_products[df_products['Inventory'] == inventory_id]
        group_by_product_type = filtered_df.groupby(['Category', 'Product Name'])['Unit Price'].sum()

        if chart_canvas is not None:
            # Clear the existing chart
            chart_canvas.get_tk_widget().destroy()

        # Specify the desired figure size
        figsize = (8, 4)

        # Plot the bar charts
        chart_fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=figsize)

        # Plot Total Value of Products by Type
        group_by_product_type.unstack().plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_title(f'Total Value of Products by Category - {selected_inventory_name}')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Total Value')
        ax1.set_xticklabels(group_by_product_type.index.levels[0], rotation=0, ha='right')

        # Plot Quantity of Products by Type
        group_by_quantity = filtered_df.groupby(['Category', 'Product Name'])['Quantity'].sum()
        group_by_quantity.unstack().plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title(f'Total Quantity of Products by Category - {selected_inventory_name}')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Total Quantity')
        ax2.set_xticklabels(group_by_quantity.index.levels[0], rotation=0, ha='right')

        chart_canvas = FigureCanvasTkAgg(chart_fig, master=tab_3)
        chart_canvas.draw()

        # Configure pack options for chart_canvas
        chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=20)

notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Sizegrip
sizegrip = ttk.Sizegrip(root)

# Center the window, and set minsize
root.update()
center_window(root)
root.mainloop()