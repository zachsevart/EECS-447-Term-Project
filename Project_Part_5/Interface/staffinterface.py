def staffInterface(choice):
    if choice == 0:  # Check out items
        print('Select the # of what to check out\
              \n\t1) Books\
              \n\t2) Magazines\
              \n\t3) Digital Media')
        item_choice = (int(input('Choose an option: ')) - 1)
        if 3 > item_choice >= 0:
            selection = {0: 'Book_Copy', 1: 'Magazine', 2: 'DigitalMedia'}
            if selection[item_choice] == 'Book_Copy':
                print('Enter the client ID:')
                client_id = input('Client ID: ').strip()
                print('Enter the ISBN of the book to check out:')
                isbn = input('ISBN: ').strip()
                print('Enter the Borrow Date of the book to check out:')
                borrow_date = input('Borrow Date: ').strip()
               
                

                
                # Check membership type and borrowing limit
                sql_limit_check = """
                SELECT COUNT(*) 
                FROM BookBorrowing 
                WHERE client_id = %s AND return_date IS NULL
                """
                mycursor.execute(sql_limit_check, (client_id,))
                borrowed_count = mycursor.fetchone()[0]

                # Assuming borrowing limit based on membership type
                sql_membership = "SELECT membership_type FROM Client WHERE unique_id = %s"
                mycursor.execute(sql_membership, (client_id,))
                membership_type = mycursor.fetchone()[0]

                limits = {'Senior': 5, 'Regular': 3, 'Student': 2}
                if borrowed_count >= limits[membership_type]:
                    print(f'Borrowing limit reached for membership type: {membership_type}')
                    return

                # Reserve book for client
                sql = "SELECT * FROM Book_Copy WHERE ISBN = %s AND status='Available' LIMIT 1"
                mycursor.execute(sql, (isbn,))
                book_copy = mycursor.fetchone()
                if book_copy:
                    item_id = book_copy[0]
                    query_update = """
                    INSERT INTO BookBorrowing (client_id, item_id, borrow_date, due_date, return_date) 
                    VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 50 DAY), NULL)
                    """
                    mycursor.execute(query_update, (client_id, item_id))  # Pass only placeholders needed
                    mycursor.execute("UPDATE Book_Copy SET status = 'Borrowed' WHERE copy_id = %s", (item_id,))
                    mydb.commit()

                    print('Book checked out successfully!')
                else:
                    print('No available copies of the book.')

            elif selection[item_choice] == 'Magazine':
                print('Enter the client ID:')
                client_id = input('Client ID: ').strip()
                print('Enter the Magazine ID to check out:')
                magazine_id = input('Magazine ID: ').strip()

                # Check if the magazine is available
                sql = "SELECT * FROM Magazine WHERE magazine_id = %s AND availability_status='Available'"
                mycursor.execute(sql, (magazine_id,))
                magazine = mycursor.fetchone()
                if magazine:
                    query_update = """
                    INSERT INTO MagazineBorrowing (client_id, item_id, borrow_date, due_date, return_date)
                    VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 50 DAY), NULL)
                    """
                    mycursor.execute(query_update, (client_id, magazine_id))
                    mycursor.execute("UPDATE Magazine SET availability_status = 'Borrowed' WHERE magazine_id = %s", (magazine_id,))
                    mydb.commit()
                    print('Magazine checked out successfully!')
                else:
                    print('No available copies of the magazine.')

            elif selection[item_choice] == 'DigitalMedia':
                print('Enter the client ID:')
                client_id = input('Client ID: ').strip()
                print('Enter the ID of the Digital Media to check out:')
                digital_media_id = input('Digital Media ID: ').strip()

                # Check if the digital media is available
                sql = "SELECT * FROM DigitalMedia WHERE digital_media_id = %s AND availability_status='Available'"
                mycursor.execute(sql, (digital_media_id,))
                digital_media = mycursor.fetchone()
                if digital_media:
                    query_update = """
                    INSERT INTO DigitalMediaBorrowing (client_id, item_id, borrow_date, due_date, return_date)
                    VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 50 DAY), NULL)
                    """
                    mycursor.execute(query_update, (client_id, digital_media_id))
                    mycursor.execute("UPDATE DigitalMedia SET availability_status = 'Borrowed' WHERE digital_media_id = %s", (digital_media_id,))
                    mydb.commit()
                    print('Digital Media checked out successfully!')
                else:
                    print('No available copies of the digital media.')

    elif choice == 1: # Process Returns (Change status, set return date, create fee if needed, edit borrowing table)
        print("Enter the book copy ID being returned:")
        copy_id = input().strip()
        print("Enter the return date (YYYY-MM-DD):")
        return_date = input().strip()
                                            
        # Fetch due date, client ID, and item type
        mycursor.execute("""
            SELECT due_date, client_id, 'Book' AS item_type
            FROM BookBorrowing
            WHERE copy_id = %s AND return_date IS NULL
        """, (copy_id,))
        result = mycursor.fetchone()

        if not result:
            print("No active borrowing record found for this copy.")
            return

        due_date, client_id, item_type = result

        # Update return date and item status
        mycursor.execute("""
            UPDATE Borrowing
            SET return_date = %s
            WHERE copy_id = %s AND return_date IS NULL
        """, (return_date, copy_id))
        mycursor.execute("UPDATE Book_copy SET status = 'Available' WHERE copy_id = %s", (copy_id,))

        # Check for overdue and calculate fee
        query = "SELECT DATEDIFF(%s, %s)"  # Calculate days overdue
        mycursor.execute(query, (return_date, due_date))
        overdue_days = mycursor.fetchone()[0]

        if overdue_days > 0:
            fee_amount = overdue_days * 0.5  # Example fee: $0.50 per day
            mycursor.execute("""
                INSERT INTO Fees (client_id, item_type, amount, fee_date)
                VALUES (%s, %s, %s, %s)
            """, (client_id, item_type, fee_amount, return_date))
            print(f"Overdue fee of ${fee_amount:.2f} has been added for client {client_id}.")

        mydb.commit()
        print(f"Book copy {copy_id} returned successfully.")



    elif choice == 2:  # Add New Items
        print('Select the # of what to add\
              \n\t1) Books\
              \n\t2) Magazines\
              \n\t3) Digital Media')
        item_choice = (int(input('Choose an option: ')) - 1)
        selection = {0: 'Book_Copy', 1: 'Magazine', 2: 'DigitalMedia'}
        if 3 > item_choice >= 0:
            table = selection[item_choice]
            print(f'Enter details for the new {table}:')
            if table == 'Book_Copy':
                isbn = input('Enter ISBN: ').strip()
                title = input('Enter Title: ').strip()
                author = input('Enter Author: ').strip()
                publication_year = input('Enter Publication Year: ').strip()
                genre = input('Enter Genre: ').strip()
                publisher = input('Enter Publisher: ').strip()
                sql = "INSERT INTO Book (ISBN, title, author, publication_year, genre, publisher) VALUES (%s, %s, %s, %s, %s, %s)"
                mycursor.execute(sql, (isbn, title, author, publication_year, genre, publisher))
            elif table == 'Magazine':
                mag_id = input('Enter Magazine ID: ').strip()
                title = input('Enter Title: ').strip()
                sql = "INSERT INTO Magazine (magazine_id, title, availability_status) VALUES (%s, %s, 'Available')"
                mycursor.execute(sql, (mag_id, title))
            elif table == 'DigitalMedia':
                media_id = input('Enter Digital Media ID: ').strip()
                title = input('Enter Title: ').strip()
                sql = "INSERT INTO DigitalMedia (digital_media_id, title, availability_status) VALUES (%s, %s, 'Available')"
                mycursor.execute(sql, (media_id, title))
            mydb.commit()
            print(f'New {table} added successfully!')

    elif choice == 3:  # Manage Client Accounts
        print('Enter the Client ID to update:')
        client_id = input('Client ID: ').strip()
        print('Select the # of what to change\
              \n\t1) Name\
              \n\t2) Membership\
              \n\t3) Account Status')
        item_choice = (int(input('Choose an option: ')) - 1)
        selection = {0: 'Name', 1: 'Membership', 2: 'Account Status'}
        if 3 > item_choice >= 0:
            table = selection[item_choice]
        if table == 'Account Status':
            print('Enter the new account status (Active/Suspended/Expired):')
            status = input('Status: ').strip()
            sql = "UPDATE Client SET account_status = %s WHERE unique_id = %s"
            mycursor.execute(sql, (status, client_id))
            mydb.commit()
            print('Client account status updated successfully!')
        elif table == 'Membership':
            print('Enter the new membership (Student/Regular/Senior):')
            status = input('Status: ').strip()
            sql = "UPDATE Client SET membership_type = %s WHERE unique_id = %s"
            mycursor.execute(sql, (status, client_id))
            mydb.commit()
            print('Membership Type updated!')
        elif table == 'Name':
            print('Enter the new name (First and Last):')
            name = input('Name: ').strip()
            sql = "UPDATE Client SET name = %s WHERE unique_id = %s"
            mycursor.execute(sql, (name, client_id))
            mydb.commit()
            print('Name updated!')
