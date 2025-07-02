import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connect DB
conn = sqlite3.connect('inventory.db')
cur = conn.cursor()

# Create table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')
conn.commit()

# GUI setup
root = tk.Tk()
root.title("🛒 Local Inventory & Billing System")

# Form to add product to inventory
tk.Label(root, text="Product Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Price:").grid(row=1, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=1, column=1)

def add_product():
    name = name_entry.get()
    price = price_entry.get()
    try:
        price = float(price)
    except:
        messagebox.showerror("Error", "Price must be a number")
        return
    cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    messagebox.showinfo("Added", f"{name} added at ${price:.2f}")
    refresh_products()

tk.Button(root, text="Add Product", command=add_product).grid(row=2, column=0, columnspan=2, pady=5)

# Product list for billing
tree = ttk.Treeview(root, columns=("Name", "Price"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.grid(row=3, column=0, columnspan=2)

cart = []
total_label = tk.Label(root, text="Total: $0.00")
total_label.grid(row=5, column=0, columnspan=2)

def refresh_products():
    for row in tree.get_children():
        tree.delete(row)
    for row in cur.execute("SELECT id, name, price FROM products"):
        tree.insert("", tk.END, iid=row[0], values=(row[1], f"${row[2]:.2f}"))

def add_to_cart():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a product to add to bill")
        return
    for item_id in selected:
        item = cur.execute("SELECT name, price FROM products WHERE id = ?", (item_id,)).fetchone()
        cart.append(item)
    update_total()

def update_total():
    total = sum(item[1] for item in cart)
    total_label.config(text=f"Total: ${total:.2f}")

tk.Button(root, text="Add to Bill", command=add_to_cart).grid(row=4, column=0, columnspan=2, pady=5)

refresh_products()

root.mainloop()
conn.close()
