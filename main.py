import tkinter as tk
from tkinter import messagebox
import sqlite3

# --- DB setup ---
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()

# --- Functions ---
def add_item():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()

    if not name or not quantity or not price:
        messagebox.showwarning("Missing info", "Fill all fields!")
        return
    
    try:
        cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", 
                       (name, int(quantity), float(price)))
        conn.commit()
        messagebox.showinfo("Success", "Item added!")
        clear_entries()
        view_items()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_items():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM inventory")
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"ID:{row[0]} | {row[1]} | Qty: {row[2]} | Price: ${row[3]:.2f}")

def update_item():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("Select item", "Choose an item to update")
        return
    
    item_id = int(selected.split('|')[0].replace("ID:", "").strip())
    new_qty = quantity_entry.get()
    new_price = price_entry.get()

    if not new_qty or not new_price:
        messagebox.showwarning("Missing info", "Enter new quantity and price")
        return

    cursor.execute("UPDATE inventory SET quantity=?, price=? WHERE id=?", 
                   (int(new_qty), float(new_price), item_id))
    conn.commit()
    messagebox.showinfo("Updated", "Item updated!")
    clear_entries()
    view_items()

def delete_item():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("Select item", "Choose an item to delete")
        return

    item_id = int(selected.split('|')[0].replace("ID:", "").strip())
    cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Item removed!")
    view_items()

def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# --- GUI ---
root = tk.Tk()
root.title("📦 Mini Inventory System")
root.geometry("400x500")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

tk.Label(root, text="Price").pack()
price_entry = tk.Entry(root)
price_entry.pack()

tk.Button(root, text="Add Item", command=add_item).pack(pady=5)
tk.Button(root, text="Update Item", command=update_item).pack(pady=5)
tk.Button(root, text="Delete Item", command=delete_item).pack(pady=5)
tk.Button(root, text="View Inventory", command=view_items).pack(pady=5)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

view_items()

root.mainloop()
conn.close()
