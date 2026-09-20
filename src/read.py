import pandas as pd
import db

# --------- SHARED HELPER -------------

def prettify_df(df):
    # Turns raw column names like "max_loans" into "Max loans" for nicer display,
    # and keeps ISBN fully uppercase since it's an abbreviation, not a word.
    df.columns = [c.upper() if c == "isbn" else c.replace("_", " ").capitalize() for c in df.columns]
    return df.fillna("")  # blank instead of "None" in the table shown to users

# --------- FRIENDS -------------

def read_friends():
    # Pulls the WHOLE friends table straight from MySQL into a pandas DataFrame
    engine = db.get_engine()
    return pd.read_sql("friends", con=engine)

def display_friends():
    friends = read_friends()
    return friends.pipe(prettify_df).loc[:, "Name":]

   

    
# --------- BOOKS -------------

def read_books(available_only=False):
    engine = db.get_engine()
    books = pd.read_sql("books", con=engine)

    if available_only:
        # Returning a book DELETES its loan row (see delete_loan in delete.py),
        # so a book is "available" simply if no loan row references its isbn at all
        loans = pd.read_sql("loans", con=engine)
        books = books[~books["isbn"].isin(loans["isbn"])]

    return books

def display_books(available_only=False):
    books = read_books(available_only)
    return books.pipe(prettify_df).sort_values(by="Title") 

def count_available_books():
    engine = db.get_engine()
    query = """
        SELECT COUNT(*) AS available_count
        FROM books
        WHERE is_available = TRUE;
    """
    result = pd.read_sql(query, con=engine)
    return int(result["available_count"].iloc[0])

def count_total_books():
    engine = db.get_engine()
    query = "SELECT COUNT(*) AS total_count FROM books;"
    result = pd.read_sql(query, con=engine)
    return int(result["total_count"].iloc[0])

# --------- LOANS -------------

"""def read_loans():
    engine = db.get_engine()
    return pd.read_sql("loans", con=engine)

def display_loans():
    # Combines loans + friends + books so the table shows names/titles
    # instead of just friend_id/isbn numbers
    friends = read_friends()
    books = read_books()
    loans = read_loans()

    display_columns = ["title", "name", "loan_date", "next_contact", "notes"]
    # return_date isn't shown -- since returning a book deletes the loan row
    # (see delete_loan), any row still visible here is, by definition, still out
    df = (
        loans
        .merge(friends, on="friend_id")
        .merge(books, on="isbn", suffixes=["", "_book"])
        [display_columns]
    )
    return df.pipe(prettify_df).sort_values(by="Loan date")"""

# --------- LOANS -------------

def read_loans():
    engine = db.get_engine()
    return pd.read_sql("loans", con=engine)

def display_loans():
    engine = db.get_engine()

    query = """
        SELECT 
            b.title, 
            f.name, 
            l.loan_date, 
            l.next_contact, 
            l.notes
        FROM loans l
        JOIN friends f ON l.friend_id = f.friend_id
        JOIN books b ON l.isbn = b.isbn
        ORDER BY l.loan_date;
    """
    
    df = pd.read_sql(query, con=engine)

    if df.empty:
        return pd.DataFrame(columns=["Title", "Name", "Loan date", "Next contact", "Notes"])

    # Format the dates as YYYY-MM-DD
    df["loan_date"] = pd.to_datetime(df["loan_date"]).dt.strftime("%Y-%m-%d")
    df["next_contact"] = pd.to_datetime(df["next_contact"]).dt.strftime("%Y-%m-%d")

    return prettify_df(df)


def read_detailed_loans():
    #Fetches loans with book titles and friend names directly via SQL.
    engine = db.get_engine()
    query = """
        SELECT 
            l.loan_id,l.isbn,
            l.notes,
            l.next_contact,
            l.last_contact,
            b.title,
            f.name
        FROM loans l
        JOIN friends f ON l.friend_id = f.friend_id
        JOIN books b ON l.isbn = b.isbn;
    """
    return pd.read_sql(query, con=engine)
def count_active_loans():
    engine = db.get_engine()
    loans = pd.read_sql("loans", con=engine)
    return len(loans)

def count_overdue_loans():
    engine = db.get_engine()
    query = """
        SELECT COUNT(*) AS overdue_count
        FROM loans
        WHERE next_contact < CURDATE();
    """
    result = pd.read_sql(query, con=engine)
    return int(result["overdue_count"].iloc[0])

def count_available_books():
    engine = db.get_engine()
    books = pd.read_sql("books", con=engine)
    loans = pd.read_sql("loans", con=engine)
    available = books[~books["isbn"].isin(loans["isbn"])]
    return len(available)

def count_total_books():
    engine = db.get_engine()
    books = pd.read_sql("books", con=engine)
    return len(books)

