-- Show Available Books
SELECT Book.ISBN, Book.title, Book.author
FROM Book
JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
WHERE Book_Copy.status = 'Available';


-- Show Available Digital Media
SELECT digital_media_id, title, author FROM digitalmedia WHERE availability_status = 'Available';


-- Show Available Magazines
SELECT magazine_id, issue_number, title, publisher FROM magazine WHERE availability_status = 'Available';


-- Find total number of items loaned out by each membership type
SELECT Client.membership_type, COUNT(Loaned.client_id) AS total_loaned
FROM Client LEFT JOIN
(SELECT client_id from bookborrowing
UNION all
SELECT client_id from digitalmediaborrowing
UNION all
SELECT client_id from magazineborrowing) AS Loaned
On Client.unique_id = Loaned.client_id
GROUP BY Client.membership_type;



-- List all overdue items/late fees



-- List Reserved but not loaned out items



-- List most popular items by number of loans



-- Generate a report of total fees collected within the last month, broken down by membership type.



-- Produce a list of clients who have exceeded their borrowing limits.



-- Determine the most frequently borrowed items by each client type



-- Find out which clients have never returned an item late
SELECT DISTINCT unique_id, Client.name
FROM Client
WHERE Client.unique_id NOT IN (
    SELECT DISTINCT client_id
    FROM Fee
    WHERE Fee.amount > 0
);
