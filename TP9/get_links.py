from bs4 import BeautifulSoup as bs
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: python aula.py <url>")
    sys.exit(1)

url = sys.argv[1]


conteudo = requests.get(url).text

doc_tree = bs(conteudo, 'lxml')

links = doc_tree.find_all('a')

#get url with main domain only
url = url.split('/')[:-1]
url = '/'.join(url)

# check if href is present
for link in links:
    if link.has_attr('href'):
        href = link['href']
        if href.startswith('http'):
            print(href)
        else:
            print(f"{url}/{href}")
            
