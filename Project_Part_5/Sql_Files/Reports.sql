-- Monthly Sumamry Report
-- Generate a report summarizing the total number of items loaned, total fees collected, and most popular items for the month.
-- Breakdown the statistics by client type and item category (Books, Digital Media, Magazines)
CREATE VIEW MonthlySummaryReport AS
SELECT 
    YEAR(borrow_date) AS year,
    MONTH(borrow_date) AS month,
    CASE 
        WHEN bb.item_id IS NOT NULL THEN 'Book'
        WHEN dmb.item_id IS NOT NULL THEN 'Digital Media'
        WHEN mb.item_id IS NOT NULL THEN 'Magazine'
    END AS item_type,
    COUNT(*) AS total_borrowed
FROM 
    BookBorrowing bb
LEFT JOIN DigitalMediaBorrowing dmb ON bb.client_id = dmb.client_id
LEFT JOIN MagazineBorrowing mb ON bb.client_id = mb.client_id
WHERE YEAR(borrow_date) = YEAR(CURRENT_DATE) 
  AND MONTH(borrow_date) = MONTH(CURRENT_DATE)
GROUP BY year, month, item_type;



-- Client Activity Report
-- Produce an individual report for each client showing their borrowing history, outstanding fees, and any reserved items
CREATE VIEW ClientActivityReport AS
SELECT 
    Client.name AS client_name,
    Client.membership_type,
    COUNT(bb.item_id) AS books_borrowed,
    COUNT(dmb.item_id) AS digital_media_borrowed,
    COUNT(mb.item_id) AS magazines_borrowed,
    SUM(CASE 
            WHEN bb.due_date < CURRENT_DATE AND bb.return_date IS NULL THEN 1
            ELSE 0
        END) AS overdue_books,
    SUM(CASE 
            WHEN dmb.due_date < CURRENT_DATE AND dmb.return_date IS NULL THEN 1
            ELSE 0
        END) AS overdue_digital_media,
    SUM(CASE 
            WHEN mb.due_date < CURRENT_DATE AND mb.return_date IS NULL THEN 1
            ELSE 0
        END) AS overdue_magazines
FROM 
    Client
LEFT JOIN BookBorrowing bb ON Client.unique_id = bb.client_id
LEFT JOIN DigitalMediaBorrowing dmb ON Client.unique_id = dmb.client_id
LEFT JOIN MagazineBorrowing mb ON Client.unique_id = mb.client_id
GROUP BY Client.unique_id;



-- Inventory Report
-- List all items, their current availability status, and their last borrowed date.
-- Highlight items that have not been borrowed in the past six months.
CREATE VIEW InventoryReport AS
SELECT 
    'Book' AS item_type,
    Book.ISBN AS item_id,
    Book.title AS item_title,
    COUNT(Book_Copy.copy_id) AS total_copies,
    SUM(CASE WHEN Book_Copy.status = 'Available' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN Book_Copy.status = 'Reserved' THEN 1 ELSE 0 END) AS reserved,
    SUM(CASE WHEN Book_Copy.status = 'Borrowed' THEN 1 ELSE 0 END) AS borrowed
FROM 
    Book
LEFT JOIN Book_Copy ON Book.ISBN = Book_Copy.ISBN
GROUP BY Book.ISBN
UNION ALL
SELECT 
    'Digital Media' AS item_type,
    DigitalMedia.digital_media_id AS item_id,
    DigitalMedia.title AS item_title,
    COUNT(*) AS total_copies,
    SUM(CASE WHEN DigitalMedia.availability_status = 'Available' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN DigitalMedia.availability_status = 'Reserved' THEN 1 ELSE 0 END) AS reserved,
    SUM(CASE WHEN DigitalMedia.availability_status = 'Borrowed' THEN 1 ELSE 0 END) AS borrowed
FROM 
    DigitalMedia
