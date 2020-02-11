# Api key: BQGA39EIATTT66DM
import requests
import urllib.request
import time
import fileinput
import sys
import re
import csv
import math
import mysql.connector
from bs4 import BeautifulSoup

# Getting full months worth of stock data using api
def get_StockData(symbols):
    for i in range(len(symbols)):
        response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbols[i] + "&apikey=BQGA39EIATTT66DM&datatype=csv")
        with open(symbols[i] + ".csv",'w') as fd:
            fd.write(response.content.decode("utf-8"))

def get_YahooStock(url, tag1, tag2, file):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ans = soup.find_all(tag1)
    ans2 = soup.find_all(tag2)

    with open(file, "w") as fo:
        fo.truncate()

    paragraphs = []
    for x in ans2:
        paragraphs.append(str(x))
    
    for i in range(len(paragraphs)):
        with open(file,'a') as fd:
            fd.write(paragraphs[i])
            fd.write("\n")
    
    return len(paragraphs)

def get_MostActiveData(htmlFile, outFile, fcount, values):
    string = []
    with open(htmlFile) as my_file:
        string = my_file.readlines()
    
    #'(?<=>)(-?\w\s?\.?)*'
    prog = re.compile('>(.*?)<')
    prog2 = re.compile('aria-label=\"(.*?)\"')
    
    with open(outFile, "w") as fo:
        fo.truncate()
    
    for i in range(fcount):
        # FOR VALUES
        result = prog.findall(string[i])
        values.append(result[1])

        # FOR ID RESULTS
        #result2 = prog2.findall(string[i])
        #tag.append(result2[0])

        # with open(outFile,'a') as fd:
        #     fd.write(tag[i])
        #     fd.write(":  ")
        #     fd.write(output[i])
        #     fd.write("\n")

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def file_len2(fname):
    with open(fname) as f:
        for j, k in enumerate(f):
            pass
    return j + 1


def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()

def amount(balance, price):
    iBal = balance
    temp = math.floor(iBal) / price
    amount = math.floor(temp)
    return amount

def stock_amount(file, array):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            array.append(Stock(row[0], row[1], row[2], row[3], row[4], row[5]))

# def purchase_stock(buyAmount, end, boughtStock, priceStock, amountStock, tempbal, sell):
#     place = 0
#     while end < amountStock:
#         tbal = float(my_list[1].b)
#         tprice = float(price[place])
#         am = amount(tbal, tprice, buyAmount)
#         if am >= 1:
#             bought = Buy(tbal,tprice,am, buyAmount)
#             bal = bought.myfunc()
#             tempbal -= bal
#             boughtStock.append(symbols[place])
#             priceStock.append(float(price[place]) * am)
#             amountStock.append(am)
#             end += 1
#         place += 1
#     return tempbal

# def purchase_stock2(buyAmount, end, boughtStock, priceStock, amountStock, tempbal, sell):
#     place = 0
#     while end < amountStock:
#         tbal = float(my_list[2].b)
#         tprice = float(price2[place])
#         am = amount(tbal, tprice, buyAmount)
#         if am >= 1:
#             bought = Buy(tbal,tprice,am, buyAmount)
#             bal = bought.myfunc()
#             tempbal -= bal
#             boughtStock.append(symbols2[place])
#             priceStock.append(float(price2[place]) * am)
#             amountStock.append(am)
#             end += 1
#         place += 1
#     return tempbal

def sell_stock(sell, percentDiff, cPrice, bought):
    for i in range(5):
        percentDiff.append(((cPrice[i] - bought[i]) / ((bought[i] + cPrice[i]) / 2)) * 100)
        rounded = float(round(percentDiff[i], 2))
        if rounded >= 5 or rounded <= -15:
            sell.append(1)
        else:
            sell.append(0)

def grab_sqlinfo(query):
    connection = mysql.connector.connect(
    host="us-cdbr-iron-east-04.cleardb.net",
    user="b0937237df5488",
    passwd="fd54464a",
    database="heroku_bcead2b1728a15f"
    )

    # sql_select_Query = "select * from Person1"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()

    connection.close()
    cursor.close()
    return records

def insert_sqlinfo(sql, val):
    connection = mysql.connector.connect(
    host="us-cdbr-iron-east-04.cleardb.net",
    user="b0937237df5488",
    passwd="fd54464a",
    database="heroku_bcead2b1728a15f"
    )

    # sql_select_Query = "select * from Person1"
    cursor = connection.cursor()
    cursor.execute(sql, val)

    connection.commit()

def delete_sqlinfo(sql):
    connection = mysql.connector.connect(
    host="us-cdbr-iron-east-04.cleardb.net",
    user="b0937237df5488",
    passwd="fd54464a",
    database="heroku_bcead2b1728a15f"
    )

    # sql_select_Query = "select * from Person1"
    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()

class Person:
    def __init__(self, name, url, balance, Stock1, Stock2, Stock3, Stock4, Stock5, Price1, Price2, Price3, Price4, Price5, Amount1, Amount2, Amount3, Amount4, Amount5):
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
        self.A1 = Amount1
        self.A2 = Amount2
        self.A3 = Amount3
        self.A4 = Amount4
        self.A5 = Amount5


class Stock:
    def __init__(self,timestamp,open,high,low,close,volume):
        self.time = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume


class Buy:
  def __init__(self, bal, price, amount, buy):
    self.b = bal
    self.p = price
    self.a = amount
    self.buy = buy

  def myfunc(self):
    i = 0
    while i < self.a:
        holdbal = self.b / self.buy
        if holdbal > self.p:
            holdbal -= self.p
        i += 1
    return float(holdbal) 


