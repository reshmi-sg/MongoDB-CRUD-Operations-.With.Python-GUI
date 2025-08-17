mport tkinter as tk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.testdb
collection = db.testcollection

# Tkinter setup
root = tk.Tk()
root.title("MongoDB CRUD with Tkinter")

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

def refresh_list():
    listbox.delete(0, tk.END)
    for doc in collection.find():
        listbox.insert(tk.END, f"{doc['_id']} : {doc.get('name','')}")

def add_item():
    name = simpledialog.askstring("Input", "Enter name:")
    if name:
        collection.insert_one({"name": name})
        refresh_list()

def update_item():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Select", "Select an item to update")
        return
    idx = selected[0]
    doc_id = list(collection.find())[idx]["_id"]
    new_name = simpledialog.askstring("Input", "Enter new name:")
    if new_name:
        collection.update_one({"_id": doc_id}, {"$set": {"name": new_name}})
        refresh_list()

def delete_item():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Select", "Select an item to delete")
        return
    idx = selected[0]
    doc_id = list(collection.find())[idx]["_id"]
    collection.delete_one({"_id": doc_id})
    refresh_list()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", command=add_item).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_item).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_item).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Refresh", command=refresh_list).grid(row=0, column=3, padx=5)

refresh_list()
root.mainloop()
