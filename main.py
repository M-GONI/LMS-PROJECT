import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from src.models.member import Member
from src.models.member_collection import MemberCollection
from src.models.book import Book
from src.models.book_collection import BookCollection

member_collection = MemberCollection()
book_collection = BookCollection()


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
    name = entry_member_name.get().strip()
    member_id = entry_member_id.get().strip()
    email = entry_member_email.get().strip()

    if not name or not member_id or not email:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        member = Member(name, member_id, email)
        member_collection.add_member(member)
        log_output("✅ Member added successfully", "green")
        clear_member_fields()
    except ValueError as e:
        log_output(f"❌ Error: {str(e)}", "red")


def view_members():
    clear_output()
    members = member_collection.get_all_members()
    if not members:
        log_output("No members found", "blue")
    else:
        log_output("==== All Members ====", "black")
        for m in members:
            log_output(f"{m.get_member_id()} - {m.get_name()} ({m.get_email()})")


def find_member():
    member_id = entry_member_id.get().strip()
    
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID")
        return
    
    clear_output()
    member = member_collection.find_by_id(member_id)
    if member:
        log_output("==== Member Found ====", "green")
        log_output(f"ID: {member.get_member_id()}")
        log_output(f"Name: {member.get_name()}")
        log_output(f"Email: {member.get_email()}")
    else:
        log_output("❌ Member not found", "red")


def remove_member():
    member_id = entry_member_id.get().strip()
    
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID to remove")
        return
    
    try:
        member_collection.remove_member(member_id)
        clear_output()
        log_output(f"✅ Member (ID: {member_id}) removed successfully", "green")
        clear_member_fields()
    except KeyError as e:
        clear_output()
        log_output(f"❌ Error: {str(e)}", "red")


def clear_member_fields():
    entry_member_name.delete(0, tk.END)
    entry_member_id.delete(0, tk.END)
    entry_member_email.delete(0, tk.END)


# Book Functions
def add_book():
    book_id = entry_book_id.get().strip()
    title = entry_book_title.get().strip()
    author = entry_book_author.get().strip()
    isbn = entry_book_isbn.get().strip()

    if not book_id or not title or not author or not isbn:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        book = Book(book_id, title, author, isbn)
        book_collection.add_book(book)
        log_output("✅ Book added successfully", "green")
        clear_book_fields()
    except ValueError as e:
        log_output(f"❌ Error: {str(e)}", "red")


def view_books():
    clear_output()
    books = book_collection.get_all_books()
    if not books:
        log_output("No books found", "blue")
    else:
        log_output("==== All Books ====", "black")
        for b in books:
            status_color = "red" if b.is_borrowed() else "green"
            log_output(f"{b.get_book_id()} - {b.get_title()} by {b.get_author()}", "black")
            log_output(f"    Status: {b.get_status()}", status_color)


def find_book():
    book_id = entry_book_id.get().strip()
    
    if not book_id:
        messagebox.showerror("Error", "Please enter a Book ID")
        return
    
    clear_output()
    book = book_collection.find_by_id(book_id)
    if book:
        log_output("==== Book Found ====", "green")
        log_output(f"ID: {book.get_book_id()}")
        log_output(f"Title: {book.get_title()}")
        log_output(f"Author: {book.get_author()}")
        log_output(f"ISBN: {book.get_isbn()}")
        status_color = "red" if book.is_borrowed() else "green"
        log_output(f"Status: {book.get_status()}", status_color)
    else:
        log_output("❌ Book not found", "red")


def borrow_book():
    book_id = entry_book_id.get().strip()
    member_id = entry_member_id.get().strip()
    
    if not book_id or not member_id:
        messagebox.showerror("Error", "Please enter both Book ID and Member ID")
        return
    
    try:
        book_collection.borrow_book(book_id, member_id)
        clear_output()
        log_output(f"✅ Book '{book_id}' borrowed by member '{member_id}'", "green")
    except (KeyError, ValueError) as e:
        clear_output()
        log_output(f"❌ Error: {str(e)}", "red")


def open_borrow_dialog():
    """Open a dialog to borrow a book"""
    dialog = tk.Toplevel(root)
    dialog.title("Borrow Book")
    dialog.geometry("400x250")
    dialog.resizable(False, False)
    
    # Member ID
    tk.Label(dialog, text="Member ID:", font=("Arial", 10)).pack(pady=5)
    member_entry = tk.Entry(dialog, width=40)
    member_entry.pack(pady=5)
    
    # Book ID
    tk.Label(dialog, text="Book ID:", font=("Arial", 10)).pack(pady=5)
    book_id_entry = tk.Entry(dialog, width=40)
    book_id_entry.pack(pady=5)
    
    # Book Name (optional - for reference)
    tk.Label(dialog, text="Book Name (optional, for reference):", font=("Arial", 10)).pack(pady=5)
    book_name_entry = tk.Entry(dialog, width=40)
    book_name_entry.pack(pady=5)
    
    # ISBN (optional - for reference)
    tk.Label(dialog, text="ISBN (optional, for reference):", font=("Arial", 10)).pack(pady=5)
    isbn_entry = tk.Entry(dialog, width=40)
    isbn_entry.pack(pady=5)
    
    def borrow():
        member_id = member_entry.get().strip()
        book_id = book_id_entry.get().strip()
        
        if not member_id or not book_id:
            messagebox.showerror("Error", "Member ID and Book ID are required")
            return
        
        try:
            book_collection.borrow_book(book_id, member_id)
            clear_output()
            log_output(f"✅ Book '{book_id}' borrowed by member '{member_id}'", "green")
            dialog.destroy()
        except (KeyError, ValueError) as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(dialog, text="Borrow Book", command=borrow, bg="#9C27B0", fg="white", width=20).pack(pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy, bg="#757575", fg="white", width=20).pack(pady=5)


