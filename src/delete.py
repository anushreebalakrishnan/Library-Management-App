import pandas as pd
from sqlalchemy import text
import db

# ------- FRIENDS ----------------

def delete_friend(friend):
    engine = db.get_engine()

    # Check if this friend currently has any active loans
    loans = pd.read_sql("loans", con=engine)
    if friend["friend_id"] in loans["friend_id"].values:
        return False, f"Can't remove '{friend['name']}' — they currently have a book on loan. It needs to be returned first."

    delete_query = """
        DELETE FROM friends
        WHERE friend_id = :val;
    """

    with engine.begin() as connection:
        connection.execute(
            text(delete_query),
            {"val": friend["friend_id"]}
        )

    return True, f"Removed '{friend['name']}' from 'friends'."

# ------- BOOKS ----------------

def delete_book(book):
    engine = db.get_engine()

    # Check if this book currently has an active loan
    loans = pd.read_sql("loans", con=engine)
    if book["isbn"] in loans["isbn"].values:
        return f"Can't remove '{book['title']}' — it's currently on loan. Return it first."

    delete_query = """
        DELETE FROM books
        WHERE isbn = :val;
    """

    with engine.begin() as connection:
        connection.execute(
            text(delete_query),
            {"val": book["isbn"]}
        )

    return f"Removed '{book['title']}' from 'books'."

# ------- LOANS ----------------

def delete_loan(loan):
    engine = db.get_engine()

    delete_query = """
        DELETE FROM loans
        WHERE loan_id = :val;
    """

    with engine.begin() as connection:
        connection.execute(
            text(delete_query),
            {"val": loan["loan_id"]}
        )
        # Mark the book as available again now that it's back
        connection.execute(
            text("UPDATE books SET is_available = 1 WHERE isbn = :isbn"),
            {"isbn": loan["isbn"]}
        )

    return f"'{loan['title']}' marked as returned."