CREATE DATABASE IF NOT EXISTS project; -- Create Database called project and set to use it
USE project;

CREATE TABLE IF NOT EXISTS Book ( -- Relation to store books, ISBN is primary key
    ISBN VARCHAR(20) PRIMARY KEY, 
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publication_year INT CHECK (publication_year > 0), 
    genre VARCHAR(100),
    publisher VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Book_Copy (
    copy_id SERIAL PRIMARY KEY,
    ISBN VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Available' CHECK (status IN ('Available', 'Borrowed', 'Reserved', 'Lost', 'Maintenance')),
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
);

CREATE TABLE IF NOT EXISTS DigitalMedia ( -- Relation to store digital media, Digital Media ID is the primary key
    digital_media_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    publication_year INT CHECK (publication_year > 0), 
    genre VARCHAR(100),
    availability_status VARCHAR(20) DEFAULT 'Available' CHECK (availability_status IN ('Available', 'Borrowed', 'Reserved'))
);

CREATE TABLE IF NOT EXISTS Magazine ( -- Relation to store magazines, magazine ID is the primary key
    magazine_id SERIAL PRIMARY KEY,
    issue_number INT NOT NULL CHECK(issue_number > 0),
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    publication_date DATE,
    availability_status VARCHAR(20) DEFAULT 'Available' CHECK (availability_status IN ('Available', 'Borrowed', 'Reserved'))
);

CREATE TABLE IF NOT EXISTS MembershipType (
    membership_type VARCHAR(100) PRIMARY KEY,
    borrowing_limit INT NOT NULL CHECK(borrowing_limit>0),
    fee_structure VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Client (
    unique_id SERIAL PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    membership_type VARCHAR(100) NOT NULL,
    account_status VARCHAR(20) NOT NULL CHECK (account_status IN ('Active', 'Suspended', 'Expired')),
    FOREIGN KEY (membership_type) REFERENCES MembershipType(membership_type)
);

CREATE TABLE IF NOT EXISTS BookBorrowing (
    client_id BIGINT UNSIGNED NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL, -- copy_id from Book_Copy
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    PRIMARY KEY (client_id, item_id, borrow_date),
    FOREIGN KEY (client_id) REFERENCES Client(unique_id),
    FOREIGN KEY (item_id) REFERENCES Book_Copy(copy_id)
);

CREATE TABLE IF NOT EXISTS DigitalMediaBorrowing (
    client_id BIGINT UNSIGNED NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL, -- digital_media_id
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    PRIMARY KEY (client_id, item_id, borrow_date),
    FOREIGN KEY (client_id) REFERENCES Client(unique_id),
    FOREIGN KEY (item_id) REFERENCES DigitalMedia(digital_media_id)
);

CREATE TABLE IF NOT EXISTS MagazineBorrowing (
    client_id BIGINT UNSIGNED NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL, -- magazine_id
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    PRIMARY KEY (client_id, item_id, borrow_date),
    FOREIGN KEY (client_id) REFERENCES Client(unique_id),
    FOREIGN KEY (item_id) REFERENCES Magazine(magazine_id)
);

CREATE TABLE IF NOT EXISTS Fee ( -- Relation to store fee information about checked out items, fee ID is the primary key
    fee_id SERIAL PRIMARY KEY, 
    client_id BIGINT UNSIGNED NOT NULL,
    item_type VARCHAR(50) NOT NULL, 
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    fee_date DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(unique_id),
    CONSTRAINT fee_item_type_chk CHECK (item_type IN ('book', 'digital_media', 'magazine')) 
);
