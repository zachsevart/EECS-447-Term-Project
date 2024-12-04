LOAD DATA INFILE '../Uploads/membership_type.csv' -- Load data in from a csv file to the "membership_type" relation
INTO TABLE MembershipType 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(membership_type, borrowing_limit, fee_structure);

LOAD DATA INFILE '../Uploads/books.csv' -- Load data in from a csv file to the "Book" relation
INTO TABLE Book
FIELDS TERMINATED BY ',' -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(ISBN, title, author, publication_year, genre, publisher);

LOAD DATA INFILE '../Uploads/magazines.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE Magazine 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(magazine_id,issue_number,title,publisher,publication_date,availability_status);

LOAD DATA INFILE '../Uploads/digitalmedia.csv' -- Load data in from a csv file to the "DigitalMedia" relation
INTO TABLE DigitalMedia 
FIELDS TERMINATED BY ',' -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(digital_media_id, title, author, publisher, publication_year, genre, availability_status);

LOAD DATA INFILE '../Uploads/clients.csv' -- Load data in from a csv file to the "clients" relation
INTO TABLE Client 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(unique_id,name,contact_info,membership_type,account_status);

LOAD DATA INFILE '../Uploads/book_copy.csv' -- Load data in from a csv file to the "Book_copy" relation
INTO TABLE Book_Copy 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(copy_id, ISBN, status);

LOAD DATA INFILE '../Uploads/book_borrowing.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE BookBorrowing
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(client_id, item_id, borrow_date, due_date, @return_date)
SET return_date = NULLIF(@return_date, '');

LOAD DATA INFILE '../Uploads/magazine_borrowing.csv'
INTO TABLE MagazineBorrowing
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(client_id, item_id, borrow_date, due_date,@return_date)
SET return_date = NULLIF(@return_date, '');



LOAD DATA INFILE '/var/lib/mysql-files/magazine_borrowing.csv'
INTO TABLE MagazineBorrowing
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(client_id, item_id, borrow_date, due_date,@return_date)
SET return_date = NULLIF(@return_date, '');



LOAD DATA INFILE '../Uploads/digital_borrowing.csv'
INTO TABLE DigitalMediaBorrowing 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS
(client_id, item_id, borrow_date, due_date);
