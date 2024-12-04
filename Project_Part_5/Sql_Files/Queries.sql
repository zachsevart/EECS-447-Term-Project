-- Show Available Books
SELECT Book.ISBN, Book.title, Book.author
FROM Book
JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
WHERE Book_Copy.status = 'Available';

-- Show Available Digital Media
SELECT digital_media_id, title, author FROM DigitalMedia WHERE availability_status = 'Available';

-- Show Available Magazines
SELECT magazine_id, issue_number, title, publisher FROM Magazine WHERE availability_status = 'Available';

-- Find total Number of items loaned out by each membership type
SELECT Client.membership_type, COUNT(Loaned.client_id) AS total_loaned
FROM Client LEFT JOIN
(SELECT client_id from BookBorrowing 
UNION all
SELECT client_id from DigitalMediaBorrowing 
UNION all
SELECT client_id from MagazineBorrowing) AS Loaned
On Client.unique_id = Loaned.client_id
GROUP BY Client.membership_type;


-- List all overdue items/late fees
SELECT 
    Client.name AS client_name, 
    CASE 
        WHEN BookBorrowing.item_id IS NOT NULL THEN 'Book' 
        WHEN DigitalMediaBorrowing.item_id IS NOT NULL THEN 'Digital Media' 
        WHEN MagazineBorrowing.item_id IS NOT NULL THEN 'Magazine' 
    END AS item_type, 
    BookBorrowing.due_date, Fee.amount AS late_fee
FROM Fee
JOIN Client ON Fee.client_id = Client.unique_id
LEFT JOIN BookBorrowing ON Fee.client_id = BookBorrowing.client_id AND Fee.fee_date = BookBorrowing.due_date
LEFT JOIN DigitalMediaBorrowing ON Fee.client_id = DigitalMediaBorrowing.client_id AND Fee.fee_date = DigitalMediaBorrowing.due_date
LEFT JOIN MagazineBorrowing ON Fee.client_id = MagazineBorrowing.client_id AND Fee.fee_date = MagazineBorrowing.due_date
WHERE Fee.amount > 0;




-- List Reserved but not loaned out items (TODO: Add magazine and digital media to this as well)
SELECT 
    Book.ISBN AS item_id, 
    Book.title AS title, 
    Client.name AS client_name
FROM 
    Book_Copy
JOIN 
    Book ON Book_Copy.ISBN = Book.ISBN
LEFT JOIN 
    BookBorrowing ON Book_Copy.copy_id = BookBorrowing.item_id
LEFT JOIN 
    Client ON Client.unique_id = BookBorrowing.client_id
WHERE 
    Book_Copy.status = 'Reserved';




-- List most popular items by number of loans
SELECT Book.title, COUNT(BookBorrowing.item_id) AS times_borrowed
FROM Book
JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
JOIN BookBorrowing ON Book_Copy.copy_id = BookBorrowing.item_id
GROUP BY Book.ISBN
ORDER BY times_borrowed DESC
LIMIT 10;



-- Generate a report of total fees collected within the last month, broken down by membership type.
SELECT MembershipType.membership_type, SUM(Fee.amount) AS total_fees
FROM Fee
JOIN Client ON Fee.client_id = Client.unique_id
JOIN MembershipType ON Client.membership_type = MembershipType.membership_type
WHERE Fee.fee_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY MembershipType.membership_type;


-- Produce a list of clients who are at their borrowing limits.
SELECT 
    Client.name,
    COUNT(*) AS borrowed_items, 
    MembershipType.borrowing_limit
FROM 
    Client
JOIN 
    MembershipType ON Client.membership_type = MembershipType.membership_type
JOIN (
    SELECT client_id 
    FROM BookBorrowing 
    WHERE return_date IS NULL
    UNION ALL
    SELECT client_id 
    FROM DigitalMediaBorrowing 
    WHERE return_date IS NULL
    UNION ALL
    SELECT client_id 
    FROM MagazineBorrowing 
    WHERE return_date IS NULL
) AS Loans 
ON Client.unique_id = Loans.client_id
GROUP BY 
    Client.unique_id, MembershipType.borrowing_limit
HAVING 
    borrowed_items = MembershipType.borrowing_limit;




-- List the top 3 borrowed items for each membership type and item type
WITH RankedItems AS (
    SELECT
        Client.membership_type, 
        CASE 
            WHEN bb.item_id IS NOT NULL THEN 'Book'
            WHEN dmb.item_id IS NOT NULL THEN 'Digital Media'
            WHEN mb.item_id IS NOT NULL THEN 'Magazine'
        END AS item_type, 
        CASE 
            WHEN bb.item_id IS NOT NULL THEN b.title
            WHEN dmb.item_id IS NOT NULL THEN dm.title
            WHEN mb.item_id IS NOT NULL THEN m.title
        END AS item_title, 
        COUNT(*) AS borrow_count,
        ROW_NUMBER() OVER (
            PARTITION BY Client.membership_type, 
                         CASE 
                             WHEN bb.item_id IS NOT NULL THEN 'Book'
                             WHEN dmb.item_id IS NOT NULL THEN 'Digital Media'
                             WHEN mb.item_id IS NOT NULL THEN 'Magazine'
                         END
            ORDER BY COUNT(*) DESC
        ) AS `rank`
    FROM  
        Client
    LEFT JOIN BookBorrowing bb ON Client.unique_id = bb.client_id
    LEFT JOIN DigitalMediaBorrowing dmb ON Client.unique_id = dmb.client_id
    LEFT JOIN MagazineBorrowing mb ON Client.unique_id = mb.client_id
    LEFT JOIN Book_Copy bc ON bb.item_id = bc.copy_id
    LEFT JOIN Book b ON bc.ISBN = b.ISBN
    LEFT JOIN DigitalMedia dm ON dmb.item_id = dm.digital_media_id
    LEFT JOIN Magazine m ON mb.item_id = m.magazine_id
    GROUP BY 
        Client.membership_type, 
        item_type, 
        item_title
)
SELECT 
    membership_type, 
    item_type, 
    item_title, 
    borrow_count
FROM 
    RankedItems
WHERE 
    `rank` <= 3
ORDER BY 
    membership_type, 
    item_type, 
    borrow_count DESC;








-- Find out which clients have never returned an item late
SELECT DISTINCT unique_id, Client.name
FROM Client
WHERE Client.unique_id NOT IN (
    SELECT DISTINCT client_id
    FROM Fee
    WHERE Fee.amount > 0
);
