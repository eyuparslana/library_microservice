

class LoanModel:

    def __init__(self, book_id, loaned_by=None, due_date=None):
        self.book_id = book_id
        self.loaned_by = loaned_by
        self.due_date = due_date
