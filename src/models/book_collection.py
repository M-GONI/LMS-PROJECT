import json
import os
from src.models.book import Book


class BookCollection:
    """Manages all books."""

    def __init__(self, json_file="books_data.json"):
        self._books = {}  # dictionary
        self.json_file = json_file
        self.load_from_json()

    def add_book(self, book):
        if book.get_book_id() in self._books:
            raise ValueError("Book already exists")
        self._books[book.get_book_id()] = book
        self.save_to_json()

    def remove_book(self, book_id):
        if book_id not in self._books:
            raise KeyError("Book not found")
        del self._books[book_id]
        self.save_to_json()

    def find_by_id(self, book_id):
        return self._books.get(book_id)

    def find_by_title(self, title):
        result = []
        for book in self._books.values():
            if title.lower() in book.get_title().lower():
                result.append(book)
        return result

    def get_all_books(self):
        return list(self._books.values())

    def borrow_book(self, book_id, member_id):
        """Borrow a book for a member."""
        book = self.find_by_id(book_id)
        if not book:
            raise KeyError("Book not found")
        if not book.borrow(member_id):
            raise ValueError("Book is already borrowed")
        self.save_to_json()
        return book

    def return_book(self, book_id):
        """Return a borrowed book."""
        book = self.find_by_id(book_id)
        if not book:
            raise KeyError("Book not found")
        if not book.return_book():
            raise ValueError("Book is not currently borrowed")
        self.save_to_json()
        return book

    def count(self):
        return len(self._books)

    def save_to_json(self):
        """Save all books to a JSON file."""
        data = []
        for book in self._books.values():
            data.append({
                "book_id": book.get_book_id(),
                "title": book.get_title(),
                "author": book.get_author(),
                "isbn": book.get_isbn(),
                "is_borrowed": book.is_borrowed(),
                "borrowed_by": book.get_borrowed_by()
            })
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        """Load all books from a JSON file."""
        if not os.path.exists(self.json_file):
            return  # File doesn't exist yet, start fresh
        
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            self._books = {}
            for item in data:
                book = Book(item["book_id"], item["title"], item["author"], item["isbn"])
                # Restore borrow status if it exists
                if item.get("is_borrowed", False):
                    book._is_borrowed = True
                    book._borrowed_by = item.get("borrowed_by")
                self._books[book.get_book_id()] = book
        except (json.JSONDecodeError, KeyError, TypeError):
            # If there's an error reading the file, start fresh
            self._books = {}