def return_book():
    book_id = entry_book_id.get().strip()
    
    if not book_id:
        messagebox.showerror("Error", "Please enter a Book ID")
        return
    
    try:
        book_collection.return_book(book_id)
        clear_output()
        log_output(f"✅ Book '{book_id}' returned successfully", "green")
    except (KeyError, ValueError) as e:
        clear_output()
        log_output(f"❌ Error: {str(e)}", "red")


def remove_book():
    book_id = entry_book_id.get().strip()
    
    if not book_id:
        messagebox.showerror("Error", "Please enter a Book ID to remove")
        return
    
    try:
        book_collection.remove_book(book_id)
        clear_output()
        log_output(f"✅ Book (ID: {book_id}) removed successfully", "green")
        clear_book_fields()
    except KeyError as e:
        clear_output()
        log_output(f"❌ Error: {str(e)}", "red")


def clear_book_fields():
    entry_book_id.delete(0, tk.END)
    entry_book_title.delete(0, tk.END)
    entry_book_author.delete(0, tk.END)
    entry_book_isbn.delete(0, tk.END)


# GUI Window
root = tk.Tk()
root.title("Library Member & Book System")
root.geometry("700x800")

# Create Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# ===== MEMBERS TAB =====
members_frame = ttk.Frame(notebook)
notebook.add(members_frame, text="Members")

# Input Section
input_frame = tk.Frame(members_frame)
input_frame.pack(padx=10, pady=10, fill=tk.X)

tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_member_name = tk.Entry(input_frame, width=30)
entry_member_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Member ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_member_id = tk.Entry(input_frame, width=30)
entry_member_id.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_member_email = tk.Entry(input_frame, width=30)
entry_member_email.grid(row=2, column=1, padx=5, pady=5)

# Buttons Section
button_frame = tk.Frame(members_frame)
button_frame.pack(padx=10, pady=5, fill=tk.X)

tk.Button(button_frame, text="Add Member", command=add_member, bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="View Members", command=view_members, bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Find Member", command=find_member, bg="#FF9800", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Remove Member", command=remove_member, bg="#f44336", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)


# ===== BOOKS TAB =====
books_frame = ttk.Frame(notebook)
notebook.add(books_frame, text="Books")

# Input Section
book_input_frame = tk.Frame(books_frame)
book_input_frame.pack(padx=10, pady=10, fill=tk.X)

tk.Label(book_input_frame, text="Book ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_book_id = tk.Entry(book_input_frame, width=30)
entry_book_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(book_input_frame, text="Title:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_book_title = tk.Entry(book_input_frame, width=30)
entry_book_title.grid(row=1, column=1, padx=5, pady=5)

tk.Label(book_input_frame, text="Author:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_book_author = tk.Entry(book_input_frame, width=30)
entry_book_author.grid(row=2, column=1, padx=5, pady=5)

tk.Label(book_input_frame, text="ISBN:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_book_isbn = tk.Entry(book_input_frame, width=30)
entry_book_isbn.grid(row=3, column=1, padx=5, pady=5)

# Book Buttons Section
book_button_frame = tk.Frame(books_frame)
book_button_frame.pack(padx=10, pady=5, fill=tk.X)

tk.Button(book_button_frame, text="Add Book", command=add_book, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)
tk.Button(book_button_frame, text="View Books", command=view_books, bg="#2196F3", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)
tk.Button(book_button_frame, text="Find Book", command=find_book, bg="#FF9800", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)

# Borrow/Return Section
borrow_label = tk.Label(book_button_frame, text="Book ID:", fg="#333")
borrow_label.pack(side=tk.LEFT, padx=5, pady=5)

tk.Button(book_button_frame, text="Borrow Book", command=open_borrow_dialog, bg="#9C27B0", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)
tk.Button(book_button_frame, text="Return Book", command=return_book, bg="#00BCD4", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)
tk.Button(book_button_frame, text="Remove Book", command=remove_book, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=3, pady=5)


# ===== OUTPUT SECTION (Shared by both tabs) =====
tk.Label(root, text="Output:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
output_text = scrolledtext.ScrolledText(root, height=15, width=80, state=tk.DISABLED, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configure text colors
output_text.tag_config("green", foreground="green")
output_text.tag_config("red", foreground="red")
output_text.tag_config("blue", foreground="blue")
output_text.tag_config("black", foreground="black")

# Clear button
tk.Button(root, text="Clear Output", command=clear_output, bg="#757575", fg="white", width=20).pack(pady=5)

root.mainloop()