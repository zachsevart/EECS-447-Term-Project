-- Show Available Books
SELECT Book.ISBN, Book.title, Book.author
FROM Book
JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
WHERE Book_Copy.status = 'Available';


-- Show Available Digital Media
SELECT digital_media_id, title, author FROM digitalmedia WHERE availability_status = 'Available';


-- Show Available Magazines
SELECT magazine_id, issue_number, title, publisher FROM magazine WHERE availability_status = 'Available';


-- Find total Number of items loaned out by each membership type



-- List all overdue items/late fees



-- List Reserved but not loaned out items



-- List most popular items by number of loans



-- Generate a report of total fees collected within the last month, broken down by membership type.



-- Produce a list of clients who have exceeded their borrowing limits.



-- Determine the most frequently borrowed items by each client type



-- Find out which clients have never returned an item late


