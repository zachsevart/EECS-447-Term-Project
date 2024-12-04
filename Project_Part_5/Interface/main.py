import mysql.connector # pip install mysql-connector-python
import os

'''
For more information on MySQL Connection to python: https://www.w3schools.com/python/python_mysql_getstarted.asp
'''


# Get directory of parent for use with proper execution
parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Connect to MySQL db
mydb = mysql.connector.connect(
  host="localhost",
  user="root", # Fill out MySQL username here (default: root) TODO: store in a config file that is in .gitignore
  password="8420", # Fill out your MySQL password here
  database='project'
)
# Create cursor to interact with DB
mycursor = mydb.cursor()

# Executes a query for a list of options
def executeQuery(query):
    try:
        mycursor.execute(query)
        return mycursor.fetchall()
    except Exception as e:
        print(f"Error occured: {e}")
        return []

# Load in the queries.sql file
def loadQuery():
    with open(os.path.join(parentDir, 'Sql_Files', 'Queries.sql'), "r") as file:
        queries = file.read()
    # Split the file into individual queries based on semicolons
    queriesList = queries.split(";")

    # Clean up lines
    return [q.strip() for q in queriesList if q.strip()]


# Staff interface for checking out items, processing return, adding new items, and managing client accounts
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
                print('Enter the Borrow Date of the book to check out (YYYY-MM-DD):')
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
            WHERE item_id = %s AND return_date IS NULL
        """, (copy_id,))
        result = mycursor.fetchone()

        if not result:
            print("No active borrowing record found for this copy.")
            return

        due_date, client_id, item_type = result

        # Update return date and item status
        mycursor.execute("""
            UPDATE BookBorrowing
            SET return_date = %s
            WHERE item_id = %s AND return_date IS NULL
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

# Interface for client interaction allows for searching/reserving/check loan status/viewing fees
def clientInterface(choice):
    if choice == 0: # Search Catalog
        print('Select the # to search for?:\
              \n\t1) Books\
              \n\t2) Magazines\
              \n\t3) Digital Media')
        choice = (int(input('Choose an option: '))-1)
        if 3 > choice >= 0:
            selection = {0:'Book', 1:'Magazine', 2:'DigitalMedia'}
            mycursor.execute(f'SELECT * FROM {selection[choice]}')
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
    elif choice == 1: # Reserve itemsa
        print('Select the # of what to reserve\
              \n\t1) Books\
              \n\t2) Magazines\
              \n\t3) Digital Media')
        choice = (int(input('Choose an option: '))-1)
        if 3 > choice >= 0:
            selection = {0:'Book', 1:'Magazine', 2:'DigitalMedia'}
            if selection[choice] == 'Book':
                print('Enter the ISBN of what book to reserve (ex:978-9916732243)')
                isbn = input('ISBN: ').strip()
                sql = "SELECT * FROM Book_copy WHERE Book_copy.ISBN = %s AND status='Available' LIMIT 1"
                mycursor.execute(sql, (isbn,))
                myresult = mycursor.fetchone()
                if myresult:
                    print(f'Selected Book: {myresult[1]}')
                    query_update = "UPDATE Book_Copy SET status = 'Reserved' WHERE copy_id = %s"
                    mycursor.execute(query_update, (myresult[0],))  # Assuming copy_id is the first column
                    mydb.commit()  # Commit the changes to the database
                else:
                    print('No available copies')
            elif selection[choice] == 'Magazine':
                print('Enter the magazine # of what to reserve: ')
                idNum = input('ID #: ').strip()
                sql = "SELECT * FROM Magazine WHERE magazine_id = %s AND availability_status='Available'"
                mycursor.execute(sql, (idNum,))
                myresult = mycursor.fetchone()
                if myresult:
                    for x in myresult:
                        print(f'Selected Magazine: {x}')
                    query_update = "UPDATE Magazine SET status = 'Reserved' WHERE copy_id = %s"
                    mycursor.execute(query_update, (myresult[0],))  # Assuming copy_id is the first column
                    mydb.commit()  # Commit the changes to the database
                else:
                    print('No available copies')
            else:
                print('Enter the id of the digital media you want to reserve')
                idNum = input('ID #: ').strip()
                sql = "SELECT * FROM DigitalMedia WHERE digital_media_id = %s AND availability_status='Available'"
                mycursor.execute(sql, (idNum,))
                myresult = mycursor.fetchone()
                if myresult:
                    for x in myresult:
                        print(f'Selected Digital Media: {x}')
                    query_update = "UPDATE DigitalMedia SET status = 'Reserved' WHERE copy_id = %s"
                    mycursor.execute(query_update, (myresult[0],))  # Assuming copy_id is the first column
                    mydb.commit()  # Commit the changes to the database
                else:
                    print('No available copies')
    elif choice == 2: # Check loan status
        print('Enter client ID:')
        idNum = input().strip()
        sql = "SELECT * FROM Client WHERE unique_id = %s"
        mycursor.execute(sql, (idNum,))
        myresult = mycursor.fetchone()
        if not myresult:
            print('Account not found')
        elif myresult[4] == 'Active':
            print(f'Welcome {myresult[1]}!')
            loanQuery = """
            SELECT item_id, item_type
            FROM (
                SELECT item_id, 'Book' AS item_type
                FROM BookBorrowing
                WHERE return_date IS NULL AND client_id = %s
                UNION ALL
                SELECT item_id, 'Digital Media' AS item_type
                FROM DigitalMediaBorrowing
                WHERE return_date IS NULL AND client_id = %s
                UNION ALL
                SELECT item_id, 'Magazine' AS item_type
                FROM MagazineBorrowing
                WHERE return_date IS NULL AND client_id = %s
            ) AS BorrowedItems;
            """
            mycursor.execute(loanQuery, (idNum,idNum,idNum))
            loans = mycursor.fetchall()
            if loans:
                print('Items borrowed:')
                for loan in loans:
                    print(f'\t{loan[1]}: Item ID: {loan[0]}')
            else:
                print('No borrowed items')
        else:
            print(f'Client Account not Active, Account: {myresult[1:3]}')
    elif choice == 3: # View outstanding fees
        print('Enter client ID:')
        idNum = input().strip()
        sql = "SELECT * FROM Client WHERE unique_id = %s"
        mycursor.execute(sql, (idNum,))
        myresult = mycursor.fetchone()
        if not myresult:
            print('Account not found')
        elif myresult[4] == 'Active':
            print(f'Welcome {myresult[1]}!')
            feeQuery = "SELECT * FROM Fee WHERE Fee.client_id = %s"
            mycursor.execute(feeQuery, (idNum,))
            fees = mycursor.fetchall()
            if fees:
                print('Fees outstanding:')
                for fee in fees:
                    if len(fee) == 5:
                        print(f'\n\t{fee[0]}:\nItem: {fee[2]}\nAmount: ${fee[3]}\nFee Due: {fee[4]}')
            else:
                print('No borrowed items')
        else:
            print(f'Client Account not Active, Account: {myresult[1:3]}')


