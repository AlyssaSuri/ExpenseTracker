import json
import os
from datetime import date

import pandas as pd
import streamlit as st

FILE_NAME = "expenses.json"


# ---------- LOAD / SAVE DATA ----------

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- PAGE SETUP + STYLE ----------

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

st.markdown(
    """
    <style>
    /* bordered cards: rounded corners + soft shadow */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
    }
    /* rounded buttons */
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    /* bolder headings */
    h1, h2, h3 { font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit reruns the script on every click, so keep data in session_state
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

st.sidebar.caption("💰 Expense Tracker")


# ---------- 0. HOME ----------

def home_page():
    expenses = st.session_state.expenses

    st.title("💰 Expense Tracker")
    st.write("Track where your money goes, one expense at a time.")

    # quick numbers
    total = sum(e["amount"] for e in expenses)
    this_month = date.today().isoformat()[:7]  # e.g. "2026-10"
    month_total = sum(
        e["amount"] for e in expenses if e.get("date", "").startswith(this_month)
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Total spent", total)
    with col2:
        with st.container(border=True):
            st.metric("This month", month_total)
    with col3:
        with st.container(border=True):
            st.metric("Expenses", len(expenses))

    # quick links
    st.subheader("Quick actions")
    c1, c2, c3, c4 = st.columns(4)
    c1.page_link(add_pg, label="Add", icon=":material/add_circle:")
    c2.page_link(view_pg, label="View", icon=":material/table:")
    c3.page_link(total_pg, label="Totals", icon=":material/payments:")
    c4.page_link(delete_pg, label="Delete", icon=":material/delete:")

    # recent expenses
    st.subheader("Recent expenses")
    if not expenses:
        st.info("No expenses yet. Use **Add** to log your first one!")
    else:
        recent = pd.DataFrame(expenses).tail(5).iloc[::-1]
        st.dataframe(recent, hide_index=True)


# ---------- 1. ADD EXPENSE ----------

def add_page():
    expenses = st.session_state.expenses

    st.title("➕ Add expense")
    st.write(f"Date: **{date.today().isoformat()}** (added automatically)")

    with st.container(border=True):
        with st.form("add_form", clear_on_submit=True, border=False):
            description = st.text_input("Expense description")
            amount = st.number_input("Expense amount", min_value=1, step=1)
            category = st.text_input("Category")
            submitted = st.form_submit_button("Add expense", type="primary")

    if submitted:
        if not description.strip():
            st.error("Please enter a description.")
        else:
            expense_id = max((e["id"] for e in expenses), default=0) + 1

            expenses.append(
                {
                    "id": expense_id,
                    "description": description.strip(),
                    "amount": int(amount),
                    "category": category.strip(),
                    "date": date.today().isoformat(),
                }
            )
            save_expenses(expenses)
            st.success("Expense added!")


# ---------- 2. VIEW EXPENSES ----------

def view_page():
    expenses = st.session_state.expenses

    st.title("📋 All expenses")

    if not expenses:
        st.info("No expenses yet")
    else:
        st.dataframe(pd.DataFrame(expenses), hide_index=True)


# ---------- 3. TOTAL SPENDING ----------

def total_page():
    expenses = st.session_state.expenses

    st.title("💵 Total spending")

    total = sum(e["amount"] for e in expenses)
    with st.container(border=True):
        st.metric("Total expenses", total)

    if expenses:
        df = pd.DataFrame(expenses)
        st.subheader("By category")
        st.bar_chart(df.groupby("category")["amount"].sum())


# ---------- 4. DELETE AN EXPENSE (DATE WISE) ----------

def delete_page():
    expenses = st.session_state.expenses

    st.title("🗑️ Delete expense")

    if not expenses:
        st.info("No expenses to delete")
        return

    # Step 1: pick a date (newest first)
    dates = sorted({e.get("date", "Unknown") for e in expenses}, reverse=True)
    selected_date = st.selectbox("Select date", dates)

    # Step 2: show only that day's expenses
    day_expenses = [e for e in expenses if e.get("date", "Unknown") == selected_date]

    st.write(f"Expenses on **{selected_date}**")
    st.dataframe(pd.DataFrame(day_expenses), hide_index=True)
    with st.container(border=True):
        st.metric("Total for this date", sum(e["amount"] for e in day_expenses))

    # Step 3a: delete one expense from that date
    selected_id = st.selectbox(
        "Choose the expense to delete",
        options=[e["id"] for e in day_expenses],
        format_func=lambda i: next(
            f'{e["id"]} - {e["description"]} ({e["amount"]})'
            for e in day_expenses
            if e["id"] == i
        ),
    )

    if st.button("Delete selected expense", type="primary"):
        st.session_state.expenses = [e for e in expenses if e["id"] != selected_id]
        save_expenses(st.session_state.expenses)
        st.toast("Expense deleted")
        st.rerun()

    # Step 3b: delete everything on that date
    st.divider()
    confirm = st.checkbox(f"Yes, delete ALL expenses on {selected_date}")

    if st.button("Delete all for this date", disabled=not confirm):
        st.session_state.expenses = [
            e for e in expenses if e.get("date", "Unknown") != selected_date
        ]
        save_expenses(st.session_state.expenses)
        st.toast(f"Deleted all expenses on {selected_date}")
        st.rerun()


# ---------- NAVIGATION (must come AFTER the functions) ----------

home_pg = st.Page(home_page, title="Home", icon=":material/home:", default=True)
add_pg = st.Page(add_page, title="Add expense", icon=":material/add_circle:")
view_pg = st.Page(view_page, title="View expenses", icon=":material/table:")
total_pg = st.Page(total_page, title="Total spending", icon=":material/payments:")
delete_pg = st.Page(delete_page, title="Delete expense", icon=":material/delete:")

pg = st.navigation([home_pg, add_pg, view_pg, total_pg, delete_pg])
pg.run()