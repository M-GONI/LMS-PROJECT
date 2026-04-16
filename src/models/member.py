class Member:
    """Represents a library member."""

    def __init__(self, name, member_id, email):
        self._name = name
        self._member_id = member_id
        self._email = email
        self._borrowed_books = []
        self._fines_owed = 0.0

    # Getters (controlled access)
    def get_name(self):
        return self._name

    def get_member_id(self):
        return self._member_id

    def get_email(self):
        return self._email

    def borrow_book(self, book):
        if len(self._borrowed_books) >= 5:
            return False
        self._borrowed_books.append(book)
        return True

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            return True
        return False

    def get_borrowed_books(self):
        return self._borrowed_books.copy()

    def add_fine(self, amount):
        self._fines_owed += amount

    def pay_fine(self, amount):
        self._fines_owed -= amount

    def get_fines(self):
        return self._fines_owed