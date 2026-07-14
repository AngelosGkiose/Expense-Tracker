from datetime import date

import expense
from category import Category
from data_base_manager import DataBaseManager
from expense import Expense



class ExpenseTrackerSystem:
    def __init__(self):
        self.database=DataBaseManager()

    def get_expense_from_user(self):
        try:
            expense_id=int(input("Enter expense id: ").strip())
            if expense_id <= 0:
                print("Expense ID must be greater than 0.")
                return None
        except ValueError:
            print("Please enter a numeric value")
            return None
        expense=self.database.get_expense_by_id(expense_id)
        if not expense:
            print("No such expense found\n")
            return None
        return expense

    def handle_view_expenses(self):
        expenses,total_amount=self.database.view_expenses()
        if not expenses:
            print("No expenses found!")
            return
        print("\n===== All Expenses =====")
        print("""ID  Title              Amount     Category        Date
        -----------------------------------------------------------""")
        for expense in expenses:
            print(expense[0],expense[1],expense[2],expense[3],expense[4])
        print("-----------------------------------------------------------")
        print(f"Total Expenses:{total_amount} ")

    def handle_add_expense(self):
        expense_title=input("Enter expense title: ").strip()
        if not expense_title:
            print("Expense title must not be empty")
            return
        try:
            expense_amount=float(input("Enter expense amount: "))
            if expense_amount <= 0 :
                print("Expense amount must be positive")
                return
        except ValueError:
            print("Please enter a numeric value")
            return
        categories=self.database.get_all_categories()
        if not categories:
            print("No category found\n")
            print("Please add a category first.")
            return
        print("Available Categories\n")
        for category in categories:
            print(category)
        try:
            category_id=int(input("Enter category id: "))
            if category_id<= 0 :
                print("Please enter a valid category id")
                return
            found_category=self.database.get_category_by_id(category_id)
            if found_category is None:
                print("No such category found\n")
                return
        except ValueError:
            print("Please enter a numeric value")
            return
        expense=Expense(expense_title,expense_amount,category_id,date.today().isoformat())
        success=self.database.add_expense(expense)
        if not success:
            print("Failed to add expense")
        else:
            print("Successfully added expense")

    def handle_delete_expense(self):
        expense=self.get_expense_from_user()
        if expense is None:
            return
        print(expense)

        confirmation = input(
            "Are you sure you want to delete this expense? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            return
        success=self.database.delete_expense(expense.expense_id)
        if success:
            print("Successfully deleted expense")
        else :
            print("Failed to delete expense")

    def handle_update_expense(self):
        expense=self.get_expense_from_user()
        if expense is None:
            return
        print("Expense Found!")
        print(expense)
        print("Leave empty to keep the current value.")
        expense_title=input(f"New title [{expense.title}]: ").strip()
        expense_amount=(input("New expense amount: ")).strip()
        expense_category_id=(input("New expense category id: ")).strip()
        if expense_amount:
            try:
                amount = float(expense_amount)

                if amount <= 0:
                    print("amount must be greater than 0.")
                    return

            except ValueError:
                print("Age must be an integer.")
                return

            expense.amount = amount
        if expense_category_id:
            try:
                category_id = int(expense_category_id)
                if category_id <= 0:
                    print("Category id must be greater than 0.")
                    return
                found_category = self.database.get_category_by_id(category_id)
                if found_category is None:
                    print("No such category found\n")
                    return
            except ValueError:
                print("Category id  must be an integer.")
                return
            expense.category_id=found_category.category_id

        if expense_title:
            expense.title  = expense_title
        success=self.database.update_expense(expense)
        if success:
            print("Successfully updated expense")
        else:
            print("Failed to update expense")







