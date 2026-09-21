import streamlit as st
import pandas as pd
import datetime
import db
from sqlalchemy import create_engine
from create import *
from delete import *
from read import *
from update import *
from pathlib import Path

APP_DIR = Path(__file__).parent
IMAGE_PATH = APP_DIR / "booksimage.jpg"
#from login import login(for login screen)

# ---------- SIDEBAR IMAGE (always visible, even on login screen) -------------------------------------------------------
with st.sidebar:
    nav_slot = st.container(key="sidebar_nav")
    st.image(str(IMAGE_PATH))

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            padding: 0rem !important;
        }
        [data-testid="stSidebarUserContent"] {
            padding: 0rem !important;
            display: flex !important;
            flex-direction: column !important;
            height: 100vh !important;
        }
        .st-key-sidebar_nav {
            padding: 1.5rem 1rem 1rem 1rem !important;
        }
        [data-testid="stImage"] {
            margin-top: auto !important;
        }
        [data-testid="stImage"] img {
            margin-top: 10vh !important;
            width: 100% !important;
            object-fit: cover !important;
            object-position: center center !important;
            border-radius: 0px !important;
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to Liana's Library")
st.subheader("Where books go on little adventures — and come home again", divider="gray")

unused_login_code = """
#Login Screen
if st.session_state.get("login") != "loggedin":
    login()
    st.stop()

db.set_engine(st.session_state["engine"])
db.initialize_database(st.session_state["engine"])

"""
# ---------- DATABASE CONNECTION (automatic, no login screen) ------------------------------------
connection_string = (
    f"mysql+pymysql://{st.secrets['db_user']}:{st.secrets['db_password']}"
    f"@{st.secrets['db_host']}:{st.secrets['db_port']}/{st.secrets['db_schema']}"
)
engine = create_engine(connection_string)
db.set_engine(engine)
db.initialize_database(engine)
# ---------- SIDEBAR NAV (what do u want to manage) --------------------------------------------------
with nav_slot:
    section = st.radio("What do you want to manage?", options=["Friends", "Books", "Loans"],index=None)

if section is not None:

    # ---------- QUICK STATS ------------------------------------------------------------------------
    available = count_available_books()
    total = count_total_books()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Books Available", available)
    with col2:
        st.metric("Total Books", total)


# ======================================================================================================
                        # FRIENDS
# ======================================================================================================
    if section == "Friends":
        action = st.radio("Selection:", options=["View Friends",
                                        "Add Friend",
                                        "Edit Friend",
                                        "Remove Friend"], horizontal=True)

        if action == "View Friends":
            friends_df = display_friends()
            st.dataframe(friends_df, hide_index=True)

        if action == "Add Friend":
            with st.form("add_friend_form", clear_on_submit=True):
                friend_name = st.text_input("Name:")
                max_loans = st.number_input("Insert Max Loans: ", value=2, min_value=1, max_value=5, placeholder="Type a number...")
                notes = st.text_area('Notes: ')
                submitted = st.form_submit_button("Submit")

            if submitted:
                result = create_friend(friend_name, max_loans, notes)
                if result.startswith("Can't"):
                    st.warning(result)
                else:
                    st.success(result)
                    st.balloons()
                    st.rerun()         

        if action == "Edit Friend":
            friends_df = read_friends()

            friend_name = st.selectbox("Select a friend...", friends_df['name'])
            friend = friends_df[friends_df['name'] == friend_name].iloc[0]

            field_choice = st.selectbox("Choose a field", options=["Name", "Max loans", "Notes"])

            if field_choice == "Name":
                new_val = st.text_input("New Name:", value=friend['name'])
            if field_choice == "Max loans":
                new_val = st.number_input("New Amount:", value=int(friend["max_loans"]), min_value=1, max_value=5)
            if field_choice == "Notes":
                new_val = st.text_area("New note:", value=friend['notes'])

            if st.button("Submit"):
                st.success(update_friend(friend, field_choice, new_val))
                st.rerun()

        if action == "Remove Friend":
            friends_df = read_friends()

            friend_name = st.selectbox("Select a friend to delete:", friends_df["name"])
            friend = friends_df[friends_df['name'] == friend_name].iloc[0]

            if st.button("Submit"):
                st.session_state["confirm_delete_friend"] = friend_name

            if st.session_state.get("confirm_delete_friend") == friend_name:
                st.warning(f"Are you sure you want to remove '{friend_name}'? This can't be undone.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, remove them"):
                        success, message = delete_friend(friend)
                        if success:
                            st.success(message)
                            del st.session_state["confirm_delete_friend"]
                            st.rerun()
                        else:
                            st.warning(message)
                with col2:
                    if st.button("Cancel"):
                        del st.session_state["confirm_delete_friend"]
                        st.rerun()

# ===========================================================================================================================
                                        # BOOKS
# ==========================================================================================================================
    if section == "Books":
        action = st.radio("Selection:", options=["View Books",
                                        "Add Book",
                                        "Edit Book",
                                        "Remove Book"], horizontal=True)

        if action == "View Books":
            only_available = st.checkbox("Only show available books")
            books_df = display_books(only_available)
            st.dataframe(books_df, hide_index=True)
            st.write(f"📚 {count_available_books()} books currently available")


        if action == "Add Book":
            with st.form("add_book_form", clear_on_submit=True):
                title = st.text_input("Title:")
                isbn = st.text_input("ISBN:")
                author = st.text_input("Author:")
                genre = st.text_input("Genre:")
                submitted = st.form_submit_button("Submit")

            if submitted:
                result = create_book(title, isbn, author, genre)
                if result.startswith("Can't"):
                    st.warning(result)
                else:
                    st.success(result)
                    st.balloons()
                    st.rerun()

        if action == "Edit Book":
            books_df = read_books()

            book_title = st.selectbox("Select a book...", books_df['title'])
            book = books_df[books_df['title'] == book_title].iloc[0]

            field_choice = st.selectbox("Choose a field", options=["Title", "Author", "Genre", "ISBN"])

            if field_choice == "Title":
                new_val = st.text_input("New Title:", value=book['title'])
            if field_choice == "Author":
                new_val = st.text_input("New Author:", value=book['author'])
            if field_choice == "Genre":
                new_val = st.text_input("New Genre:", value=book['genre'])
            if field_choice == "ISBN":
                new_val = st.text_input("New ISBN:", value=book['isbn'])

            if st.button("Submit"):
                st.success(update_book(book, field_choice, new_val))
                st.rerun()

        if action == "Remove Book":
            books_df = read_books()

            book_title = st.selectbox("Select a book to delete:", books_df["title"])
            book = books_df[books_df['title'] == book_title].iloc[0]

            if st.button("Submit"):
                st.session_state["confirm_delete_book"] = book_title

            if st.session_state.get("confirm_delete_book") == book_title:
                st.warning(f"Are you sure you want to remove '{book_title}'? This can't be undone.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, remove it"):
                        result = delete_book(book)
                        if result.startswith("Can't"):
                            st.warning(result)
                        else:
                            st.success(result)
                            del st.session_state["confirm_delete_book"]
                            st.rerun()
                with col2:
                    if st.button("Cancel"):
                        del st.session_state["confirm_delete_book"]
                        st.rerun()

    # ================================================================================================================
                                                            # LOANS
    # ================================================================================================================
    if section == "Loans":
        action = st.radio("Selection:", options=["View loans",
                                        "Add loan",
                                        "Edit loan",
                                        "Return a book"], horizontal=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Loans", count_active_loans())
        with col2:
            st.metric("Overdue", count_overdue_loans())

        if action == "View loans":
            loans_df = display_loans()
            st.dataframe(loans_df, hide_index=True)

        if action == "Add loan":
            friends_df = read_friends()
            books_df = read_books(available_only=True)

            friend_name = st.selectbox("Who is borrowing?", friends_df['name'])
            friend = friends_df[friends_df['name'] == friend_name].iloc[0]

            book_title = st.selectbox("Which book?", books_df['title'])
            book = books_df[books_df['title'] == book_title].iloc[0]

            loan_date = st.date_input("Loan date")

            suggested_return = loan_date + datetime.timedelta(days=30)
            st.caption(f"📅 Expected return date: {suggested_return.strftime('%Y-%m-%d')} (30 days from loan date)")

            next_contact = st.date_input("Next check-in date", value=suggested_return)
            notes = st.text_area("Notes:")
            if st.button("Submit"):
                result = create_loan(friend, book, loan_date, next_contact, notes)
                if "Can't lend" in result or "maximum limit" in result:
                    st.warning(result)
                else:
                    st.success(result)
                    st.balloons()
                    st.rerun()

        if action == "Edit loan":
            loans_df = read_detailed_loans()

            if loans_df.empty:
                st.info("No active loans to update.")
            else:
                loans_df["label"] = loans_df["title"] + " - " + loans_df["name"]

                loan_label = st.selectbox("Select a loan...", loans_df["label"])
                loan = loans_df[loans_df["label"] == loan_label].iloc[0]

                field_choice = st.selectbox("Choose a field", options=["Notes", "Next contact", "Last contact"])

                if field_choice == "Notes":
                    current_note = loan["notes"] or ""
                    new_val = st.text_area("New note:", value=current_note)

                if field_choice == "Next contact":
                    new_val = st.date_input("New next contact date:", value=loan["next_contact"])

                if field_choice == "Last contact":
                    new_val = st.date_input("New last contact date:", value=loan["last_contact"])

                if st.button("Submit"):
                    st.success(update_loan(loan, field_choice, new_val))
                    st.rerun()

        if action == "Return a book":
            loans_df = read_detailed_loans()

            if loans_df.empty:
                st.info("No active loans to return.")
            else:
                loans_df["label"] = loans_df["title"] + " - " + loans_df["name"]

                loan_label = st.selectbox("Which loan is being returned?", loans_df["label"])
                loan = loans_df[loans_df["label"] == loan_label].iloc[0]

                if st.button("Submit"):
                    st.success(delete_loan(loan))
                    st.rerun()
