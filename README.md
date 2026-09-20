# 📚 Liana's Library

A personal library management app built with **Streamlit** and **MySQL**, for tracking books, friends, and loans in a small, shared book collection.

Instead of losing track of who borrowed what, Liana's Library keeps a simple, interactive record of every book, every friend, and every loan — with built-in safeguards against common mistakes (like deleting a book that's still on loan, or lending past someone's borrowing limit).

## ✨ Features

- **Friends** — add, view, edit, and remove friends, each with their own borrowing limit (`max_loans`) and notes
- **Books** — add, view, edit, and remove books, with author, genre, and ISBN tracking
- **Loans** — lend a book to a friend, track next check-in dates, and mark books as returned
- **Live stats** — see books available, total books, active loans, and overdue loans at a glance
- **Safety checks**:
  - Can't delete a friend or book that currently has an active loan
  - Can't lend a book past a friend's personal borrowing limit
  - Confirmation step before deleting a friend or book
  - Blank names/ISBNs and duplicate ISBNs are caught before they hit the database

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Database:** MySQL
- **ORM / DB access:** SQLAlchemy + PyMySQL
- **Data handling:** pandas

## 📂 Project Structure

```
├── app.py              # Main Streamlit app — UI and page routing
├── db.py                # Shared database engine (single connection)
├── login.py             # Login screen and MySQL connection handling
├── create.py             # Create operations (friends, books, loans)
├── read.py               # Read operations and display formatting
├── update.py              # Update operations
├── delete.py               # Delete operations (with safety checks)
├── sample_library1.sql       # Database schema + sample seed data
└── environment.yml            # Conda environment definition
```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

### 2. Set up the environment
```bash
conda env create -f environment.yml
conda activate lianes-lib-env
```

### 3. Set up the database
Run `sample_library1.sql` in your local MySQL instance to create the schema and load sample data:
```bash
mysql -u root -p < sample_library1.sql
```

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Log in
Enter your local MySQL username and password on the login screen to connect.

## 📸 Screenshots

*(Add a screenshot or two of the app here once it's running!)*

## 📝 Notes

This project was built as part of a data analytics bootcamp capstone, focused on practicing full CRUD application design with a real relational database backend.
