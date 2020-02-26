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
from datetime import datetime
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

def get_CurrentPrice(htmlFile, outFile, fcount, values):
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
        if i == 5:
            values.append(result[1])
        

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
    purchased = amount * price
    return purchased, amount
    
    

 
def sell_stock(sell, percentDiff, cPrice, bought):
    for i in range(5):
        percentDiff.append(((cPrice[i] - bought[i]) / ((bought[i] + cPrice[i]) / 2)) * 100)
        rounded = float(round(percentDiff[i], 2))
        if rounded >= 1 or rounded <= -10:
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

    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()

def bought_it(a, bal, price):
    i = 0
    while i < a:
        holdbal = bal
        if holdbal > price:
            holdbal -= price
        i += 1
    return float(holdbal)

    
def purchase(sell, num, price, symbols, ids, bal, pTime):
    newBal = 0
    if(sell[num] == 1):
        newBal = cPrice[num] + bal[num]
        tprice = float(price[num])
        bought_total, am = amount(newBal, tprice)
        if am > 0:
            newBal -= bought_total
            sql1 = "DELETE FROM person1 WHERE Id = " + str(ids[num])
            delete_sqlinfo(sql1)
            print("purchasing: " + str(symbols[num]) + " Price: " + str(tprice) + " Amount: " + str(am))
            sql = "INSERT INTO person1 (balance, stockname, price, amount) VALUES (%s, %s, %s, %s)"
            val = (str(newBal), str(symbols[num]), str(tprice), str(am))
            insert_sqlinfo(sql, val)
            sql1 = "INSERT INTO purchased (stockname, price, amount, date) VALUES (%s, %s, %s, %s)"
            val1 = (str(symbols[num]), str(tprice), str(am), str(pTime))
            insert_sqlinfo(sql1, val1)

def get_Current_Stock_Price(url, file):
  r = requests.get(url)
  with open(file, 'wb') as f:
      f.write(r.content)

  pattern = re.compile("\"price\": \"(.*?)\"")
  textfile = open(file, 'r')
  matches = []
  for line in textfile:
      matches += pattern.findall(line)
  textfile.close()
  return matches
     



htmlFile = "trending.html"
htmlFile2 = "gainer.html"
outFile = "out.txt"
#url = 'https://finance.yahoo.com/gainers'
tag1 = 'tr'
tag2 = 'td'

start = datetime.now()
current_start = start.strftime("%D %H:%M:%S")

# START OF THE FIRST PERSON #
fileCount = get_YahooStock("https://finance.yahoo.com/most-active", tag1, tag2, htmlFile)

values = []
get_MostActiveData(htmlFile, outFile, fileCount, values)

symbols = values[::10]
price = values[2::10]
change = values[3::10]

# GRABS ALL CURRENT STOCK OWNED AND ALL THE ATTRIBUTES #
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

# FINDS CURRENT STOCK PRICES #
urls = []

values2 = []
fname = "stock.html"
for x in range(5):
    urls.append("https://markets.businessinsider.com/stocks/" + own_symbols[x])
    values2 += get_Current_Stock_Price(urls[x], fname)

buyAmount = 5
end = 0
boughtStock = []
priceStock = []
amountStock = []

bought = []
query1 = "SELECT * FROM paid"
total = grab_sqlinfo(query1)

sell = []
percentDiff = []
cPrice = [float(values2[0]) * stock_Amount[0], float(values2[1]) * stock_Amount[1], float(values2[2]) * stock_Amount[2], float(values2[3]) * stock_Amount[3], float(values2[4]) * stock_Amount[4]]

for t in total:
    bought.append(t[0])

sell_stock(sell, percentDiff, cPrice, bought)
amountToBuy = sell.count(1)

stocks_to_buy = []
new_symbols = []
for ch in range(len(price)):
    if float(change[ch]) > 0 and float(price[ch]) < 200:
        stocks_to_buy.append(price[ch])
        new_symbols.append(symbols[ch])

# PURCHASE STOCK IF NEED BE #
for k in range(len(sell)):
    print("stock: " + str(own_symbols[k]) + " percentDiff: " + str(percentDiff[k]))
    if sell[k] == 1:
        purchase(sell, k, stocks_to_buy, new_symbols, ids, bal, current_start)


# USED FOR LOGGING THE CURRENT TIME OF PROGRAM #
endTime = datetime.now()
current_end = endTime.strftime("%D:%H:%M:%S")

sql2 = "INSERT INTO logger (StartTime, EndTime) VALUES (%s, %s)"
val2 = (str(current_start), str(current_end))
insert_sqlinfo(sql2, val2)

