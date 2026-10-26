# 💰 Expense Tracker

A simple expense tracker built with Python and Streamlit. Add, view and delete expenses, and see your spending at a glance. Data is saved locally in `expenses.json`.

## Features

- 🏠 Home page with total spent, this month's spending, expense count and recent expenses
- ➕ Add expenses (date is added automatically)
- 📋 View all expenses in a table
- 💵 Total spending with a by-category bar chart
- 🗑️ Delete expenses date-wise (one expense, or all on a date)
- 💾 Data persists in `expenses.json`

## Setup

1. Install [uv](https://docs.astral.sh/uv/) (Windows PowerShell):
   ```
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
2. Create and activate a virtual environment:
   ```
   uv venv
   .venv\Scripts\activate
   ```
3. Install Streamlit:
   ```
   uv pip install streamlit
   ```

## Run

```
streamlit run expense_tracker-web.py
```

The app opens at http://localhost:8501.

> Don't use the VS Code ▶ Run button. Always start the app with `streamlit run`.

## Project structure

```
ExpenseTracker/
├── expense_tracker-web.py   # Streamlit app
├── expense_tracker.py       # Original CLI version
├── expenses.json            # Saved expenses
└── README.md
```

## Data format

Each expense in `expenses.json` looks like:

```json
{
    "id": 1,
    "description": "Lunch",
    "amount": 200,
    "category": "Food",
    "date": "2026-10-26"
}
```

## Built with

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
