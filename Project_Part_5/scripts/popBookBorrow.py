# For book borrowing
import csv, random, datetime

if __name__ == "__main__":
    clients = []
    with open('../Data/clients.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            clients += [lines[0]]
    clients.pop(0)
    book_copy = []
    with open("../Data/book_copy.csv") as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            book_copy.append(lines)
    book_copy.pop(0)
    books = []
    with open('../Data/books.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        isFirst = True 
        for lines in csvFile:
            books.append(lines)
    for cp in book_copy:
        if cp[2] != "Borrowed":
            continue
        out = f'{random.choice(clients)},'
        for y in range(len(books)):
            book = books[y]
            if (cp[1] == book[0]):
                out += cp[0]
                book_copy.pop(y)
                break;
        # Generating a random checkout date in a range
        start = datetime.datetime(2024,10,1,0,0,0)
        delta = datetime.timedelta(days=random.randint(0,62))
        out += ","+ (start + delta).strftime("%Y-%m-%d")  

        # Setting the return window
        delta += datetime.timedelta(days=50)
        out += ","+ (start + delta).strftime("%Y-%m-%d")

        out += ",NULL"
        print(out)
