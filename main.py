import json

FILE_NAME = "expenses.json"


def show_menu():
    print("""===== Expense Tracker =====

1. View Expenses
2. Add Expense
3. Delete Expense
4. Edit Expense
5. Show Total Expenses
6. Exit
""")


def load_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Invalid JSON file. Starting with an empty expense list.")
        return []


def save_data(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as json_file:
        json.dump(expenses, json_file, indent=4)


def get_user_input():
    while True:
        try:
            choice = int(input("Enter your choice: "))

            if choice not in range(1, 7):
                print("Please enter a number between 1 and 6.")
                continue

            return choice

        except ValueError:
            print("Please enter a valid number.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. {expense['title']} - €{expense['amount']:.2f}")


def add_expense(expenses):
    while True:
        expense_title = input("Enter expense name: ").strip()
        if not expense_title:
            print("Expense name cannot be empty.")
            continue
        duplicate = False
        for expense in expenses:
            if expense["title"].lower() == expense_title.lower():
                print("This expense already exists.")
                duplicate = True
                break
        if duplicate:
            continue

        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                print("Invalid amount")
                continue
            expenses.append({"title": expense_title, "amount": expense_amount})
            save_data(expenses)
            print("Expense added successfully!")
            break
        except ValueError:
            print("Please enter a valid amount")


def delete_expense(expenses):
    if not expenses:
        print("No expenses found.")
        return

    view_expenses(expenses)

    while True:
        try:
            expense_number = int(input("Which expense do you want to delete? "))

            if expense_number not in range(1, len(expenses) + 1):
                print("Invalid choice.")
                continue

            expenses.pop(expense_number - 1)

            save_data(expenses)

            print("Expense deleted successfully!")
            break

        except ValueError:
            print("Please enter a valid number.")



def edit_expense(expenses):
    if not expenses:
        print("No expenses found.")
        return

    view_expenses(expenses)

    while True:
        try:
            expense_number = int(input("Which expense do you want to edit? "))

            if expense_number not in range(1, len(expenses) + 1):
                print("Invalid choice.")
                continue

            expense = expenses[expense_number - 1]

            field = input("What would you like to edit? (name/amount): ").strip().lower()

            if field == "name":

                while True:
                    new_name = input("Enter new expense name: ").strip()

                    if not new_name:
                        print("Expense name cannot be empty.")
                        continue

                    duplicate = any(
                        item["title"].lower() == new_name.lower()
                        and item != expense
                        for item in expenses
                    )

                    if duplicate:
                        print("An expense with this name already exists.")
                        continue

                    expense["title"] = new_name
                    save_data(expenses)

                    print("Expense updated successfully!")
                    return

            elif field == "amount":

                while True:
                    try:
                        new_amount = float(input("Enter new amount: "))

                        if new_amount <= 0:
                            print("Amount must be greater than zero.")
                            continue

                        expense["amount"] = new_amount

                        save_data(expenses)

                        print("Expense updated successfully!")
                        return

                    except ValueError:
                        print("Please enter a valid amount.")

            else:
                print("Please enter 'name' or 'amount'.")

        except ValueError:
            print("Please enter a valid number.")




def show_total_expenses(expenses):
    if not expenses:
        print("No expenses found")
        return
    for expense in expenses:
        print(f"{expense['title']:<15}{expense['amount']:>6.2f}")
    total_expenses = sum(expense["amount"] for expense in expenses)
    print("\n------------------\n")
    print(f"Total: €{total_expenses:.2f}")


def main():
    expenses = load_data()
    while True:
        show_menu()
        user_choice = get_user_input()
        if user_choice == 1:
            view_expenses(expenses)
        elif user_choice == 2:
            add_expense(expenses)
        elif user_choice == 3:
            delete_expense(expenses)
        elif user_choice == 4:
            edit_expense(expenses)
        elif user_choice == 5:
            show_total_expenses(expenses)
        elif user_choice == 6:
            print("Thank you for using Expense Tracker!")
            break


if __name__ == '__main__':
    main()
