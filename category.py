class Category:
    def __init__(self,name,category_id=None):
        self.category_id = category_id
        self.name = name

    def __str__(self):
        return (
            f"ID: {self.category_id} | "
            f"Name: {self.name}"
        )