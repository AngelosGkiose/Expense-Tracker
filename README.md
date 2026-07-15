# Expense Tracker (Python + SQLite)

A command-line Expense Tracker application built with **Python**, **Object-Oriented Programming (OOP)** and **SQLite**.

The application allows users to manage expenses and categories while storing all data in a SQLite database.

## Features

### Expense Management

* View all expenses
* Add a new expense
* Update an existing expense
* Delete an expense

### Category Management

* View all categories
* Add a new category
* Delete a category
* Prevent deletion of categories that are still used by expenses

### Reports

* Spending by category
* Monthly expense report
* Total expenses for the selected month

## Database Design

The application uses two main tables:

### Categories

* id
* name

### Expenses

* id
* title
* amount
* category_id
* date

The tables are connected using a **FOREIGN KEY** relationship.

## Technologies Used

* Python 3
* SQLite3
* Object-Oriented Programming (OOP)

## SQL Concepts Practiced

* CRUD Operations
* PRIMARY KEY
* FOREIGN KEY
* AUTOINCREMENT
* INNER JOIN
* GROUP BY
* SUM()
* ORDER BY
* strftime() for date filtering
* CHECK constraints
* UNIQUE constraints



## Learning Goals

This project was built to practice:

* Object-Oriented Programming
* SQLite database design
* Database normalization
* SQL queries
* CRUD operations
* Input validation
* Clean project structure
* Separation of responsibilities between UI, business logic and database layers

## Future Improvements

* Search expenses
* Export reports to CSV
* Budget tracking
* Expense statistics
* Web version using Flask or Django
* User authentication
