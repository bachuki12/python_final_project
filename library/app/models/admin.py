from app.models.user import User
from app.models.book import Book


class Admin(User):
    def __init__(self, pid, name, phone, password):
        super().__init__(pid, name, phone, password)

    # --- ADMIN PRIVILEGES ---
    def add_book(self, library, title, author, pages, rating):
        library.books.append(Book(title, author, pages, rating))
        library.save_books()

    def remove_book(self, library, title):
        library.books = [
            b for b in library.books
            if b.title.lower() != title.lower()
        ]
        library.save_books()

    def to_dict(self):
        base = super().to_dict()
        base["type"] = "admin"
        return base

    @staticmethod
    def from_dict(pid, data):
        return Admin(
            pid,
            data["name"],
            data["phone"],
            data["password"]
        )
