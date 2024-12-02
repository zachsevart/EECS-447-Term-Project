LOAD DATA INFILE '../Uploads/books.csv'
INTO TABLE Book 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ISBN, title, author, publication_year, genre, publisher);

LOAD DATA INFILE '../Uploads/magazines.csv'
INTO TABLE Magazine 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(magazine_id,issue_number,title,publisher,publication_date,availability_status);

LOAD DATA INFILE '../Uploads/digitalmedia.csv' 
INTO TABLE DigitalMedia 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(digital_media_id, title, author, publisher, publication_year, genre, availability_status);
