SELECT Book.ISBN, Book.title, Book.author
FROM Book
JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
WHERE Book_Copy.status = 'Available';
