import json
import os
from app.models.book import Book 
from app.models.user import User
from app.models.admin import Admin

class Library:
    # ---------------- PATH SETUP ----------------
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
    DATA_DIR = os.path.join(BASE_DIR, "data")

    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    BOOKS_FILE = os.path.join(DATA_DIR, "books.json")

    def __init__(self):
        os.makedirs(self.DATA_DIR, exist_ok=True)

        self.users = {}
        self.books = []

        self.load_users()
        self.load_books()
        self._ensure_admin_exists()


    def load_users(self):
        if not os.path.exists(self.USERS_FILE):
            self.users = {}
            return

        try:
            with open(self.USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.users = {}
            return

        for pid, user_data in data.items():
            if user_data.get("type") == "admin":
                self.users[pid] = Admin.from_dict(pid, user_data)
            else:
                self.users[pid] = User.from_dict(pid, user_data)
            if not os.path.exists(self.USERS_FILE):
                return

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

        self.books = sorted(
            (Book.from_dict(b) for b in data),
            key=lambda book: book.rating,
            reverse=True
        )

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

    def _ensure_admin_exists(self):
        ADMIN_PID = "11111111111"

        if ADMIN_PID not in self.users:
            admin = Admin(
                pid="11111111111",
                name="Administrator",
                phone="000111222",
                password="admin123"
            )
            self.users[admin.pid] = admin
            self.save_users()

    def rate_book(self, title, rating):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.add_rating(rating)
                self.save_books()
                return book.rating
        return None
    
    def remove_user(self, pid):
        user_todelete = self.users.get(pid)
        
        if not user_todelete:
            return False, 'მომხმარებელი ვერ მოიძებნა'

        if user_todelete.borrowed_books:
            return False, 'გთხოვთ დააბრუნოთ წიგნები ანგარიშის გაუქმებამდე'
        
        del self.users[pid]
        self.save_users()
        return True, 'თქვენი ანგარიში წარმატებით გაუქმდა'
            
        
