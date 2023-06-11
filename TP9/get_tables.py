from bs4 import BeautifulSoup as bs
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: python aula.py <url>")
    sys.exit(1)

url = sys.argv[1]


conteudo = requests.get(url).text

doc_tree = bs(conteudo, 'lxml')

tabelas = doc_tree.find_all('table')


index = 0
for tabela in tabelas:
    print(f"-------Table {index}----------")
    linhas = tabela.find_all('tr')
    for linha in linhas:
        colunas = linha.find_all('td')
        linha_txt = ";".join([coluna.text for coluna in colunas])
        print(linha_txt)
    print(f"----------END Table {index}----------")
    index += 1