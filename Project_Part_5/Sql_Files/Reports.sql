CREATE OR REPLACE VIEW MonthlySummaryReport AS
-- Total borrowed for Books
SELECT 
    c.membership_type AS client_type,
    'Book' AS item_type,
    COUNT(bb.item_id) AS total_borrowed,
    COALESCE(SUM(f.amount), 0) AS total_fees_collected,
    (SELECT b.title 
     FROM BookBorrowing bb_pop
     JOIN Book_Copy bc ON bb_pop.item_id = bc.copy_id
     JOIN Book b ON bc.ISBN = b.ISBN
     WHERE YEAR(bb_pop.borrow_date) = 2024 AND MONTH(bb_pop.borrow_date) = 11
     GROUP BY b.title
     ORDER BY COUNT(bb_pop.item_id) DESC
     LIMIT 1) AS most_popular_item
FROM 
    BookBorrowing bb
JOIN Client c ON bb.client_id = c.unique_id
LEFT JOIN Fee f ON f.client_id = bb.client_id 
                 AND f.item_type = 'book'
WHERE YEAR(bb.borrow_date) = 2024 AND MONTH(bb.borrow_date) = 11
GROUP BY client_type, item_type

UNION ALL

-- Total borrowed for Digital Media
SELECT 
    c.membership_type AS client_type,
    'Digital Media' AS item_type,
    COUNT(dmb.item_id) AS total_borrowed,
    COALESCE(SUM(f.amount), 0) AS total_fees_collected,
    (SELECT dm.title 
     FROM DigitalMediaBorrowing dmb_pop
     JOIN DigitalMedia dm ON dmb_pop.item_id = dm.digital_media_id
     WHERE YEAR(dmb_pop.borrow_date) = 2024 AND MONTH(dmb_pop.borrow_date) = 11
     GROUP BY dm.title
     ORDER BY COUNT(dmb_pop.item_id) DESC
     LIMIT 1) AS most_popular_item
FROM 
    DigitalMediaBorrowing dmb
JOIN Client c ON dmb.client_id = c.unique_id
LEFT JOIN Fee f ON f.client_id = dmb.client_id 
                 AND f.item_type = 'digital_media'
WHERE YEAR(dmb.borrow_date) = 2024 AND MONTH(dmb.borrow_date) = 11
GROUP BY client_type, item_type

UNION ALL

-- Total borrowed for Magazines
SELECT 
    c.membership_type AS client_type,
    'Magazine' AS item_type,
    COUNT(mb.item_id) AS total_borrowed,
    COALESCE(SUM(f.amount), 0) AS total_fees_collected,
    (SELECT m.title 
     FROM MagazineBorrowing mb_pop
     JOIN Magazine m ON mb_pop.item_id = m.magazine_id
     WHERE YEAR(mb_pop.borrow_date) = 2024 AND MONTH(mb_pop.borrow_date) = 11
     GROUP BY m.title
     ORDER BY COUNT(mb_pop.item_id) DESC
     LIMIT 1) AS most_popular_item
FROM 
    MagazineBorrowing mb
JOIN Client c ON mb.client_id = c.unique_id
LEFT JOIN Fee f ON f.client_id = mb.client_id 
                 AND f.item_type = 'magazine'
WHERE YEAR(mb.borrow_date) = 2024 AND MONTH(mb.borrow_date) = 11
GROUP BY client_type, item_type;




-- Client Activity Report
-- Produce an individual report for each client showing their borrowing history, outstanding fees, and any reserved items
CREATE OR REPLACE VIEW ClientActivityReport AS
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
CREATE OR REPLACE VIEW InventoryReport AS
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
CREATE OR REPLACE VIEW OverdueItemReport AS
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
LEFT JOIN Book b ON bb.item_id = b.ISBN
LEFT JOIN DigitalMedia dm ON dmb.item_id = dm.digital_media_id
LEFT JOIN Magazine m ON mb.item_id = m.magazine_id
WHERE 
    bb.item_id IS NOT NULL OR dmb.item_id IS NOT NULL OR mb.item_id IS NOT NULL;



-- Financial Report
-- Summarize the library’s revenue from fees, showing the breakdown by membership type and item category
CREATE OR REPLACE VIEW FinancialReport AS
SELECT 
    c.name AS client_name,
    c.membership_type,
    f.item_type,
    SUM(f.amount) AS total_revenue
FROM 
    Client c
LEFT JOIN Fee f ON c.unique_id = f.client_id
GROUP BY 
    c.name, c.membership_type, f.item_type
HAVING 
    SUM(f.amount) IS NOT NULL;
