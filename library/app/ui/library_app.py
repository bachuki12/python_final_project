import sys

from app.services.library import Library
from app.models.admin import Admin


class Colors:
    HEADER = '\033[95m'   # იასამნისფერი
    BLUE = '\033[94m'     # ლურჯი
    GREEN = '\033[92m'    # მწვანე
    WARNING = '\033[93m'  # ყვითელი
    FAIL = '\033[91m'     # წითელი
    ENDC = '\033[0m'      # ფერის დასრულება
    BOLD = '\033[1m'      # მუქი

import os
import sys

def clear_screen():
    # Windows-ისთვის 'cls', სხვებისთვის 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

# აქედან გრძელდება თქვენი კლასი...

class LibraryApp:
    def __init__(self):
        self.library = Library()
        self.current_user = None

    # ---------------- ENTRY POINT ----------------
    def run(self):
        width = 60  # ტერმინალის პირობითი სიგანე ცენტრირებისთვის

        while True:
            clear_screen()
            print()
            # მისალმება და მენიუ ცენტრში
            print(f"{Colors.BOLD}{'👋 მოგესალმებით ბიბლიოთეკის სისტემაში'.center(width)}{Colors.ENDC}")
            print(f"{Colors.BLUE}{('═' * 45).center(width)}{Colors.ENDC}")

            print(f"{Colors.GREEN}{'1. ✅ კი, რეგისტრირებული ვარ'.center(width)}{Colors.ENDC}")
            print(f"{'2. 📝 არა, მსურს რეგისტრაცია'.center(width)}")
            print(f"{Colors.FAIL}{'3. 🚪 გასვლა (Exit)'.center(width)}{Colors.ENDC}")

            print(f"{Colors.BLUE}{('═' * 45).center(width)}{Colors.ENDC}")

            # ინპუტის ხაზი (ესეც შეგვიძლია ცოტა შევწიოთ)
            choice = input(f"\n{Colors.BOLD}   👉 გთხოვთ აირჩიოთ (1/2/3): {Colors.ENDC}").strip()

            if choice == "1" or choice.lower() == "კი":
                self.current_user = self.login()
            elif choice == "2" or choice.lower() == "არა":
                self.current_user = self.register()
            elif choice == "3" or choice.lower() == "გასვლა":
                print(f"\n{('👋 ნახვამდის!').center(width)}")
                break
            else:
                print(f"\n{Colors.FAIL}{'❌ არასწორი არჩევანი!'.center(width)}{Colors.ENDC}")
                import time
                time.sleep(1.2)
                continue

            if self.current_user:
                self.main_menu()    # ---------------- AUTH ----------------
    def register(self):
        print("\n--- რეგისტრაცია ---")
        pid = input("პირადი ნომერი: ").strip()
        name = input("სახელი და გვარი: ").strip()
        phone = input("ტელეფონი: ").strip()
        password = input("პაროლი: ").strip()

        user = self.library.register_user(pid, name, phone, password)
        if not user:
            print("❌ ამ პირადი ნომრით მომხმარებელი უკვე არსებობს")
            print("სცადეთ ავტორიზაცია ")
            return None

        print("✅ რეგისტრაცია წარმატებით დასრულდა")
        return user

    def login(self):
        print(f"\n{Colors.BLUE}╔" + "═" * 30 + "╗")
        print(f"║      {Colors.BOLD}🔐 ავტორიზაცია{Colors.ENDC}         {Colors.BLUE}║")
        print(f"╚" + "═" * 30 + "╝{Colors.ENDC}")

        attempts = 3  # მცდელობების რაოდენობა

        for i in range(attempts):
            pid = input(f"{Colors.BOLD}🆔 პირადი ნომერი: {Colors.ENDC}").strip()
            password = input(f"{Colors.BOLD}🔑 პაროლი: {Colors.ENDC}").strip()

            user = self.library.login_user(pid, password)

            if user:
                print(f"\n{Colors.GREEN}✅ მოგესალმებით, {user.name}!{Colors.ENDC}")
                return user
            else:
                remaining = attempts - (i + 1)
                if remaining > 0:
                    print(f"{Colors.FAIL}❌ არასწორი მონაცემები. დაგრჩათ {remaining} მცდელობა.{Colors.ENDC}\n")
                else:
                    print(f"{Colors.FAIL}❌ მცდელობები ამოიწურა!{Colors.ENDC}")

        return None  # თუ აქამდე მოვიდა, ე.ი. 3-ჯერ შეცდა და ბრუნდება საწყის კითხვაზე
    # ---------------- MENU ----------------
        # 1. მთავარი მენიუ
    def main_menu(self):
        while True:
            clear_screen()

            # -------- ADMIN --------
            if isinstance(self.current_user, Admin):
                print(f"\n{Colors.BOLD}🛠️ ADMIN მენიუ:{Colors.ENDC}")
                print(f"{Colors.BLUE} 1. ➕ წიგნის დამატება")
                print(f" 2. 🗑️ წიგნის წაშლა")
                print(f" 3. 📚 ყველა წიგნის ნახვა")
                print(f"{Colors.FAIL} 4. 🚪 გასვლა{Colors.ENDC}")

                choice = input(f"\n{Colors.BOLD}👉 აირჩიეთ მოქმედება: {Colors.ENDC}").strip()

                if choice == "1":
                    self.admin_add_book()
                elif choice == "2":
                    self.admin_remove_book()
                elif choice == "3":
                    self.admin_list_books()
                elif choice == "4":
                    sys.exit()
                else:
                    input("❌ არასწორი არჩევანი. Enter...")

            # -------- USER --------
            else:
                print(f"\n{Colors.BOLD}🚀 მთავარი მენიუ:{Colors.ENDC}")
                print(f"{Colors.BLUE} 1. 👤 პირადი გვერდი")
                print(f" 2. 📚 ყველა წიგნის ნახვა")
                print(f" 3. 📖 წიგნის გატანა")
                print(f" 4. 🔄 წიგნის დაბრუნება")
                print(f"{Colors.FAIL} 5. 🚪 გასვლა{Colors.ENDC}")

                choice = input(f"\n{Colors.BOLD}👉 აირჩიეთ მოქმედება: {Colors.ENDC}").strip()

                if choice == "1":
                    self.personal_page()
                elif choice == "2":
                    self.admin_list_books()
                elif choice == "3":
                    self.borrow_book()
                elif choice == "4":
                    self.return_book()
                elif choice == "5":
                    sys.exit()
                else:
                    input("❌ არასწორი არჩევანი. Enter...")

        # 2. პირადი გვერდის "ეკრანი"
    def personal_page(self):
            clear_screen()
            print(f"\n{Colors.BLUE}╔" + "═" * 45 + "╗")
            print(f"║          {Colors.BOLD}👤 თქვენი პირადი გვერდი{Colors.ENDC}            {Colors.BLUE}║")
            print(f"╚" + "═" * 45 + "╝")

            # აქ ვიძახებთ მხოლოდ მონაცემების ბეჭდვას (რეკურსიის გარეშე!)
            self.display_user_data()

            print(f"\n{Colors.BOLD}🔙 დააჭირეთ 'Enter'-ს მთავარ მენიუში დასაბრუნებლად...{Colors.ENDC}")
            input()
            # ფუნქცია მთავრდება და ავტომატურად ბრუნდება main_menu-ში

        # 3. მხოლოდ მონაცემების ბეჭდვა (ჩარჩო)
    def display_user_data(self):
        user = self.current_user

        # მომხმარებლის ძირითადი ინფორმაცია
        print(f"{Colors.BLUE}╔" + "═" * 50 + "╗")
        print(f"║ {Colors.BOLD}👤 მომხმარებელი:{Colors.ENDC} {user.name:<32} {Colors.BLUE}║")
        print(f"║ {Colors.BOLD}📞 ტელეფონი:{Colors.ENDC} {user.phone:<36} {Colors.BLUE}║")
        print(f"╠" + "═" * 50 + "╣")

        # გატანილი წიგნების სექცია
        print(f"║ {Colors.BOLD}📚 გატანილი წიგნები და ვადები:{Colors.ENDC}                {Colors.BLUE}║")

        if not user.borrowed_books:
            print(f"║ {Colors.WARNING}   - ამჟამად გატანილი წიგნები არ გაქვთ. {Colors.ENDC}       {Colors.BLUE}║")
        else:
            for i, b in enumerate(user.borrowed_books):
                # ტექსტის ფორმატირება: წიგნის სახელი და დაბრუნების ვადა
                title_part = f"{i + 1}. {b['title']}"
                date_part = f"📅 ვადა: {b['due_date']}"

                # ვსაზღვრავთ თავისუფალ ადგილს, რომ ჩარჩო არ დაიშალოს
                # 46 არის შიდა სივრცის სიგრძე (50 - გვერდითა სიმბოლოები)
                line = f"  {title_part:<25} | {date_part:<15}"
                print(f"║ {Colors.GREEN}{line:<48}{Colors.BLUE} ║")

        print(f"╚" + "═" * 50 + "╝{Colors.ENDC}")
    # ---------------- BORROW ----------------
    # ---------------- BORROW ----------------
    # ---------------- BORROW (შესწორებული) ----------------
    def borrow_book(self):
        clear_screen()
        print(f"\n{Colors.BLUE}🔎 --- წიგნის ძებნა ---{Colors.ENDC}")
        search_type = input("მოძებნა: 1. სახელით | 2. ავტორით: ").strip()

        if search_type == "1":
            title = input("შეიყვანეთ წიგნის სახელი: ").strip()
            books = self.library.find_books_by_title(title)
            if not books:
                print(f"{Colors.FAIL}❌ ასეთი წიგნი ვერ მოიძებნა{Colors.ENDC}")
                input("\nდააჭირეთ Enter-ს მენიუში დასაბრუნებლად...")
                return
        elif search_type == "2":
            author = input("შეიყვანეთ ავტორი: ").strip()
            books = self.library.find_books_by_author(author)
            if not books:
                print(f"{Colors.FAIL}❌ ასეთი ავტორის წიგნი არ მოიძებნა{Colors.ENDC}")
                input("\nდააჭირეთ Enter-ს მენიუში დასაბრუნებლად...")
                return
        else:
            print(f"{Colors.FAIL}❌ არასწორი არჩევანი{Colors.ENDC}")
            return

        # წიგნის შერჩევა
        book = None
        if len(books) == 1:
            book = books[0]
            print(f"\n{Colors.GREEN}✅ ნაპოვნია: {book.title} | {book.author}{Colors.ENDC}")
        else:
            print(f"\n{Colors.BOLD}📚 ნაპოვნია რამდენიმე წიგნი:{Colors.ENDC}")
            for i, b in enumerate(books):
                print(f"{i + 1}. {b.title} | {b.author} | ⭐ {b.rating}")

            try:
                index = int(input(f"\n{Colors.BOLD}👉 რომელი წიგნის გატანა გსურთ? (ნომერი): {Colors.ENDC}")) - 1
                book = books[index]
            except (ValueError, IndexError):
                print(f"{Colors.FAIL}❌ არასწორი ნომერი{Colors.ENDC}")
                input("\nდააჭირეთ Enter-ს მენიუში დასაბრუნებლად...")
                return

        # გატანის გაფორმება - ხდება მხოლოდ ერთხელ აქ!
        if book:
            days = input(f"{Colors.BOLD}📅 რამდენი ხნით გსურთ გატანა? (მაგ: 10): {Colors.ENDC}").strip()
            # ვამატებთ სიტყვა "დღე"-ს ავტომატურად, თუ მომხმარებელმა მხოლოდ ციფრი დაწერა
            due_date = f"{days} დღე" if days.isdigit() else days

            self.current_user.borrow_book(book.title, due_date)
            self.library.save_users()

            print(f"\n{Colors.GREEN}✅ წიგნი „{book.title}“ წარმატებით გატანილია!{Colors.ENDC}")
            input("\nგასაგრძელებლად დააჭირეთ Enter-ს...")

    # ---------------- RETURN (დაბრუნება) ----------------
    def return_book(self):
        user = self.current_user

        if not user.borrowed_books:
            print(f"{Colors.FAIL}❌ დასაბრუნებელი წიგნები არ გაქვთ{Colors.ENDC}")
            input("\nდააჭირეთ Enter-ს მენიუში დასაბრუნებლად...")
            return

        print(f"\n{Colors.BOLD}📚 თქვენი გატანილი წიგნები:{Colors.ENDC}")
        for i, b in enumerate(user.borrowed_books):
            print(f"{i + 1}. {b['title']} (ვადა: {b['due_date']})")

        try:
            choice = input(
                f"\n{Colors.BOLD}👉 შეიყვანეთ დასაბრუნებელი წიგნების ნომრები (მძიმით გამოყოფილი, მაგ: 1, 2) ან 'q' გასასვლელად: {Colors.ENDC}").strip()

            if choice.lower() == 'q':
                return

            # შეყვანილი ტექსტის დაყოფა მძიმით და ინდექსებად გადაქცევა
            indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip().isdigit()]

            # ინდექსების დალაგება კლებადობით, რომ ამოშლისას სია არ აირიოს
            indices.sort(reverse=True)

            if not indices:
                print(f"{Colors.FAIL}❌ არასწორი ფორმატი{Colors.ENDC}")
                return

            returned_count = 0
            for index in indices:
                if 0 <= index < len(user.borrowed_books):
                    returned = user.return_book(index)
                    print(f"{Colors.GREEN}✅ წიგნი „{returned['title']}“ მონიშნულია დაბრუნებულად.{Colors.ENDC}")
                    returned_count += 1
                else:
                    print(f"{Colors.FAIL}⚠️ წიგნი ნომრით {index + 1} ვერ მოიძებნა.{Colors.ENDC}")

            if returned_count > 0:
                self.library.save_users()
                print(f"\n{Colors.BOLD}🎉 სულ დაბრუნდა {returned_count} წიგნი.{Colors.ENDC}")

                # სურვილისამებრ შეფასება (მხოლოდ ერთხელ)
                rating_input = input(f"\n{Colors.BOLD}⭐ შეაფასეთ წიგნი (0–5) ან გამოტოვეთ: {Colors.ENDC}").strip()

                if rating_input:
                    try:
                        rating_value = float(rating_input)

                        if 0 <= rating_value <= 5:
                            new_avg = self.library.rate_book(returned["title"], rating_value)
                            if new_avg is not None:
                                print(f"{Colors.GREEN}📊 ახალი საშუალო რეიტინგი: {new_avg}{Colors.ENDC}")
                        else:
                            print(f"{Colors.FAIL}❌ რეიტინგი უნდა იყოს 0-დან 5-მდე{Colors.ENDC}")

                    except ValueError:
                        print(f"{Colors.FAIL}❌ გთხოვთ შეიყვანოთ რიცხვი (მაგ: 4.5){Colors.ENDC}")

        except ValueError:
            print(f"{Colors.FAIL}❌ გთხოვთ გამოიყენოთ მხოლოდ ციფრები და მძიმე{Colors.ENDC}")

        input("\nგასაგრძელებლად დააჭირეთ Enter-ს...")

    def admin_add_book(self):
        clear_screen()
        print(f"{Colors.BOLD}➕ წიგნის დამატება{Colors.ENDC}")

        title = input("📖 სახელი: ").strip()
        author = input("✍️ ავტორი: ").strip()
        pages = input("📄 გვერდები: ").strip()
        rating = input("⭐ რეიტინგი: ").strip()

        try:
            self.current_user.add_book(
                self.library,
                title,
                author,
                int(pages),
                float(rating)
            )
            print(f"\n{Colors.GREEN}✅ წიგნი წარმატებით დაემატა!{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}❌ არასწორი მონაცემები{Colors.ENDC}")

        input("\nEnter...")

    def admin_remove_book(self):
        clear_screen()
        print(f"{Colors.BOLD}🗑️ წიგნის წაშლა{Colors.ENDC}")

        title = input("წიგნის ზუსტი სახელი: ").strip()
        self.current_user.remove_book(self.library, title)

        print(f"{Colors.GREEN}✅ თუ არსებობდა, წიგნი წაშლილია{Colors.ENDC}")
        input("\nEnter...")

    def admin_list_books(self):
        clear_screen()
        print(f"{Colors.BOLD}📚 ბიბლიოთეკის წიგნები{Colors.ENDC}\n")

        if not self.library.books:
            print(f"{Colors.WARNING}ბიბლიოთეკა ცარიელია{Colors.ENDC}")
        else:
            for i, b in enumerate(self.library.books):
                print(f"{i + 1}. {b.title} | {b.author} | {b.pages} გვ | ⭐ {b.rating}")

        input("\nEnter...")

