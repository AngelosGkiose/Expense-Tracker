from datetime import date

from category import Category
from data_base_manager import DataBaseManager
from EXPENSE import Expense



class ExpenseTrackerSystem:
    def __init__(self):
        self.database=DataBaseManager()

    # --------------------------------------------------
    # HELPER METHODS
    # --------------------------------------------------

    def get_expense_from_user(self):
        while True:
            user_input = input("Enter expense id (0 to cancel): ").strip()
            if user_input == "0":
                print("Operation cancelled.")
                return None
            try:
                expense_id = int(user_input)
                if expense_id <= 0:
                    print("Expense ID must be greater than 0.")
                    continue
            except ValueError:
                print("Please enter a numeric value.")
                continue
            expense = self.database.get_expense_by_id(expense_id)
            if expense is None:
                print("No such expense found.")
                continue
            return expense

    def get_category_from_user(self):
        categories = self.database.get_all_categories()

        if not categories:
            print("No category found.")
            print("Please add a category first.")
            return None

        print("Available Categories\n")

        for category in categories:
            print(category)

        while True:
            user_input = input("Enter category id (0 to cancel): ").strip()
            if user_input == "0":
                print("Operation cancelled.")
                return None
            try:
                category_id = int(user_input)
                if category_id <= 0:
                    print("Category id must be greater than 0.")
                    continue
            except ValueError:
                print("Category id must be an integer.")
                continue
            category = self.database.get_category_by_id(category_id)
            if category is None:
                print("No such category found.")
                continue
            return category

    @staticmethod
    def get_expense_title(message):
        while True:
            expense_title = input(message).strip()
            if not expense_title:
                print("Expense title must not be empty.")
                continue
            return expense_title

    @staticmethod
    def get_expense_amount(message):
        while True:
            user_input = input(message).strip()
            try:
                expense_amount = float(user_input)
                if expense_amount <= 0:
                    print("Expense amount must be positive.")
                    continue
                return expense_amount
            except ValueError:
                print("Please enter a numeric value.")

    @staticmethod
    def get_optional_expense_amount(message):
        while True:
            user_input = input(message).strip()
            if not user_input:
                return None
            try:
                amount = float(user_input)
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                return amount
            except ValueError:
                print("Amount must be a number.")

    @staticmethod
    def get_confirmation(message):
        while True:
            confirmation = input(
                message
            ).strip().lower()
            if confirmation == "yes":
                return True
            if confirmation == "no":
                return False
            print("Please enter yes or no.")

    @staticmethod
    def get_positive_year():
        while True:
            user_input = input(
                "Enter year (0 to cancel): "
            ).strip()
            if user_input == "0":
                print("Operation cancelled.")
                return None
            try:
                year = int(user_input)
                if year <= 0:
                    print("Year must be greater than 0.")
                    continue
                return year
            except ValueError:
                print("Year must be an integer.")

    @staticmethod
    def get_valid_month():
        while True:
            user_input = input(
                "Enter month (1-12 or 0 to cancel): "
            ).strip()
            if user_input == "0":
                print("Operation cancelled.")
                return None
            try:
                month = int(user_input)
                if month < 1 or month > 12:
                    print("Month must be between 1 and 12.")
                    continue
                return month
            except ValueError:
                print("Month must be an integer.")

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
        expense_title = self.get_expense_title(
            "Enter expense title: "
        )
        expense_amount = self.get_expense_amount(
            "Enter expense amount: "
        )
        found_category = self.get_category_from_user()
        if found_category is None:
            return
        expense=Expense(expense_title,expense_amount,found_category.category_id,date.today().isoformat())
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
        confirmation = self.get_confirmation("Are you sure you want to delete this expense? (yes/no): ")
        if not confirmation:
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
        expense_amount = self.get_optional_expense_amount(f"New expense amount [{expense.amount}]: ")
        categories=self.database.get_all_categories()
        if not categories:
            print("No category found\n")
            print("Please add a category first.")
            return
        print("Available Categories\n")
        for category in categories:
            print(category)
        while True:
            expense_category_id = input("New expense category id (leave empty to keep current): ").strip()
            if not expense_category_id:
                found_category = None
                break
            try:
                category_id = int(expense_category_id)
                if category_id <= 0:
                    print("Category id must be greater than 0.")
                    continue
            except ValueError:
                print("Category id must be an integer.")
                continue
            found_category = self.database.get_category_by_id( category_id)
            if found_category is None:
                print("No such category found.")
                continue
            break
        if expense_amount is not None:
            expense.amount = expense_amount
        if found_category is not None:
            expense.category_id = found_category.category_id
        if expense_title:
            expense.title = expense_title
        success = self.database.update_expense(expense)
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
        while True:
            category_name = input(
                "Enter category name (0 to cancel): ").strip().title()
            if category_name == "0":
                print("Operation cancelled.")
                return
            if not category_name:
                print("Please enter a valid category name")
                continue
            category = Category(category_name)
            success = self.database.add_category(category)
            if not success:
                print(
                "A category with this name already exists.")
                continue
            print("Successfully added category")
            return

    def handle_delete_category(self):
        found_category = self.get_category_from_user()
        if found_category is None:
            return
        has_expenses = self.database.has_expenses(found_category)
        if has_expenses:
            print("Cannot delete this category. ""It has expenses assigned to it.")
            return
        confirmation = self.get_confirmation("Are you sure you want to delete ""this category? (yes/no): ")
        if not confirmation:
            print("Deletion cancelled.")
            return
        success = self.database.delete_category(found_category)
        if success:
            print("Successfully deleted category")
        else:
            print("Failed to delete category")

    def handle_get_spending_by_category(self):
        category_spending=self.database.get_spending_by_category()
        if not category_spending:
            print("No spending found.")
            return
        print("===== Spending by Category =====\n")
        for category in category_spending:
            print(f"{category[0]}     ${category[1]}")
        print("\n")

    def handle_monthly_report(self):
        year = self.get_positive_year()
        if year is None:
            return
        month = self.get_valid_month()
        if month is None:
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

    def close(self):
        self.database.close_connection()









