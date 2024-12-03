import csv
import random
import mysql.connector # pip install mysql-connector-python
import os

# Get directory of parent for use with proper execution
parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Connect to MySQL db
mydb = mysql.connector.connect(
  host="localhost",
  user="username", # Fill out MySQL username here TODO: store in a config file that is in .gitignore
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
        if choice >= 0 and len(queryList) > choice:
            results = executeQuery(queryList[choice])
            for row in results:
                print(row)
    elif choice == '2':
        print(f'Report Options:\
              \n\t1) Monthly Sumamry Report\
              \n\t2) Client Activity Report\
              \n\t3) Inventory Report\
              \n\t4) Overdue Item Report\
              \n\t5) Financial Report')
    elif choice == '3':
        print(f'Staff Interface:\
              \n\t1) Check Out Items\
              \n\t2) Process Returns\
              \n\t3) Add New Items\
              \n\t4) Manage Client Accounts')
    else:
        print(f'Client Interface:\
              \n\t1) Search Catalog\
              \n\t2) Reserve Item\
              \n\t3) Check Loan Status\
              \n\t4) View outstanding Fees')


if __name__ == '__main__':
    main()
