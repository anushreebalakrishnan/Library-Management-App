CREATE SCHEMA IF NOT EXISTS sample_library1;
USE sample_library1;

-- books: back to tracking title + whether it's currently out on loan
CREATE TABLE IF NOT EXISTS books (
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    author VARCHAR(80),
    genre VARCHAR(20),
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);

-- friends: keeping v2's simpler shape, phone_number optional if you want it back later
CREATE TABLE IF NOT EXISTS friends (
    friend_id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(80),
    max_loans INT DEFAULT 2,
    notes TEXT
);

-- loans: surrogate key (loan_id) so the same friend can borrow the same
-- book again later -- the old composite key blocked that entirely.
-- return_date is back so you know when a loan actually closed.
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


USE sample_library1;
select * from books;
select * from friends;
select * from loans;
-- Books
INSERT INTO books (isbn, title, author, genre, is_available) VALUES
('9780143127550', 'The Goldfinch', 'Donna Tartt', 'Fiction', TRUE),
('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', TRUE),
('9780441172719', 'Dune', 'Frank Herbert', 'Sci-Fi', FALSE),
('9780307474278', 'The Da Vinci Code', 'Dan Brown', 'Thriller', TRUE),
('9780553380163', 'A Brief History of Time', 'Stephen Hawking', 'Science', FALSE),
('9780142437230', 'Meditations', 'Marcus Aurelius', 'Philosophy', TRUE);

-- Friends
INSERT INTO friends (`name`, max_loans, notes) VALUES
('Priya Nair', 2, 'Prefers thrillers, returns on time'),
('Tom Becker', 3, 'Bit slow with returns, send reminders'),
('Meera Iyer', 2, NULL),
('Jonas Weber', 1, 'Only borrows non-fiction');

-- Loans (mix of open and closed)
-- Dune -> Tom, still out
INSERT INTO loans (isbn, friend_id, loan_date, return_date, last_contact, next_contact, notes) VALUES
('9780441172719', 2, '2026-08-15', NULL, '2026-09-01', '2026-09-15', 'Reminded via text');

-- A Brief History of Time -> Jonas, still out
INSERT INTO loans (isbn, friend_id, loan_date, return_date, last_contact, next_contact, notes) VALUES
('9780553380163', 4, '2026-09-01', NULL, NULL, '2026-10-01', NULL);

-- The Da Vinci Code -> Priya, already returned (closed loan)
INSERT INTO loans (isbn, friend_id, loan_date, return_date, last_contact, next_contact, notes) VALUES
('9780307474278', 1, '2026-07-01', '2026-07-20', NULL, NULL, 'Returned in great condition');

-- To Kill a Mockingbird -> Meera, already returned (closed loan)
INSERT INTO loans (isbn, friend_id, loan_date, return_date, last_contact, next_contact, notes) VALUES
('9780061120084', 3, '2026-06-10', '2026-06-25', NULL, NULL, NULL);