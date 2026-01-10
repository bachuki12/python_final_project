# app/ui/library_app.py
import os
import sys
import time

from app.services.library import Library
from app.models.admin import Admin

from app.utils.validators import InputValidator as V, ValidationError
from app.utils.safe import SafeExecutor as Safe


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class LibraryApp:
    def __init__(self):
        self.library = Library()
        self.current_user = None

    # ==================================================
    # Small helpers (no repetitive try/except in features)
    # ==================================================
    def _pause(self, msg="\nგასაგრძელებლად დააჭირეთ Enter-ს..."):
        input(msg)

    def _ask(self, prompt, validator=None):
        """
        validator: function(text)-> validated value
        If validator is None, returns stripped text (non-empty not enforced).
        Keeps asking until valid.
        """
        while True:
            value = input(prompt).strip()
            try:
                if validator is None:
                    return value
                return validator(value)
            except ValidationError as e:
                print(f"{Colors.FAIL}❌ {e}{Colors.ENDC}")
                time.sleep(1.0)

    def _ask_choice(self, prompt, allowed):
        return self._ask(prompt, lambda x: V.choice(x, allowed, "არასწორი არჩევანი"))

    def _is_admin(self):
        return isinstance(self.current_user, Admin)

    # ==================================================
    # ENTRY POINT
    # ==================================================
    def run(self):
        width = 60

        while True:
            clear_screen()
            print()
            print(f"{Colors.BOLD}{'👋 მოგესალმებით ბიბლიოთეკის სისტემაში'.center(width)}{Colors.ENDC}")
            print(f"{Colors.BLUE}{('═' * 45).center(width)}{Colors.ENDC}")
            print(f"{Colors.GREEN}{'1. ✅ კი, რეგისტრირებული ვარ'.center(width)}{Colors.ENDC}")
            print(f"{'2. 📝 არა, მსურს რეგისტრაცია'.center(width)}")
            print(f"{Colors.FAIL}{'3. 🚪 გასვლა (Exit)'.center(width)}{Colors.ENDC}")
            print(f"{Colors.BLUE}{('═' * 45).center(width)}{Colors.ENDC}")

            choice = self._ask_choice(
                f"\n{Colors.BOLD}   👉 გთხოვთ აირჩიოთ (1/2/3): {Colors.ENDC}",
                ["1", "2", "3"]
            )

            if choice == "3":
                print(f"\n{('👋 ნახვამდის!').center(width)}")
                return

            if choice == "1":
                self.current_user = self.login()
            else:
                self.current_user = self.register()

            if self.current_user:
                self.main_menu()
                # user/admin მენიუდან დაბრუნების შემდეგ ისევ მთავარ ეკრანზე
                self.current_user = None

    # ==================================================
    # AUTH
    # ==================================================
    def register(self):
        clear_screen()
        print("\n--- რეგისტრაცია ---")

        def action():
            pid = self._ask("პირადი ნომერი: ", lambda x: V.digits_exact(x, 11, "გთხოვთ შეიყვანოთ ვალიდური 11-ციფრიანი პირადი ნომერი"))
            name = self._ask("სახელი და გვარი: ", lambda x: V.name(x, "სახელი არ უნდა შეიცავდეს ციფრებს"))
            phone = self._ask("ტელეფონი (9 ციფრი): ", lambda x: V.digits_exact(x, 9, "გთხოვთ შეიყვანოთ ვალიდური 9-ციფრიანი ნომერი"))
            password = self._ask("პაროლი: ", lambda x: V.password(x, min_len=3))

            user = self.library.register_user(pid, name, phone, password)
            if not user:
                raise ValidationError("ამ პირადი ნომრით მომხმარებელი უკვე არსებობს")

            print(f"{Colors.GREEN}✅ რეგისტრაცია წარმატებით დასრულდა{Colors.ENDC}")
            time.sleep(1.0)
            return user

        user = Safe.run(action)
        if user is None:
            # თუ რეგისტრაცია ვერ გამოვიდა, დავბრუნდეთ მთავარ მენიუში
            self._pause()
        return user

    def login(self):
        attempts = 3

        while attempts > 0:
            clear_screen()
            print(f"\n{Colors.BLUE}╔" + "═" * 30 + "╗")
            print(f"║      {Colors.BOLD}🔐 ავტორიზაცია{Colors.ENDC}         {Colors.BLUE}║")
            print(f"╚" + "═" * 30 + "╝{Colors.ENDC}\n")

            pid = self._ask(f"{Colors.BOLD}🆔 პირადი ნომერი: {Colors.ENDC}", lambda x: V.non_empty(x, "პირადი ნომერი ცარიელია"))
            password = self._ask(f"{Colors.BOLD}🔑 პაროლი: {Colors.ENDC}", lambda x: V.non_empty(x, "პაროლი ცარიელია"))

            user = self.library.login_user(pid, password)
            if user:
                print(f"\n{Colors.GREEN}✅ მოგესალმებით, {user.name}!{Colors.ENDC}")
                time.sleep(1.0)
                return user

            attempts -= 1
            if attempts > 0:
                print(f"{Colors.FAIL}❌ არასწორი მონაცემები. დაგრჩათ {attempts} მცდელობა.{Colors.ENDC}")
                time.sleep(1.2)
            else:
                print(f"{Colors.FAIL}❌ მცდელობები ამოიწურა!{Colors.ENDC}")
                time.sleep(1.2)
                return None

    # ==================================================
    # MENU
    # ==================================================
    def main_menu(self):
        while True:
            clear_screen()

            if self._is_admin():
                print(f"\n{Colors.BOLD}🛠️ ADMIN მენიუ:{Colors.ENDC}")
                print(f"{Colors.BLUE} 1. ➕ წიგნის დამატება")
                print(f" 2. 🗑️ წიგნის წაშლა")
                print(f" 3. 📚 ყველა წიგნის ნახვა")
                print(f"{Colors.FAIL} 4. 🚪 გასვლა{Colors.ENDC}")

                choice = self._ask_choice(f"\n{Colors.BOLD}👉 აირჩიეთ მოქმედება: {Colors.ENDC}", ["1", "2", "3", "4"])

                if choice == "1":
                    self.admin_add_book()
                elif choice == "2":
                    self.admin_remove_book()
                elif choice == "3":
                    self.admin_list_books()
                else:
                    return

            else:
                print(f"\n{Colors.BOLD}🚀 მთავარი მენიუ:{Colors.ENDC}")
                print(f"{Colors.BLUE} 1. 👤 პირადი გვერდი")
                print(f" 2. 📚 ყველა წიგნის ნახვა")
                print(f" 3. 📖 წიგნის გატანა")
                print(f" 4. 🔄 წიგნის დაბრუნება")
                print(f"{Colors.FAIL} 5. 🚪 გასვლა{Colors.ENDC}")

                choice = self._ask_choice(f"\n{Colors.BOLD}👉 აირჩიეთ მოქმედება: {Colors.ENDC}", ["1", "2", "3", "4", "5"])

                if choice == "1":
                    self.personal_page()
                elif choice == "2":
                    self.admin_list_books()
                elif choice == "3":
                    self.borrow_book()
                elif choice == "4":
                    self.return_book()
                else:
                    return

    # ==================================================
    # PERSONAL PAGE
    # ==================================================
    def personal_page(self):
        clear_screen()
        print(f"\n{Colors.BLUE}╔" + "═" * 45 + "╗")
        print(f"║          {Colors.BOLD}👤 თქვენი პირადი გვერდი{Colors.ENDC}            {Colors.BLUE}║")
        print(f"╚" + "═" * 45 + "╝{Colors.ENDC}")

        self.display_user_data()
        self._pause(f"\n{Colors.BOLD}🔙 Enter - დაბრუნება მთავარ მენიუში{Colors.ENDC}")

    def display_user_data(self):
        user = self.current_user

        print(f"{Colors.BLUE}╔" + "═" * 50 + "╗")
        print(f"║ {Colors.BOLD}👤 მომხმარებელი:{Colors.ENDC} {user.name:<32} {Colors.BLUE}║")
        print(f"║ {Colors.BOLD}📞 ტელეფონი:{Colors.ENDC} {user.phone:<36} {Colors.BLUE}║")
        print(f"╠" + "═" * 50 + "╣")
        print(f"║ {Colors.BOLD}📚 გატანილი წიგნები და ვადები:{Colors.ENDC}                {Colors.BLUE}║")

        if not user.borrowed_books:
            print(f"║ {Colors.WARNING}   - ამჟამად გატანილი წიგნები არ გაქვთ. {Colors.ENDC}       {Colors.BLUE}║")
        else:
            for i, b in enumerate(user.borrowed_books):
                title_part = f"{i + 1}. {b['title']}"
                date_part = f"📅 ვადა: {b['due_date']}"
                line = f"  {title_part:<25} | {date_part:<15}"
                print(f"║ {Colors.GREEN}{line:<48}{Colors.BLUE} ║")

        print(f"╚" + "═" * 50 + "╝{Colors.ENDC}")

    # ==================================================
    # BORROW
    # ==================================================
    def borrow_book(self):
        clear_screen()
        print(f"\n{Colors.BLUE}🔎 --- წიგნის ძებნა ---{Colors.ENDC}")

        search_type = self._ask_choice("მოძებნა: 1. სახელით | 2. ავტორით: ", ["1", "2"])

        if search_type == "1":
            title = self._ask("შეიყვანეთ წიგნის სახელი: ", lambda x: V.non_empty(x, "სახელი ცარიელია"))
            books = self.library.find_books_by_title(title)
        else:
            author = self._ask("შეიყვანეთ ავტორი: ", lambda x: V.non_empty(x, "ავტორი ცარიელია"))
            books = self.library.find_books_by_author(author)

        if not books:
            print(f"{Colors.FAIL}❌ ასეთი წიგნი/ავტორი ვერ მოიძებნა{Colors.ENDC}")
            self._pause()
            return

        # არჩევა
        if len(books) == 1:
            book = books[0]
            print(f"\n{Colors.GREEN}✅ ნაპოვნია: {book.title} | {book.author}{Colors.ENDC}")
        else:
            print(f"\n{Colors.BOLD}📚 ნაპოვნია რამდენიმე წიგნი:{Colors.ENDC}")
            for i, b in enumerate(books, start=1):
                print(f"{i}. {b.title} | {b.author} | ⭐ {b.rating}")

            idx = self._ask(
                f"\n{Colors.BOLD}👉 რომელი წიგნის გატანა გსურთ? (ნომერი): {Colors.ENDC}",
                lambda x: V.int_in_range(x, 1, len(books), "არასწორი ნომერი")
            )
            book = books[idx - 1]

        # გატანა
        days = self._ask(
            f"{Colors.BOLD}📅 რამდენი ხნით გსურთ გატანა? (მაგ: 10): {Colors.ENDC}",
            lambda x: V.non_empty(x, "ვადა ცარიელია")
        )
        due_date = f"{days} დღე" if days.isdigit() else days

        self.current_user.borrow_book(book.title, due_date)
        self.library.save_users()

        print(f"\n{Colors.GREEN}✅ წიგნი „{book.title}“ წარმატებით გატანილია!{Colors.ENDC}")
        self._pause()

    # ==================================================
    # RETURN + RATING
    # ==================================================
    def return_book(self):
        user = self.current_user

        if not user.borrowed_books:
            print(f"{Colors.FAIL}❌ დასაბრუნებელი წიგნები არ გაქვთ{Colors.ENDC}")
            self._pause()
            return

        clear_screen()
        print(f"\n{Colors.BOLD}📚 თქვენი გატანილი წიგნები:{Colors.ENDC}")
        for i, b in enumerate(user.borrowed_books, start=1):
            print(f"{i}. {b['title']} (ვადა: {b['due_date']})")

        choice = self._ask(
            f"\n{Colors.BOLD}👉 შეიყვანეთ დასაბრუნებელი წიგნების ნომრები (მძიმით, მაგ: 1,2) ან 'q' გასასვლელად: {Colors.ENDC}",
            lambda x: V.non_empty(x, "შეყვანა ცარიელია")
        )

        if choice.lower() == "q":
            return

        def parse_indices(text):
            # validators-ში არ ვამატებთ ზედმეტ სპეციფიკურ ფუნქციას, მაგრამ ვალიდაციაზე ვიყენებთ ValidationError-ს.
            parts = [p.strip() for p in text.split(",") if p.strip()]
            if not parts:
                raise ValidationError("არასწორი ფორმატი")

            idxs = []
            for p in parts:
                if not p.isdigit():
                    raise ValidationError("გამოიყენეთ მხოლოდ ციფრები და მძიმე")
                idxs.append(int(p) - 1)

            if any(i < 0 or i >= len(user.borrowed_books) for i in idxs):
                raise ValidationError("ერთ-ერთი ნომერი არასწორია")

            # კლებადობით რომ ამოშლისას სია არ აირიოს
            idxs.sort(reverse=True)
            return idxs

        idxs = Safe.run(lambda: parse_indices(choice))
        if idxs is None:
            self._pause()
            return

        returned_titles = []
        for index in idxs:
            returned = user.return_book(index)
            returned_titles.append(returned["title"])
            print(f"{Colors.GREEN}✅ დაბრუნდა: „{returned['title']}“{Colors.ENDC}")

        self.library.save_users()
        print(f"\n{Colors.BOLD}🎉 სულ დაბრუნდა {len(returned_titles)} წიგნი.{Colors.ENDC}")

        # შეფასება (მხოლოდ ბოლოს, ერთჯერ)
        rating_input = input(f"\n{Colors.BOLD}⭐ შეაფასეთ (0–5, შესაძლებელია ათწილადი) ან გამოტოვეთ: {Colors.ENDC}").strip()
        if rating_input:
            rating_value = Safe.run(lambda: V.float_in_range(rating_input, 0, 5, "რეიტინგი უნდა იყოს 0-დან 5-მდე"))
            if rating_value is not None:
                # შენს CLI-ში "returned" ბოლო წიგნი იყო; აქ ლოგიკურად ვაფასებთ ბოლოს დაბრუნებულს.
                title_to_rate = returned_titles[-1]
                new_avg = self.library.rate_book(title_to_rate, rating_value)
                if new_avg is not None:
                    print(f"{Colors.GREEN}📊 „{title_to_rate}“ ახალი საშუალო რეიტინგი: {new_avg}{Colors.ENDC}")

        self._pause()

    # ==================================================
    # ADMIN
    # ==================================================
    def admin_add_book(self):
        clear_screen()
        print(f"{Colors.BOLD}➕ წიგნის დამატება{Colors.ENDC}")

        title = self._ask("📖 სახელი: ", lambda x: V.non_empty(x, "სათაური ცარიელია"))
        author = self._ask("✍️ ავტორი: ", lambda x: V.non_empty(x, "ავტორი ცარიელია"))
        pages = self._ask("📄 გვერდები: ", lambda x: V.int_in_range(x, 1, 100000, "გვერდების რაოდენობა არასწორია"))
        rating = self._ask("⭐ რეიტინგი (0–5): ", lambda x: V.float_in_range(x, 0, 5, "რეიტინგი უნდა იყოს 0-დან 5-მდე"))

        def action():
            self.current_user.add_book(self.library, title, author, pages, rating)
            print(f"\n{Colors.GREEN}✅ წიგნი წარმატებით დაემატა!{Colors.ENDC}")

        Safe.run(action)
        self._pause()

    def admin_remove_book(self):
        clear_screen()
        print(f"{Colors.BOLD}🗑️ წიგნის წაშლა{Colors.ENDC}")

        title = self._ask("წიგნის ზუსტი სახელი: ", lambda x: V.non_empty(x, "სათაური ცარიელია"))

        def action():
            self.current_user.remove_book(self.library, title)
            print(f"{Colors.GREEN}✅ თუ არსებობდა, წიგნი წაშლილია{Colors.ENDC}")

        Safe.run(action)
        self._pause()

    def admin_list_books(self):
        clear_screen()
        print(f"{Colors.BOLD}📚 ბიბლიოთეკის წიგნები{Colors.ENDC}\n")

        if not self.library.books:
            print(f"{Colors.WARNING}ბიბლიოთეკა ცარიელია{Colors.ENDC}")
        else:
            for i, book in enumerate(self.library.books, start=1):
                print(f"{i}. {book.title} | {book.author} | {book.pages} გვ | ⭐ {book.rating}")

        self._pause()


if __name__ == "__main__":
    LibraryApp().run()
