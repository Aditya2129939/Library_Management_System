CREATE DATABASE library_management;
USE library_management;

CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    author VARCHAR(100),
    isbn VARCHAR(20)
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    role ENUM('admin', 'user') DEFAULT 'user'
);

CREATE TABLE issued_books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    user_id INT,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO books (title, author, isbn) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565'),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084'),
('1984', 'George Orwell', '9780451524935');

UPDATE users
SET password = 'admin'
WHERE username = 'admin' AND password = 'admin123';

UPDATE users
SET password = 'user'
WHERE username = 'user1' AND password = 'user123';

select * from books;


