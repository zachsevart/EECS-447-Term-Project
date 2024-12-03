import csv
import random

if __name__ == "__main__":
    with open('../Data/books.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        num = 0
        for lines in csvFile:
            
            out = f'{num},'
            count = 0
            for x in lines:
                if count == 0:
                    out += x + ","
                count += 1
            status = ["Available", "Borrowed", "Reserved", "Lost", "Maintenance","Available","Available", "Available"]
            out += random.choice(status)
            print(out)
            num += 1
     
