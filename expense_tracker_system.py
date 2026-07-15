from datetime import date

from category import Category
from data_base_manager import DataBaseManager
from EXPENSE import Expense



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
        categories=self.database.get_all_categories()
        if not categories:
            print("No category found\n")
            print("Please add a category first.")
            return
        print("Available Categories\n")
        for category in categories:
            print(category)
        expense_category_id=(input("New expense category id: ")).strip()
        if expense_amount:
            try:
                amount = float(expense_amount)

                if amount <= 0:
                    print("amount must be greater than 0.")
                    return

            except ValueError:
                print("Amount must be a number.")
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

    def handle_view_categories(self):
        categories=self.database.get_all_categories()
        if not categories:
            print("No category found\n")
            print("Please add a category first.")
            return
        print(" ===== Categories =====\n")
        for category in categories:
            print(category)

    def handle_add_category(self):
        category_name=input("Enter category name: ").strip().title()
        if not category_name:
            print("Please enter a valid category name")
            return
        category=Category(category_name)
        success=self.database.add_category(category)
        if not success:
            print("A category with this name already exists.")
        else:
            print("Successfully added category")

    def handle_delete_category(self):
        categories = self.database.get_all_categories()

        if not categories:
            print("No categories found.")
            return

        for category in categories:
            print(category)
        try:
            category_id = int(input("Enter category id: "))
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
        has_expenses = self.database.has_expenses(
            found_category
        )
        if has_expenses:
            print("Cannot delete this category.It has expenses assigned to it.")
            return
        confirmation = input(
            "Are you sure you want to delete this category? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            return
        success= self.database.delete_category(found_category)
        if success:
            print("Successfully deleted category")
        else :
            print("Failed to delete category")

    def handle_get_spending_by_category(self):
        category_spending=self.database.get_spending_by_category()
        if not category_spending:
            print("No spending found.")
            return
        print("===== Spending by Category =====\n")
        for category in category_spending:
            print(f"{category[0]}     ${category[1]}")

    def handle_monthly_report(self):
        try:
            year=int(input("Enter year: "))
            if year <= 0:
                print(" Year must be greater than 0.")
                return
        except ValueError:
            print("Year  must be an integer.")
            return
        try:
            month=int(input("Enter month: "))
            if month < 1 or month > 12:
                print("Month must be between 1 and 12.")
                return
        except ValueError:
            print("Month must be an integer.")
            return
        month_filter = f"{year:04d}-{month:02d}"
        rows,total_amount=self.database.get_monthly_report(month_filter)
        if not rows:
            print(f"No expenses found for {month_filter}")
            return
        print(f"===== Monthly Report:{month_filter} =====\n")
        print("""ID  Title              Amount     Category        Date
               -----------------------------------------------------------""")
        for row in rows:
            print(f"{row[0]}   {row[1]}    ${row[2]}    {row[3]}    {row[4]}")
        print("-----------------------------------------------------------")
        print(f"Total Expenses: ${total_amount} ")











