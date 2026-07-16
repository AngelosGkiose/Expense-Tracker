import json

from expense_tracker_system import ExpenseTrackerSystem

FILE_NAME = "expenses.json"


def show_menu():
    print("""===== Expense Tracker =====

1. View All Expenses
2. Add Expense
3. Update Expense
4. Delete Expense

5. View All Categories
6. Add Category
7. Delete Category

8. Spending by Category
9. Monthly Report
10. Exit
""")




def get_user_input():
    while True:
        try:
            choice = int(input("Enter your choice: "))

            if choice not in range(1, 11):
                print("Please enter a number between 1 and 10.")
                continue

            return choice

        except ValueError:
            print("Please enter a valid number.")




def main():
    system=ExpenseTrackerSystem()
    try:
        while True:
            show_menu()
            user_choice = get_user_input()
            if user_choice == 1:
                system.handle_view_expenses()
            elif user_choice == 2:
                system.handle_add_expense()
            elif user_choice == 3:
                system.handle_update_expense()
            elif user_choice == 4:
                system.handle_delete_expense()
            elif user_choice == 5:
                system.handle_view_categories()
            elif user_choice == 6:
                system.handle_add_category()
            elif user_choice == 7:
                system.handle_delete_category()
            elif user_choice == 8:
                system.handle_get_spending_by_category()
            elif user_choice == 9:
                system.handle_monthly_report()
            elif user_choice == 10:
                print("Thank you for using Expense Tracker!")
                break
    finally:
        system.close()





if __name__ == '__main__':
    main()
