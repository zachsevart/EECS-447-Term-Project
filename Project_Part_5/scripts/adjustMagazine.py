
# For populating the Magazine Borrowing table
import csv, random, datetime

if __name__ == "__main__":
    clients = []
    with open('../Data/digitalmedia.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            out = ""
            for x in lines:
                if x == "Available":
                    choices = ['Available','Available','Borrowed', 'Borrowed', 'Reserved']
                    out += random.choice(choices)
                else:
                    out += x + ","
            print(out) 
