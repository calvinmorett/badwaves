from urllib.parse import urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import requests

###################
# ex, for testing # 
base = "https://www.badmovies.org/movies/"
url = "http://www.badmovies.org/movies/index.html"
###################

ixval = 2

reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

maintable = soup.find("table", {"class": "tdmainbx"})
alltables = maintable.findAll("table", {"class": "listtab"})
maxtables = int(len(alltables))
maxtables = maxtables + 2
# hard coded 2nd element start
# page elements not working with me
print(maxtables)

### `bad.py`
### gets movie title, rating, 
### media elements and synopsis

def get_wavey(badlink):
    global media_links
    
    r = requests.get(badlink)
    soup = BeautifulSoup(r.text, 'html.parser')

    filetype_wav = 'wav'
    fpindex = soup.find("table", {"class": "tdmainbx"})
    tr = fpindex.findAll("tr", {"": ""})
    fpscan = fpindex.findAll('a', href=True)

    for link in fpscan:
        if link['href']:
            relative = link['href']
            media_links = urljoin(base, relative).strip()
            if filetype_wav in media_links:
                tf.write('|'+str(media_links))

def soupy(tableindex):
    global relative
    global tf
    tf = open('abadwave.txt', 'a')

    # listtab = maintable.find("table", {"class": "listtab"})
    # use getlisttab instead of url
    # you're already on the page you need
    rows = tableindex.findChildren(['tr'])

    for row in rows:
        cellink = row.find_all('a', href=True)
        for link in cellink:
            if link['href']:
                relative = link['href'] 
                badmov = urljoin(base, relative).strip()
                tf.write('\n'+str(badmov))
                
        cells = row.findChildren('td', {"": ""})

        for cell in cells:
            value_string = cell.string
            value_text = cell.text
            img = cell.find('img', alt=True)
            if value_string != None or if img != None:
                if value_string != None:
                    valuestrip = value_text.rstrip()
                    tf.write('|'+str(valuestrip))
                if img != None:
                    ia = img['alt']
                    tf.write('|'+str(ia))
            if value_string == None: # use value_text
                valuestrip = value_text.rstrip()
                tf.write('|'+str(valuestrip))

        for link in cellink:
            if link['href']:
                relative = link['href'] 
                badmov = urljoin(base, relative).strip()
                get_wavey(badmov)
        
                
### end of `bad.py`

### `findtables.py`
### gets tables inside the main page
### run `bad.py` inbetween

def finding():
    global ixval
    global getlisttab
    getlisttab = maintable.select("table", {"class": "listtab"})[ixval]
    gettr = getlisttab.find("td", {"class": "listbox"})
    if gettr == None:
        print('Skip - Bad Sector: ',ixval)
        ixval += 1
        checkindex()
    else:
        soupy(getlisttab)
        
        ixval += 1
        printtr = gettr.get_text()
        print('Currently Scraping: ',printtr,ixval)
        tf.write('\n\n')
        checkindex()

def checkindex():
    global ixval
    if ixval <= maxtables:
        finding()
    else:
        ixval += 1
        print('++ Final add to ixval', ixval)

try:
    print('++ Running check index', ixval)
    checkindex()
except IndexError:
    pass