GROUP BY DigitalMedia.digital_media_id
UNION ALL
SELECT 
    'Magazine' AS item_type,
    Magazine.magazine_id AS item_id,
    Magazine.title AS item_title,
    COUNT(*) AS total_copies,
    SUM(CASE WHEN Magazine.availability_status = 'Available' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN Magazine.availability_status = 'Reserved' THEN 1 ELSE 0 END) AS reserved,
    SUM(CASE WHEN Magazine.availability_status = 'Borrowed' THEN 1 ELSE 0 END) AS borrowed
FROM 
    Magazine
GROUP BY Magazine.magazine_id;



-- Overdue Item Report
-- Generate a report listing all overdue items, the client responsible, and the calculated late fees.
CREATE VIEW OverdueItemReport AS
SELECT 
    Client.name AS client_name,
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
    CASE 
        WHEN bb.item_id IS NOT NULL THEN bb.due_date
        WHEN dmb.item_id IS NOT NULL THEN dmb.due_date
        WHEN mb.item_id IS NOT NULL THEN mb.due_date
    END AS due_date,
    DATEDIFF(CURRENT_DATE, CASE 
                            WHEN bb.item_id IS NOT NULL THEN bb.due_date
                            WHEN dmb.item_id IS NOT NULL THEN dmb.due_date
                            WHEN mb.item_id IS NOT NULL THEN mb.due_date
                        END) AS overdue_days
FROM 
    Client
LEFT JOIN BookBorrowing bb ON Client.unique_id = bb.client_id AND bb.return_date IS NULL AND bb.due_date < CURRENT_DATE
LEFT JOIN DigitalMediaBorrowing dmb ON Client.unique_id = dmb.client_id AND dmb.return_date IS NULL AND dmb.due_date < CURRENT_DATE
LEFT JOIN MagazineBorrowing mb ON Client.unique_id = mb.client_id AND mb.return_date IS NULL AND mb.due_date < CURRENT_DATE
LEFT JOIN Book b ON bb.item_id = b.copy_id
LEFT JOIN DigitalMedia dm ON dmb.item_id = dm.digital_media_id
LEFT JOIN Magazine m ON mb.item_id = m.magazine_id;



-- Financial Report
-- Summarize the library’s revenue from fees, showing the breakdown by membership type and item category
CREATE VIEW FinancialReport AS
SELECT 
    Client.name AS client_name,
    Client.membership_type,
    CASE 
        WHEN bb.item_id IS NOT NULL THEN 'Book'
        WHEN dmb.item_id IS NOT NULL THEN 'Digital Media'
        WHEN mb.item_id IS NOT NULL THEN 'Magazine'
    END AS item_type,
    CASE 
        WHEN bb.item_id IS NOT NULL THEN DATEDIFF(CURRENT_DATE, bb.due_date) * 0.50
        WHEN dmb.item_id IS NOT NULL THEN DATEDIFF(CURRENT_DATE, dmb.due_date) * 0.50
        WHEN mb.item_id IS NOT NULL THEN DATEDIFF(CURRENT_DATE, mb.due_date) * 0.50
    END AS late_fee
FROM 
    Client
LEFT JOIN BookBorrowing bb ON Client.unique_id = bb.client_id AND bb.return_date IS NULL AND bb.due_date < CURRENT_DATE
LEFT JOIN DigitalMediaBorrowing dmb ON Client.unique_id = dmb.client_id AND dmb.return_date IS NULL AND dmb.due_date < CURRENT_DATE
LEFT JOIN MagazineBorrowing mb ON Client.unique_id = mb.client_id AND mb.return_date IS NULL AND mb.due_date < CURRENT_DATE
WHERE 
    (bb.due_date < CURRENT_DATE AND bb.return_date IS NULL) OR
    (dmb.due_date < CURRENT_DATE AND dmb.return_date IS NULL) OR
    (mb.due_date < CURRENT_DATE AND mb.return_date IS NULL);
