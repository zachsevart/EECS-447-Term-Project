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
  password="password", # Fill out your MySQL password here
  database='project'
)
# Create cursor to interact with DB
mycursor = mydb.cursor()


def executeQuery(query):
    mycursor.execute(query)
    return mycursor.fetchall()

def loadQuery():
    with open(os.path.join(parentDir, 'Sql_Files', 'Queries.sql'), "r") as file:
        queries = file.read()

    # Split the file into individual queries based on semicolons
    queriesList = queries.split(";")

    # Clean up lines
    return [q.strip() for q in queriesList if q.strip()]


def loadReports():
    with open(os.path.join(parentDir, 'Sql_Files', 'Reports.sql'), "r") as file:
        reports = file.read()

    # Split the file into individual reports based on semicolon
    reportList = reports.split(";")

    return [r.strip() for r in reportList if r.strip()] 



'''
TODO: Code the processes below, if not understanding how to do the code
    If you can map out what all needs to be changed and what tables and in order we can code that ezpz after

TODO: Look into DATEDIFF or other date based sql/python stuff to
    figure our how to get a date X days after given date for fee date
'''
def staffInterface(choice):
    if choice == 0: # Check out (Check membership type against borrowing limit, change status of media, set date, create fee date = Date + 30, edit borrowing)
        pass
    elif choice == 1: # Process Returns (Change status, set return date, create fee if needed, edit borrowing table)
        pass
    elif choice == 2: # Add new items (Insert new book/book_copy, magazine, digital media)
        pass
    elif choice == 3: # Manage Client Accounts (Change Client.account_status only)
        pass


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
    elif choice == 1: # Reserve items
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
                    for x in myresult:
                        print(f'Selected Book: {x}')
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
        sql = ""
        mycursor.execute()
    elif choice == 3: # View outstanding fees
        pass


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
            for row in results:
                print(row)
    elif choice == '2':
        reportList = loadReports()
        print(f'Report Options:\
              \n\t1) Monthly Summary Report\
              \n\t2) Client Activity Report\
              \n\t3) Inventory Report\
              \n\t4) Overdue Item Report\
              \n\t5) Financial Report')
        choice = (int(input('Choose an option: '))-1)
        if len(reportList) > choice >= 0:
            results = executeQuery(reportList[choice])
            for row in results:
                print(row)
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
