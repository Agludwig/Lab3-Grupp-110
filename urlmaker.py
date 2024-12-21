from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
with open("D:\\PythonFiles\\tramstop_google_url.json",encoding='utf-8') as file:#orkar inte hålla på med filväg här
    y = json.load(file)
print(len(y))
url = "https://www.vasttrafik.se/reseplanering/hallplatslista/"

page = requests.get(url)
soup = (BeautifulSoup(page.content, "html.parser"))

hyperlinks = soup.find_all("a")

linkdict = {}
for i in hyperlinks:
    href = i["href"]
    a = i.text.strip()
    
    if "Zon A" in a:
        b = a.split()
        b[-4] = b[-4][:-1]
        stop = " ".join(b[:-3])
        if stop in y:
            linkdict[stop] = href

def stop_url(stop):
    google_url = 'https://www.vasttrafik.se'
    
    return google_url+stop

findict = {}

for i in linkdict:
    findict[i] = stop_url(linkdict[i])

print(len(findict))

z = json.dumps(findict)
with open("TRAM_URL_FILE.json", "w",encoding="utf-8") as file:
    file.write(z)


