# Api key: BQGA39EIATTT66DM
import requests
import urllib.request
import time
import fileinput
import sys
import re
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
    
    print(len(paragraphs))
    for i in range(len(paragraphs)):
        with open(file,'a') as fd:
            fd.write(paragraphs[i])
            fd.write("\n")

# tickerSymbols = ["A", "AA", "AAN","AAP", "AB"]
# get_StockData(tickerSymbols)

url = 'https://finance.yahoo.com/most-active'
tag1 = 'tr'
tag2 = 'td'
#get_YahooStock(url, tag1, tag2, "test.html")

string = []
with open('test.html') as my_file:
    string = my_file.readlines()

#'(?<=>)(-?\w\s?\.?)*'
prog = re.compile('>(.*?)<')
result = prog.findall(string[2])

print(result[1])
#print(response.content)