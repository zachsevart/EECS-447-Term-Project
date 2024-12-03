# For populating the Magazine Borrowing table
import csv, random, datetime

if __name__ == "__main__":
    clients = []
    with open('../Data/clients.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            clients += [lines[0]]
    clients.pop(0)
    magazines = []
    with open('../Data/magazines.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        isFirst = True 
        for lines in csvFile:
            magazines.append(lines)
    magazines.pop()
    for mag in magazines:
        if(mag[5] != "Borrowed"):
            continue
        out = f'{random.choice(clients)},'
        out += f'{random.choice(magazines)[0]}'
        # Generating a random checkout date in a range
        start = datetime.datetime(2024,9,1,0,0,0)
        delta = datetime.timedelta(days=random.randint(0,93))
        out += ","+ (start + delta).strftime("%Y-%m-%d")  

        # Setting the return window
        delta += datetime.timedelta(days=50)
        out += ","+ (start + delta).strftime("%Y-%m-%d")

        print(out)
