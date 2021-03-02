import requests 
import re 

rootdir = "/Users/mattiashallberg/Dropbox/PhD/data/valresultat/"
url_stub = "https://data.val.se/val/val2006/slutlig/xml/"
r = requests.get("https://data.val.se/val/val2006/slutlig/xml/index.html")
for file in re.findall(r'slutresultat_\d{2,4}[KLR].xml' , r.text):
    path = rootdir+"raw/2006/"+file
    with open(path, 'wb') as f:
        for chunk in requests.get(url_stub+file):
            f.write(chunk)
