from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Change if using Atlas
db = client["BasicDB"]
collection = db["users"]

# -------- Functions --------
def add_user():
    user = {
        "name": entry_name.get(),
        "age": entry_age.get(),
        "email": entry_email.get()
    }
    collection.insert_one(user)
    messagebox.showinfo("Success", "User added!")
    show_users()

def show_users():
    for row in tree.get_children():
        tree.delete(row)
    for user in collection.find():
        tree.insert("", "end", values=(user["_id"], user["name"], user["age"], user["email"]))

def delete_user():
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    collection.delete_one({"_id": ObjectId(values[0])})
    messagebox.showinfo("Deleted", "User deleted")
    show_users()

def update_user():
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    new_data = {
        "name": entry_name.get(),
        "age": entry_age.get(),
        "email": entry_email.get()
    }
    collection.update_one({"_id": ObjectId(values[0])}, {"$set": new_data})
    messagebox.showinfo("Updated", "User updated")
    show_users()

# -------- GUI --------
root = Tk()
root.title("Basic CRUD App")
root.geometry("600x400")

Label(root, text="Name").grid(row=0, column=0)
entry_name = Entry(root)
entry_name.grid(row=0, column=1)

Label(root, text="Age").grid(row=1, column=0)
entry_age = Entry(root)
entry_age.grid(row=1, column=1)

Label(root, text="Email").grid(row=2, column=0)
entry_email = Entry(root)
entry_email.grid(row=2, column=1)

Button(root, text="Add", command=add_user).grid(row=3, column=0)
Button(root, text="Update", command=update_user).grid(row=3, column=1)
Button(root, text="Delete", command=delete_user).grid(row=3, column=2)

# Table
columns = ("ID", "Name", "Age", "Email")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=3)

show_users()
root.mainloop()
