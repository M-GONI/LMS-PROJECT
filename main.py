import tkinter as tk
from tkinter import scrolledtext, messagebox
from src.models.member import Member
from src.models.member_collection import MemberCollection

collection = MemberCollection()


def log_output(message, color="black"):
    """Display message in the output text area"""
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.tag_add(color, f"end-{len(message)+1}c", "end-1c")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)  # Auto-scroll to bottom


def clear_output():
    """Clear the output text area"""
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)


def add_member():
    name = entry_name.get().strip()
    member_id = entry_id.get().strip()
    email = entry_email.get().strip()

    if not name or not member_id or not email:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        member = Member(name, member_id, email)
        collection.add_member(member)
        log_output("✅ Member added successfully", "green")
        clear_fields()
    except ValueError as e:
        log_output(f"❌ Error: {str(e)}", "red")


def view_members():
    clear_output()
    members = collection.get_all_members()
    if not members:
        log_output("No members found", "blue")
    else:
        log_output("==== All Members ====", "black")
        for m in members:
            log_output(f"{m.get_member_id()} - {m.get_name()} ({m.get_email()})")


def find_member():
    member_id = entry_id.get().strip()
    
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID")
        return
    
    clear_output()
    member = collection.find_by_id(member_id)
    if member:
        log_output("==== Member Found ====", "green")
        log_output(f"ID: {member.get_member_id()}")
        log_output(f"Name: {member.get_name()}")
        log_output(f"Email: {member.get_email()}")
    else:
        log_output("❌ Member not found", "red")


def remove_member():
    member_id = entry_id.get().strip()
    
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID to remove")
        return
    
    try:
        collection.remove_member(member_id)
        clear_output()
        log_output(f"✅ Member (ID: {member_id}) removed successfully", "green")
        clear_fields()
    except KeyError as e:
        clear_output()
        log_output(f"❌ Error: {str(e)}", "red")


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_email.delete(0, tk.END)


# GUI Window
root = tk.Tk()
root.title("Library Member System")
root.geometry("600x700")

# Input Section
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.X)

tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_name = tk.Entry(input_frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Member ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_id = tk.Entry(input_frame, width=30)
entry_id.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_email = tk.Entry(input_frame, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Buttons Section
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=5, fill=tk.X)

tk.Button(button_frame, text="Add Member", command=add_member, bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="View Members", command=view_members, bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Find Member", command=find_member, bg="#FF9800", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Remove Member", command=remove_member, bg="#f44336", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)

# Output Section
tk.Label(root, text="Output:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
output_text = scrolledtext.ScrolledText(root, height=20, width=70, state=tk.DISABLED, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configure text colors
output_text.tag_config("green", foreground="green")
output_text.tag_config("red", foreground="red")
output_text.tag_config("blue", foreground="blue")
output_text.tag_config("black", foreground="black")

# Clear button
tk.Button(root, text="Clear Output", command=clear_output, bg="#757575", fg="white", width=20).pack(pady=5)

root.mainloop()