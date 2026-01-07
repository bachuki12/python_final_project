class Book:
    def __init__(self, title, author, pages, rating):
        self.title = title
        self.author = author
        self.pages = pages
        self.rating = rating

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Book(**data)