def main():
    choice = 0
    while choice not in ['1','2','3','4']:
        print(f'Welcome, select an option?\n\t1) Queries\n\t2) Generate Reports\n\t3) Staff Interface\n\t4) Client Interface')
        choice=input()
    if choice == '1':
        queryList = loadQuery()
        print(f'Query Options:\
              \n\t1) Show Available books\
              \n\t2) Show Available Digital Media\
              \n\t3) Show Available Magazines\
              \n\t4) Total number of items loaned out by each membership type\
              \n\t5) List all overdue items/late fees\
              \n\t6) List Reserved but not loaned out items\
              \n\t7) List most popular items by number of loans\
              \n\t8) List of total fees collected within the last month, broken down by membership type\
              \n\t9) List of clients who have exceeded their borrowing limits\
              \n\t10) List most frequently borrowed items by each client type\
              \n\t11) List clients have never returned an item late')
        choice = (int(input('Choose an option: '))-1)
        if len(queryList) > choice >= 0:
            results = executeQuery(queryList[choice])
            if choice == 9:
                for row in results:
                    if row[1]:
                        print(row)
            else:
                for row in results:
                    print(row)
    elif choice == '2':
        reports = {0:'MonthlySummaryReport', 1:'ClientActivityReport', 2:'InventoryReport', 3:'OverdueItemReport', 4:'FinancialReport'}
        print(f'Report Options:\
              \n\t1) Monthly Summary Report\
              \n\t2) Client Activity Report\
              \n\t3) Inventory Report\
              \n\t4) Overdue Item Report\
              \n\t5) Financial Report')
        try:
            choice = (int(input('Choose an option: '))-1)
            if len(reports) > choice >= 0:
                results = executeQuery(f'SELECT * FROM {reports[choice]}')
                if results:
                    for row in results:
                        print(row)
                else:
                    print('No results found.')
        except Exception as e:
            print(f'Error occured: {e}')
            return
    elif choice == '3':
        print(f'Staff Interface:\
              \n\t1) Check Out Items\
              \n\t2) Process Returns\
              \n\t3) Add New Items\
              \n\t4) Manage Client Accounts')
        choice = (int(input('Choose an option: '))-1)
        if 4 > choice >= 0:
            staffInterface(choice)
    else:
        print(f'Client Interface:\
              \n\t1) Search Catalog\
              \n\t2) Reserve Item\
              \n\t3) Check Loan Status\
              \n\t4) View outstanding Fees')
        choice = (int(input('Choose an option: '))-1)
        if 4 > choice >= 0:
            clientInterface(choice)


if __name__ == '__main__':
    main()
