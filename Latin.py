import requests
import sys
from bs4 import BeautifulSoup



def getTrans(word):
    URL = "https://www.online-latin-dictionary.com/latin-english-dictionary.php?parola=" + word
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #results = soup.find(id='wrapper')
    #print(soup.div)
    search = soup.find_all('span', class_='english')
    res = ''

    if (search == []):
        search = soup.find_all('a')[20]
        page = requests.get("https://www.online-latin-dictionary.com/" + search.get('href'))
        soup = BeautifulSoup(page.content, 'html.parser')
        search = soup.find_all('span', class_='english')
    if search != []:
        i = 0
        search = search[0]
        while search.text[i] != ',':
             i +=1
             if i == len(search.text):
                 break
        res = search.text[0:i]
    return res


text = sys.argv[1]
s = open (text, 'r+')
t = open (text + '(trans)', 'a')
for line in s:
    wstart = 0
    newline = ''
    test = False
    for i in range(len(line)):
        if (line[i] == ' ' or line[i] ==  ',' or line[i] ==  '.' or line[i] ==  ':' or line[i] ==  ';' or line[i] ==  '?' or line[i] ==  '!' or line[i] == '\n') and not test:
            newline += line[wstart : i]
            word = line[wstart : i]
            newline += ' (' + getTrans(word) + ')' + line[i]
            wstart = i+2 if i < len(line)-1 and line[i+1] == ' ' else i+1
            i += 1
            if i < len(line) and line[i] == '\n':
                newline += line[i]
            test = True
        else:
            test = False
            continue
    t.write(newline)
