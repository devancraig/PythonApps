from bs4 import BeautifulSoup
import json
import re
import requests




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

url = 'https://markets.businessinsider.com/stocks/f-stock'
file = 'stock.html'
ans = get_Current_Stock_Price(url, file)
print(ans[0])

