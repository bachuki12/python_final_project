import json
import os
from app.models.book import Book 
from app.models.user import User

class Library:
    USERS_FILE = "users.json"
    BOOKS_FILE = "books.json"

    def __init__(self):
        self.users = {}
        self.books = []

        self.load_users()
        self.load_books()

    # ---------- USERS ----------
    def load_users(self):
        if not os.path.exists(self.USERS_FILE):
            return

        with open(self.USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for pid, user_data in data.items():
            self.users[pid] = User.from_dict(pid, user_data)

    def save_users(self):
        data = {pid: user.to_dict() for pid, user in self.users.items()}
        with open(self.USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ---------- BOOKS ----------
    def load_books(self):
        if not os.path.exists(self.BOOKS_FILE):
            self.books = []
            return

        with open(self.BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.books = [Book.from_dict(b) for b in data]

    def save_books(self):
        with open(self.BOOKS_FILE, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, ensure_ascii=False, indent=4)

    # ---------- AUTH ----------
    def register_user(self, pid, name, phone, password):
        if pid in self.users:
            return None
        user = User(pid, name, phone, password)
        self.users[pid] = user
        self.save_users()
        return user

    def login_user(self, pid, password):
        user = self.users.get(pid)
        if user and user.password == password:
            return user
        return None
    
        # ---------- SEARCH ----------
    def find_books_by_title(self, title):
        return [
            book for book in self.books
            if book.title.lower() == title.lower()
        ]

    def find_books_by_author(self, author):
        return [
            book for book in self.books
            if book.author.lower() == author.lower()
        ]

