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
