# For adding books that were previously checked out and returned 
import csv, random, datetime

def rand_book(clients, cpy):
    # Add a random client
    out = f'{random.choice(clients)},'
    out += cpy[0]
    # Generating a random checkout date in a range
    start = datetime.datetime(2024,6,1,0,0,0)
    delta = datetime.timedelta(days=random.randint(0,140))
    out += ","+ (start + delta).strftime("%Y-%m-%d")  
    checked = start + delta

    # Setting the return window
    delta += datetime.timedelta(days=50)
    out += ","+ (start + delta).strftime("%Y-%m-%d")

    # Setting the return date 
    delta = datetime.timedelta(days=random.randint(0,58))
    out += ","+ (checked + delta).strftime("%Y-%m-%d")

    print(out)

def rand_media(clients, cpy):
    # Add a random client
    out = f'{random.choice(clients)},'
    out += cpy[0]
    # Generating a random checkout date in a range
    start = datetime.datetime(2024,6,1,0,0,0)
    delta = datetime.timedelta(days=random.randint(0,140))
    out += ","+ (start + delta).strftime("%Y-%m-%d")  
    checked = start + delta

    # Setting the return window
    delta += datetime.timedelta(days=50)
    out += ","+ (start + delta).strftime("%Y-%m-%d")

    # Setting the return date 
    delta = datetime.timedelta(days=random.randint(0,58))
    out += ","+ (checked + delta).strftime("%Y-%m-%d")

    print(out)

def rand_mag(clients, cpy):
    # Add a random client
    out = f'{random.choice(clients)},'
    out += cpy[0]
    # Generating a random checkout date in a range
    start = datetime.datetime(2024,6,1,0,0,0)
    delta = datetime.timedelta(days=random.randint(0,140))
    out += ","+ (start + delta).strftime("%Y-%m-%d")  
    checked = start + delta

    # Setting the return window
    delta += datetime.timedelta(days=50)
    out += ","+ (start + delta).strftime("%Y-%m-%d")

    # Setting the return date 
    delta = datetime.timedelta(days=random.randint(0,65))
    out += ","+ (checked + delta).strftime("%Y-%m-%d")

    print(out)

if __name__ == "__main__":
    clients = []
    with open('../Data/clients.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            clients += [lines[0]]
    clients.pop(0)
    media = []
    with open("../Data/digitalmedia.csv") as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            media.append(lines)
    media.pop(0)
    books = []
    with open('../Data/books.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        isFirst = True 
        for lines in csvFile:
            books.append(lines)
    for thing in media:
        num_checkouts = random.choice([0,1,2,3])
        for x in range(num_checkouts):
            rand_mag(clients, thing)

