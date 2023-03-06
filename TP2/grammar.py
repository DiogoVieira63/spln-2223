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
termo: WORD*
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

p = Lark(grammar)   #não muito bem


f = open("medicina_completas.txt", "r")
frase = f.read()
lista = frase.split("---")
lista.pop(0)
termos = []
for i in range(len(lista)):
    lista[i] = "---" + lista[i]
    tree = p.parse(lista[i])
    data = MedicinaTransformer().transform(tree)
    termos += data

import json

with open('data.json', 'w') as outfile:
    json.dump(termos, outfile, indent=4, ensure_ascii=False)