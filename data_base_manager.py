import sqlite3

from category import Category
from expense import Expense


class DataBaseManager:
    def __init__(self,database_name="Expense.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor=self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON")


        self.create_table_categories()
        self.create_table_expenses()

    def create_table_expenses(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "title TEXT NOT NULL,amount REAL NOT NULL CHECK (amount > 0),category_id "
                            "INTEGER NOT NULL,date TEXT NOT NULL,FOREIGN KEY (category_id)REFERENCES "
                            "categories(id))")
        self.connection.commit()

    def create_table_categories(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS  categories (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
        )""")
        self.connection.commit()

    def view_expenses(self):
        self.cursor.execute("SELECT expenses.id,expenses.title,expenses.amount,categories.name,expenses.date FROM expenses JOIN categories on expenses.category_id=categories.id ORDER BY expenses.id")
        rows=self.cursor.fetchall()
        self.cursor.execute("Select SUM(expenses.amount) from expenses")
        total=self.cursor.fetchone()
        return rows,total[0]

    def get_all_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        rows=self.cursor.fetchall()
        categories=[]
        for row in rows:
            categories.append(Category(row[1],row[0]))
        return categories

    def add_expense(self,expense):
        sql="Insert into expenses(title,amount,category_id,date) VALUES(?,?,?,?)"
        values=(expense.title,expense.amount,expense.category_id,expense.date)
        try:
            self.cursor.execute(sql,values)
            self.connection.commit()
            expense.expense_id = self.cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def get_category_by_id(self,category_id):
        self.cursor.execute("SELECT * FROM categories WHERE id=?",(category_id,))
        rows=self.cursor.fetchone()
        if rows is None:
            return None
        return Category(rows[1],rows[0])

    def get_expense_by_id(self,expense_id):
        self.cursor.execute("SELECT * FROM expenses WHERE id=?",(expense_id,))
        expense=self.cursor.fetchone()
        if expense is None:
            return None
        return Expense(expense[1],expense[2],expense[3],expense[4],expense[0])

    def delete_expense(self,expense_id):
        try:
            self.cursor.execute("DELETE FROM expenses WHERE id=?",(expense_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_expense(self,expense):
        sql="Update expenses  set title=?,amount=?,category_id=?,date=? where id=?"
        values=(expense.title,expense.amount,expense.category_id,expense.date)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True

        except sqlite3.IntegrityError:
            return False




