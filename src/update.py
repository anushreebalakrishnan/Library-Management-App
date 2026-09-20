from sqlalchemy import text
import db

# --------- SHARED HELPER ----------------
def get_column_name(field_choice):
    # Translates the friendly dropdown label the user sees ("Max loans")
    # into the real column name in the database ("max_loans")
    mapping = {
        "Name": "name",
        "Max loans": "max_loans",
        "Notes": "notes",
        "Title": "title",
        "Author": "author",
        "Genre": "genre",
        "ISBN": "isbn",
        "Next contact": "next_contact",
        "Last contact": "last_contact",
    }
    return mapping.get(field_choice)

# --------- FRIENDS ----------------
def update_friend(friend, field_choice, new_data):
    engine = db.get_engine()
    column = get_column_name(field_choice)

    update_query = text(f"""
        UPDATE friends
        SET {column} = :new_data
        WHERE friend_id = :friend_id
    """)

    with engine.begin() as connection:
        connection.execute(
            update_query,
            {"new_data": new_data, "friend_id": friend["friend_id"]}
        )
    return f"{field_choice} updated."

# --------- BOOKS ----------------
def update_book(book, field_choice, new_data):
    engine = db.get_engine()
    column = get_column_name(field_choice)

    update_query = text(f"""
        UPDATE books
        SET {column} = :new_data
        WHERE isbn = :isbn
    """)

    with engine.begin() as connection:
        connection.execute(
            update_query,
            {"new_data": new_data, "isbn": book["isbn"]}
        )
    return f"{field_choice} updated."

# --------- LOANS ----------------
def update_loan(loan, field_choice, new_data):
    engine = db.get_engine()
    column = get_column_name(field_choice)

    # loan_id (not isbn/friend_id) uniquely identifies ONE loan row --
    # this matters because the same friend can borrow the same book more than once
    update_query = text(f"""
        UPDATE loans
        SET {column} = :new_data
        WHERE loan_id = :loan_id
    """)

    with engine.begin() as connection:
        connection.execute(
            update_query,
            {"new_data": new_data, "loan_id": loan["loan_id"]}
        )
    return f"{field_choice} updated."

