# For populating the Digital Media Borrowing table
import csv, random, datetime

if __name__ == "__main__":
    clients = []
    with open('../Data/clients.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            clients += [lines[0]]
    clients.pop(0)
    media = []
    with open('../Data/digitalmedia.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        isFirst = True 
        for lines in csvFile:
            media.append(lines)
    media.pop(0)
    for med in media:
        if(med[6] != "Borrowed"):
            continue
        out = f'{random.choice(clients)},'
        out += f'{random.choice(media)[0]}'
        # Generating a random checkout date in a range
        start = datetime.datetime(2024,9,1,0,0,0)
        delta = datetime.timedelta(days=random.randint(0,93))
        out += ","+ (start + delta).strftime("%Y-%m-%d")  

        # Setting the return window
        delta += datetime.timedelta(days=50)
        out += ","+ (start + delta).strftime("%Y-%m-%d")

        print(out)
