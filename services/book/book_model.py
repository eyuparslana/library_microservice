

class BookModel:
    def __init__(self, book_name, isbn, author, publish_date=None, genre=None):
        self.book_name = book_name
        self.isbn = isbn
        self.author = author
        self.publish_date = publish_date
        self.genres = genre
