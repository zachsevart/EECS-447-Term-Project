import csv
import random

if __name__ == "__main__":
    with open('../Data/clients.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            out = ""
            count = 0
            for x in lines:
                if count == 1:
                    out += x + " "
                elif count == 2:
                    out += x + ","
                else:
                    out += x + ","
                count += 1
            memb_type = ["Senior", "Regular", "Student"]
            account_status = ["Active", "Suspended", "Expired"]
            temp = random.choice(memb_type)+ "," + random.choice(account_status)
            print(out)
            
