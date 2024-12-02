LOAD DATA INFILE '/var/lib/mysql-files/books.csv' -- Load data in from a csv file to the "Book" relation
INTO TABLE Book
FIELDS TERMINATED BY ',' -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(ISBN, title, author, publication_year, genre, publisher);

LOAD DATA INFILE '/var/lib/mysql-files/magazines.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE Magazine 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(magazine_id,issue_number,title,publisher,publication_date,availability_status);

LOAD DATA INFILE '/var/lib/mysql-files/digitalmedia.csv' -- Load data in from a csv file to the "DigitalMedia" relation
INTO TABLE DigitalMedia 
FIELDS TERMINATED BY ',' -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
IGNORE 1 ROWS -- This line ignores the header and inserts just the data
(digital_media_id, title, author, publisher, publication_year, genre, availability_status);

LOAD DATA INFILE '/var/lib/mysql-files/clients.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE Client 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
(unique_id,name,contact_info,membership_type,account_status);

LOAD DATA INFILE '/var/lib/mysql-files/membership_type.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE MembershipType 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
(membership_type, borrowing_limit, fee_structure);

LOAD DATA INFILE '/var/lib/mysql-files/book_copy.csv' -- Load data in from a csv file to the "Magazine" relation
INTO TABLE Book_Copy 
FIELDS TERMINATED BY ','  -- Define the file headings being seperated by commas
LINES TERMINATED BY '\n' -- Define lines being seperated by new line characters
(copy_id, ISBN, status);

