class Expense:
    def __init__(self, title, amount, category_id=None, date=None, expense_id=None):
        self.expense_id = expense_id
        self.title = title
        self.amount = amount
        self.category_id = category_id   
        self.date = date

    def __str__(self):
        return (
            f"ID: {self.expense_id} | "
            f"Title: {self.title} | "
            f"Amount: €{self.amount:.2f} | "
            f"Date: {self.date}"
        )
