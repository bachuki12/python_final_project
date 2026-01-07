import sys

from app.services.library import Library


class LibraryApp:
    def __init__(self):
        self.library = Library()
        self.current_user = None

    # ---------------- ENTRY POINT ----------------
    def run(self):
        print("\n=== მოგესალმებით ბიბლიოთეკის სისტემაში ===")

        while True:
            answer = input("\nხართ თუ არა რეგისტრირებული? (კი/არა): ").strip().lower()
            if answer == "კი":
                self.current_user = self.login()
            elif answer == "არა":
                self.current_user = self.register()
            else:
                print("გთხოვთ უპასუხოთ: კი ან არა")
                continue

            if self.current_user:
                self.main_menu()

    # ---------------- AUTH ----------------
    def register(self):
        print("\n--- რეგისტრაცია ---")
        pid = input("პირადი ნომერი: ").strip()
        name = input("სახელი და გვარი: ").strip()
        phone = input("ტელეფონი: ").strip()
        password = input("პაროლი: ").strip()

        user = self.library.register_user(pid, name, phone, password)
        if not user:
            print("❌ მომხმარებელი უკვე არსებობს")
            return None

        print("✅ რეგისტრაცია წარმატებით დასრულდა")
        return user

    def login(self):
        print("\n--- ავტორიზაცია ---")
        pid = input("პირადი ნომერი: ").strip()
        password = input("პაროლი: ").strip()

        user = self.library.login_user(pid, password)
        if not user:
            print("❌ არასწორი პირადი ნომერი ან პაროლი")
            return None

        print(f"✅ მოგესალმებით, {user.name}")
        return user

    # ---------------- MENU ----------------
    def main_menu(self):
        while True:
            self.show_profile()

            choice = input(
                "\nაირჩიეთ მოქმედება:\n"
                "1. წიგნის გატანა\n"
                "2. წიგნის დაბრუნება\n"
                "3. გასვლა\n"
                "პასუხი: "
            ).strip()

            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                print("👋 ნახვამდის!")
                sys.exit()
            else:
                print("❌ არასწორი არჩევანი")

    # ---------------- PROFILE ----------------
    def show_profile(self):
        user = self.current_user
        print("\n" + "=" * 40)
        print(f"მომხმარებელი: {user.name}")
        print(f"ტელეფონი: {user.phone}")
        print("გატანილი წიგნები:")

        if not user.borrowed_books:
            print(" - არ გაქვთ გატანილი წიგნები")
        else:
            for i, b in enumerate(user.borrowed_books):
                print(f" {i + 1}. {b['title']} (ვადა: {b['due_date']})")

        print("=" * 40)

    # ---------------- BORROW ----------------
    def borrow_book(self):
        print("\n--- წიგნის ძებნა ---")
        search_type = input("მოძებნა: 1. სახელით | 2. ავტორით: ").strip()

        if search_type == "1":
            title = input("შეიყვანეთ წიგნის სახელი: ").strip()
            books = self.library.find_books_by_title(title)
        elif search_type == "2":
            author = input("შეიყვანეთ ავტორი: ").strip()
            books = self.library.find_books_by_author(author)
        else:
            print("❌ არასწორი არჩევანი")
            return

        if not books:
            print("❌ წიგნი ვერ მოიძებნა")
            return

        print("\nნაპოვნი წიგნები:")
        for i, b in enumerate(books):
            print(f"{i + 1}. {b.title} | {b.author} | {b.pages} გვ | ⭐ {b.rating}")

        try:
            index = int(input("რომელი წიგნის გატანა გსურთ? (ნომერი): ")) - 1
            book = books[index]
        except (ValueError, IndexError):
            print("❌ არასწორი ნომერი")
            return

        days = input("რამდენი ხნით გსურთ გატანა? (მაგ: 10 დღე): ").strip()
        self.current_user.borrow_book(book.title, days)
        self.library.save_users()

        print(f"✅ წიგნი „{book.title}“ წარმატებით გატანილია")

    # ---------------- RETURN ----------------
    def return_book(self):
        user = self.current_user

        if not user.borrowed_books:
            print("❌ დასაბრუნებელი წიგნები არ გაქვთ")
            return

        print("\nთქვენი გატანილი წიგნები:")
        for i, b in enumerate(user.borrowed_books):
            print(f"{i + 1}. {b['title']}")

        try:
            index = int(input("რომელი წიგნი დააბრუნეთ? (ნომერი): ")) - 1
            returned = user.return_book(index)
        except (ValueError, IndexError):
            print("❌ არასწორი ნომერი")
            return

        self.library.save_users()
        rating = input("გთხოვთ შეაფასოთ წიგნი (1-5): ")

        print(f"✅ წიგნი „{returned['title']}“ დაბრუნებულია. მადლობა შეფასებისთვის!")
