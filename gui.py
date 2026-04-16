import tkinter as tk
from models.member import Member
from models.member_collection import MemberCollection

collection = MemberCollection()


def add_member():
    name = entry_name.get()
    member_id = entry_id.get()
    email = entry_email.get()

    try:
        member = Member(name, member_id, email)
        collection.add_member(member)
        output_label.config(text="Member added successfully", fg="green")
        clear_fields()
    except ValueError as e:
        output_label.config(text=str(e), fg="red")


def view_members():
    members = collection.get_all_members()
    if not members:
        output_label.config(text="No members found", fg="blue")
    else:
        text = "\n".join([f"{m.get_member_id()} - {m.get_name()}" for m in members])
        output_label.config(text=text, fg="black")


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_email.delete(0, tk.END)


# GUI Window
root = tk.Tk()
root.title("Library Member System")
root.geometry("400x400")

# Labels & Inputs
tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Member ID").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

# Buttons
tk.Button(root, text="Add Member", command=add_member).pack(pady=5)
tk.Button(root, text="View Members", command=view_members).pack(pady=5)

# Output
output_label = tk.Label(root, text="")
output_label.pack(pady=10)

root.mainloop()