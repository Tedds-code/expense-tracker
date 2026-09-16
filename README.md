This project is a simple expense-tracker for personal use and education.

## Overview:

This simple budget tracker was made as a simple project for educational purposes. It serves as a working progress to learn about 
the basics of python needed for real world application, as well as a personal expense tracker to manage expenses.

## Features:

The project includes the following functions of:
    • adding items
    • filtering according to category, year, month, day, or any combination
    • calculating the total amount for the expenses on screen
    • deleting items
    • viewing items in a graphical environment
    • checking for input validity
    • pie chart and percentages of total expenses each chategory takes up
     
    
## Tech stack:

Python, Flask, SQLite, pywebview, pytest


## Project Structure:

expense-tracker/
├── README.md
├── app.py
├── database.py
├── desktop.py
├── run.sh
├── expense-tracker.desktop
├── icon.png
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
└── tests/
    ├── __init__.py
    └── test_app.py


## Setup

1. Clone or download this repository
2. Navigate into the project folder:
   cd expense-tracker
3. Create a virtual environment:
   python3 -m venv venv
4. Activate it:
   source venv/bin/activate   (Mac/Linux)
   venv\Scripts\activate      (Windows)
5. Install dependencies:
   pip install -r requirements.txt


## Running the app

### As a web app
   python app.py
Then visit http://127.0.0.1:5000 in your browser.

### As a desktop app
   python desktop.py
This opens the app in its own native window.

### Desktop launcher (Linux)
A `.desktop` launcher file (`expense-tracker.desktop`) is included for 
opening the app directly from your applications menu, without using the 
command line. To install it:

   cp expense-tracker.desktop ~/.local/share/applications/

Make sure `run.sh` is executable first:
   chmod +x run.sh


## Running Tests

This project uses pytest for automated testing.

Run all tests with:
   pytest

What's covered:
- Creating expenses, including input validation (missing fields, 
  invalid types, negative amounts)
- Listing all expenses
- Filtering expenses by category
- Deleting expenses, including handling requests for IDs that don't exist
- Filtering by year, month, day, and combinations of category and date filters

Tests run against a separate test database that is created and 
deleted automatically after each test. Your real expense data is never 
touched.


## API Endpoints

| Method | Endpoint                                         | Description                                         |
|--------|--------------------------------------------------|-----------------------------------------------------|
| GET    | /expenses                                        | List all expenses                                   |
| GET    | /expenses?category=<name>                        | List expenses filtered by category                  |
| POST   | /expenses                                        | Create a new expense                                |
| DELETE | /expenses/<id>                                   | Delete an expense by its ID                         |
| GET    | /expenses                                        | List all expenses                                   |
| GET    | /expenses?category=<name>                        | Filter by category                                  |
| GET    | /expenses?year=<yyyy>                            | Filter by year                                      |
| GET    | /expenses?month=<mm>                             | Filter by month                                     |
| GET    | /expenses?day=<dd>                               | Filter by day                                       |
| GET    | /expenses?category=<name>&year=<yyyy>&month=<mm> | Any combination of filters can be used together     |


### POST /expenses — request body

   {
     "amount": 20.5,
     "category": "food",
     "description": "Groceries",
     "date": "2026-08-21"
   }

`description` is optional. All other fields are required. `amount` must 
be a positive number.

### Response codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 200  | Success (GET, DELETE)                        |
| 201  | Expense created successfully (POST)          |
| 400  | Invalid or missing input                     |
| 404  | Expense not found (DELETE on non-existent id)|



## Future improvements

    • Windows desktop launcher 
	• pie chart / bar chart for the percentage of the total spent per category


## Author 

Theodore Christopoulos
