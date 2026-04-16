class Book:
    """Represents a library book."""

    def __init__(self, book_id, title, author, isbn):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_borrowed = False
        self._borrowed_by = None  # member_id who borrowed the book

    # Getters
    def get_book_id(self):
        return self._book_id

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_isbn(self):
        return self._isbn

    def is_borrowed(self):
        return self._is_borrowed

    def get_borrowed_by(self):
        return self._borrowed_by

    # Setters
    def borrow(self, member_id):
        """Mark book as borrowed by a member."""
        if self._is_borrowed:
            return False
        self._is_borrowed = True
        self._borrowed_by = member_id
        return True

    def return_book(self):
        """Mark book as returned."""
        if not self._is_borrowed:
            return False
        self._is_borrowed = False
        self._borrowed_by = None
        return True

    def get_status(self):
        """Get book status."""
        if self._is_borrowed:
            return f"Borrowed (by {self._borrowed_by})"
        return "Available"
