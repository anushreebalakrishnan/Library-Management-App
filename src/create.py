import pandas as pd
import db
from sqlalchemy import text

# ---------- FRIENDS ------------------------------
def create_friend(name, max_loans=2, notes=None):
    engine = db.get_engine()

    if not name or not name.strip():
        return "Can't add friend — name can't be blank."

    df = pd.DataFrame([[name.strip(), max_loans, notes]],
                      columns=["name",
                               "max_loans",
                               "notes"])

    df.to_sql("friends", if_exists="append", con=engine, index=False)

    return f"Added '{name}' to 'friends'."

# ---------- BOOKS ------------------------------------
def create_book(title, isbn, author=None, genre=None):
    engine = db.get_engine()

    if not title or not title.strip():
        return "Can't add book — title can't be blank."

    if not isbn or not isbn.strip():
        return "Can't add book — ISBN can't be blank."

    # Check if this ISBN already exists before trying to insert
    existing = pd.read_sql("books", con=engine)
    if isbn.strip() in existing["isbn"].values:
        return f"Can't add book — ISBN '{isbn}' already exists in the library."

    df = pd.DataFrame([[title.strip(), isbn.strip(), author, genre]],
                      columns=["title",
                               "isbn",
                               "author",
                               "genre"])

    df.to_sql("books", if_exists="append", con=engine, index=False)

    return f"Added '{title}' to 'books'."

# ------------------------LOANS -------------------------------------------------------------------------

def create_loan(friend, book, loan_date, next_contact, notes=None):
    engine = db.get_engine()

    # Count how many books this friend currently has out
    loans = pd.read_sql("loans", con=engine)
    current_loans = len(loans[loans["friend_id"] == friend["friend_id"]])

    if current_loans >= friend["max_loans"]:
       return f"⚠️ You've reached the maximum limit of {int(friend['max_loans'])} book(s) for '{friend['name']}'."
    df = pd.DataFrame([[book["isbn"], friend["friend_id"], loan_date, next_contact, notes]],
                      columns=["isbn",
                               "friend_id",
                               "loan_date",
                               "next_contact",
                               "notes"])

    df.to_sql("loans", if_exists="append", con=engine, index=False)

    message = f"'{friend['name']}' borrowed '{book['title']}'."
    return message