def bought_it(a, bal, price):
    i = 0
    while i < a:
        holdbal = bal
        if holdbal > price:
            holdbal -= price
        i += 1
    return float(holdbal) 

# my_list=[]
# with open('test.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         my_list.append(Person(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],row[13],row[14],row[15],row[16],row[17]))


htmlFile = "trending.html"
htmlFile2 = "gainer.html"
outFile = "out.txt"
#url = 'https://finance.yahoo.com/gainers'
tag1 = 'tr'
tag2 = 'td'




# START OF THE FIRST PERSON #


fileCount = get_YahooStock("https://finance.yahoo.com/most-active", tag1, tag2, htmlFile)

values = []
get_MostActiveData(htmlFile, outFile, fileCount, values)

symbols = values[::10]
price = values[2::10]
change = values[4::10]

query = "select * from Person1"
records = grab_sqlinfo(query)

own_symbols = []
stock_Amount = []
bal = []
og_price = []
ids = []

for rows in records:
    own_symbols.append(rows[2])
    stock_Amount.append(rows[4])
    bal.append(rows[1])
    og_price.append(rows[3])
    ids.append(rows[0])

# tickerSymbols = [own_symbols[0], own_symbols[1], own_symbols[2], own_symbols[3], own_symbols[4]]
# get_StockData(tickerSymbols)

stock_list = []
for tot in range(5):
    with open(own_symbols[tot] + ".csv", 'r') as f:
        lines = f.readlines()
        stock_list.append(lines[1].split(",")[1])


# print(Stock_list[0].split(",")[1])
buyAmount = 5
end = 0
boughtStock = []
priceStock = []
amountStock = []
# tempbal = float(my_list[1].b)

bought = []
query1 = "SELECT * FROM paid"
total = grab_sqlinfo(query1)



sell = []
percentDiff = []
cPrice = [float(stock_list[0]) * stock_Amount[0], float(stock_list[1]) * stock_Amount[1], float(stock_list[2]) * stock_Amount[2], float(stock_list[3]) * stock_Amount[3], float(stock_list[4]) * stock_Amount[4]]

for t in total:
    bought.append(t[0])

sell_stock(sell, percentDiff, cPrice, bought)

amountToBuy = sell.count(1)

num = 0
while end < amountToBuy:
    newBal = 0
    if(sell[num] == 1):
        newBal = (float(stock_list[num]) * stock_Amount[num]) + bal[num]
        tprice = float(price[num])
        am = amount(newBal, tprice)
        if am >= 1:
            bal = bought_it(am, newBal, tprice)
            newBal -= bal
            sql1 = "DELETE FROM person1 WHERE Id = " + str(ids[num])
            delete_sqlinfo(sql1)
            sql = "INSERT INTO person1 (balance, stockname, price, amount) VALUES (%s, %s, %s, %s)"
            val = (str(newBal), str(symbols[num]), str(tprice), str(am))
            insert_sqlinfo(sql, val)
            end += 1
        else:
            num += 1
    num += 1

# amount = sell.count(1)
# new_balance = purchase_stock(buyAmount, end, boughtStock, priceStock, amount, tempbal, sell)

# START OF THE SECOND PERSON #
# fileCount2 = get_YahooStock(my_list[2].u, tag1, tag2, htmlFile2)

# values2 = []
# get_MostActiveData(htmlFile2, outFile, fileCount2, values2)

# symbols2 = values2[::10]
# price2 = values2[2::10]
# change2 = values2[4::10]

# buyAmount1 = 5
# end1 = 0
# boughtStock1 = []
# priceStock1 = []
# amountStock1 = []
# tempbal1 = float(my_list[2].b)



# sell1 = []
# percentDiff1 = []
# bought1 = [float(my_list[2].P1), float(my_list[2].P2), float(my_list[2].P3), float(my_list[2].P4), float(my_list[2].P5)]
# cPrice1 = [float(stock_list1[2].open) * float(my_list[2].A1), float(stock_list2[2].open) * float(my_list[2].A2), float(stock_list3[2].open) * float(my_list[2].A3), float(stock_list4[2].open) * float(my_list[2].A4), float(stock_list5[2].open) * float(my_list[2].A5)]

# sell_stock(sell1, percentDiff1, cPrice1, bought1)
# amount1 = sell1.count(1)
# new_balance1 = purchase_stock2(buyAmount1, end1, boughtStock1, priceStock1, amount1, tempbal1, sell1)

# with open('test.csv', mode='w') as person:
#     person_writer = csv.writer(person, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     person_writer.writerow(["name","url","balance","Stock1","Stock2","Stock3","Stock4","Stock5","Price1","Price2","Price3","Price4","Price5","Amount1","Amount2","Amount3","Amount4","Amount5"])
#     person_writer.writerow([my_list[1].n, my_list[1].u, new_balance, boughtStock[0], boughtStock[1], boughtStock[2], boughtStock[3], boughtStock[4], priceStock[0], priceStock[1], priceStock[2], priceStock[3], priceStock[4], amountStock[0], amountStock[1], amountStock[2], amountStock[3], amountStock[4]])
#     person_writer.writerow([my_list[2].n, my_list[2].u, new_balance1, boughtStock1[0], boughtStock1[1], boughtStock1[2], boughtStock1[3], boughtStock1[4], priceStock1[0], priceStock1[1], priceStock1[2], priceStock1[3], priceStock1[4], amountStock1[0], amountStock1[1], amountStock1[2], amountStock1[3], amountStock1[4]])

# remove_empty_lines("test.csv")
