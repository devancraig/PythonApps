import requests
import re
from bs4 import BeautifulSoup

def get_YahooStock(url, tag1, tag2, files):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ans = soup.find_all(tag1)
    ans2 = soup.find_all(tag2)

    with open(files, "w") as fo:
        fo.truncate()

    paragraphs = []
    for x in ans2:
        paragraphs.append(str(x))
    
    for i in range(len(paragraphs)):
        with open(files,'a') as fd:
            fd.write(paragraphs[i])
            fd.write("\n")
    
    return len(paragraphs)

def get_MostActiveData(htmlFile, fcount, values):
    string = []
    with open(htmlFile) as my_file:
        string = my_file.readlines()
    
    #'(?<=>)(-?\w\s?\.?)*'
    prog = re.compile('>(.*?)<')
    # prog2 = re.compile('aria-label=\"(.*?)\"')
    
    # with open(outFile, "w") as fo:
    #     fo.truncate()
    
    for i in range(6):
        # FOR VALUES
        result = prog.findall(string[i])
        values.append(result[1])

url = "https://finance.yahoo.com/quote/GOOGL"
tag1 = 'tr'
tag2 = 'td'
files = "lookup.html"
fileCount = get_YahooStock(url, tag1, tag2, files)

values = []
get_MostActiveData(files, fileCount, values)
print(values[3])
