# db.py
# Holds ONE shared database connection ("engine") that every other file can use,
# and sets up the database tables automatically if they don't exist yet.

from sqlalchemy import text

engine = None

def set_engine(e):
    # Called once, when the app starts up, to store the connection.
    global engine
    engine = e

def get_engine():
    # Called by every create/read/update/delete function to grab that same connection.
    return engine

def initialize_database(e):
    with e.begin() as connection:
        # Books table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS books (
                isbn VARCHAR(13) PRIMARY KEY,
                title VARCHAR(80) NOT NULL,
                author VARCHAR(80),
                genre VARCHAR(20),
                is_available BOOLEAN NOT NULL DEFAULT TRUE
            );
        """))

        # Friends table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS friends (
                friend_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(80),
                max_loans INT DEFAULT 2,
                notes TEXT
            );
        """))

        # Loans table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INT AUTO_INCREMENT PRIMARY KEY,
                isbn VARCHAR(13) NOT NULL,
                friend_id INT NOT NULL,
                loan_date DATE NOT NULL DEFAULT (CURRENT_DATE()),
                return_date DATE,
                last_contact DATE,
                next_contact DATE DEFAULT (DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)),
                notes TEXT,
                FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (friend_id) REFERENCES friends(friend_id) ON DELETE CASCADE
            );
        """))

        # Only seed sample data if the books table is currently empty
        result = connection.execute(text("SELECT COUNT(*) FROM books")).scalar()
        if result == 0:
            connection.execute(text("""
                INSERT INTO books (isbn, title, author, genre, is_available) VALUES
                ('9780143127550', 'The Goldfinch', 'Donna Tartt', 'Fiction', TRUE),
                ('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', TRUE),
                ('9780441172719', 'Dune', 'Frank Herbert', 'Sci-Fi', TRUE),
                ('9780307474278', 'The Da Vinci Code', 'Dan Brown', 'Thriller', TRUE),
                ('9780553380163', 'A Brief History of Time', 'Stephen Hawking', 'Science', TRUE),
                ('9780142437230', 'Meditations', 'Marcus Aurelius', 'Philosophy', TRUE);
            """))
            connection.execute(text("""
                INSERT INTO friends (name, max_loans, notes) VALUES
                ('Priya Nair', 2, 'Prefers thrillers, returns on time'),
                ('Tom Becker', 3, 'Bit slow with returns, send reminders'),
                ('Meera Iyer', 2, NULL),
                ('Jonas Weber', 1, 'Only borrows non-fiction');
            """))