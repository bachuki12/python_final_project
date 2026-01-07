class User:
    def __init__(self, pid, name, phone, password, borrowed_books=None):
        self.pid = pid
        self.name = name
        self.phone = phone
        self.password = password
        self.borrowed_books = borrowed_books or []

    def borrow_book(self, title, due_date):
        self.borrowed_books.append({
            "title": title,
            "due_date": due_date
        })

    def return_book(self, index):
        return self.borrowed_books.pop(index)

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "password": self.password,
            "borrowed_books": self.borrowed_books
        }

    @staticmethod
    def from_dict(pid, data):
        return User(
            pid=pid,
            name=data["name"],
            phone=data["phone"],
            password=data["password"],
            borrowed_books=data.get("borrowed_books", [])
        )
