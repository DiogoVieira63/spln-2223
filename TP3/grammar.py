from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark import Transformer
from lark import Discard

grammar = '''
//Regras Sintaticas
start: items+
items: BREAK item+
item : atributo_termo | lingua
atributo_termo: "_" termo ":" valor
lingua: def_lingua atributos_lingua*
def_lingua: WORD ":" termo
atributos_lingua: "+" termo ":" valor
valor: FRASE | termo | INT | lista 
termo: WORD+
lista: "[" valor ("," valor)* "]"
//Regras Lexicográficas
BREAK: "---"
FRASE: /.*\./
WORD: /[\w\-\(\)][\w\()\-’%\/\+]*/u
//Tratamento dos espaços em branco
%import common.WS
%import common.INT
%ignore WS
'''




class MedicinaTransformer(Transformer):

    def __init__(self) :
        self.termos = []
        self.atributos = {}
        self.linguas = {}

        

    def start(self,args):
        return self.termos

    def items(self,args):
        termo = {"atributos": self.atributos, "linguas": self.linguas}
        self.termos.append(termo)
        self.atributos = {}
        self.linguas = {}
        return args
    
    def item(self,args):
        return args
    
    def atributo_termo(self,args):
        self.atributos[args[0]] = args[1]
        return args
    
    def lingua(self,args):
        key = args[0][0]
        value = args[0][1]
        if key not in self.linguas:
            self.linguas[key] = []
        for index in range(1,len(args)):
            value["atributos"][args[index][0]] = args[index][1]
        self.linguas[key].append(value)
        return args
    
    def def_lingua(self,args):
        return (args[0],{"palavra": args[1], "atributos": {}})
    
    def atributos_lingua(self,args):
        valor = " ".join(args[1:])
        return (args[0],valor)
    
    def valor(self,args):
        return args[0]
    
    def termo(self,args):
        word = " ".join(args)
        return word
    
    def lista(self,args):
        return args
    
    def WORD(self,args):
        return str(args)
   
    def FRASE(self,args):
        return args
    
    def INT(self,args):
        return int(args)
    
    

#class ExemploTransformer(Transformer):


#p = Lark(grammar)   #não muito bem
#
#
#f = open("medicina_completas.txt", "r")
#frase = f.read()
#lista = frase.split("---")
#lista.pop(0)
#termos = []
#for i in range(len(lista)):
#    lista[i] = "---" + lista[i]
#    tree = p.parse(lista[i])
#    print(tree.pretty())
#    data = MedicinaTransformer().transform(tree)
#    termos += data




import json
import os

folder = "hmtl"

if not os.path.exists(folder):
    os.mkdir(folder)

#with open('data.json', 'w') as outfile:
#    json.dump(termos, outfile, indent=4, ensure_ascii=False)

with open('data.json') as infile:
    termos = json.load(infile)




def addTermo(elem,_from,to):
    langs = elem["linguas"][to][1:] if _from == to else elem["linguas"][to]
    if langs:
        text = f'<li><h3>{elem["linguas"][_from][0]["palavra"]}</h3><ul>'
        for palavra in langs:
            text += f'<li>{palavra["palavra"]}</p></li>'
        text+="</ul></li>"
        return text 
    return ""


indices = {}
for elem in termos:
    for _from in elem["linguas"]:
        for to in elem["linguas"]:
            if _from not in indices:
                indices[_from] = {}
            if to not in  indices[_from]:
                indices[_from][to]= ""
            indices[_from][to] += addTermo(elem,_from,to)


for _from in indices:
    for to in indices[_from]:
        pag = f"""
          <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8"/>
                    <link rel="stylesheet" href="../w3.css"/>
                    <title>Dicionário Medicina</title>
                </head>
                <body class="w3-light-gray">
                <div class="w3-container">
                    <ul class="w3-ul"> 
                        {indices[_from][to]}
                    </ul>
                </div>
                </body>
            </html>
        """
        f = open(f"{folder}/dict_{_from}_{to}.html","w")
        f.write(pag)


links = ""

for _from in indices:
    links += f"<li><h3>{_from}</h3><ul>"
    links += f'<li><a href="dict_{_from}_{_from}.html">Synonyms</a>'
    for to in indices[_from]:
        if not(_from == to):
            links += f'<li><a href="dict_{_from}_{to}.html">{to}</a>'
    links+="</ul></li>"


pag = f"""
  <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8"/>
            <link rel="stylesheet" href="../w3.css"/>
            <title>Index</title>
        </head>
        <body class="w3-light-gray">
        <div class="w3-container">
            <ul class="w3-ul"> 
                {links}
            </ul>
        </div>
        </body>
    </html>
"""

f = open(f"{folder}/index.html","w")
f.write(pag)




