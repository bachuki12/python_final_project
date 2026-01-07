class Book:
    def __init__(self, title, author, pages, rating=0.0, ratings=None):
        self.title = title
        self.author = author
        self.pages = pages
        self.ratings = ratings or []

        # თუ ძველი JSON-დან მოდის მხოლოდ rating
        if rating and not self.ratings:
            self.ratings = [rating]

        self.rating = self.calculate_rating()

    def add_rating(self, value):
        self.ratings.append(value)
        self.rating = self.calculate_rating()

    def calculate_rating(self):
        if not self.ratings:
            return 0.0
        return round(sum(self.ratings) / len(self.ratings), 2)

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "pages": self.pages,
            "ratings": self.ratings,
            "rating": self.rating
        }

    @staticmethod
    def from_dict(data):
        return Book(
            title=data["title"],
            author=data["author"],
            pages=data["pages"],
            rating=data.get("rating", 0.0),
            ratings=data.get("ratings", [])
        )
