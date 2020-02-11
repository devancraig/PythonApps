import csv
import sys

class Person:
    def __init__(self, name, url, balance, Stock1, Stock2, Stock3, Stock4, Stock5, Price1, Price2, Price3, Price4, Price5):
        self.n = name
        self.u = url
        self.b = balance
        self.S1 = Stock1
        self.S2 = Stock2
        self.S3 = Stock3
        self.S4 = Stock4
        self.S5 = Stock5
        self.P1 = Price1
        self.P2 = Price2
        self.P3 = Price3
        self.P4 = Price4
        self.P5 = Price5


my_list = []

with open('test.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        my_list.append(Person(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]))

print(my_list[0].n)
with open('test.csv', mode='w') as person:
    person_writer = csv.writer(person, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    person_writer.writerow(["name","url","balance","Stock1","Stock2","Stock3","Stock4","Stock5","Price1","Price2","Price3","Price4","Price5"])
    person_writer.writerow([my_list[1].n, my_list[1].u, my_list[1].b,",",",",",",",",",",",",",",",",",",","])
    person_writer.writerow([my_list[2].n, my_list[2].u, my_list[2].b,",",",",",",",",",",",",",",",",",",","])

def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

remove_empty_lines("test.csv")


