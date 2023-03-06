import json
import re 

# load json

completas = []
remissivas = []

with open("medicina.json") as f:
    content = json.load(f)
    completas = content["completas"]
    remissivas = content["remissivas"]


def build_ga(elem, termo):
    atributo_genero(elem['género'],termo["atributos"])
    termo["atributos"]['multiplcidade'] = "plural" if elem['plural'] == "yes" else "singular"
    if 'nota' in elem:
        termo['nota'] = elem['nota']
        if termo['nota'][-1] != '.':
            termo['nota'] += '.'
        del(elem['nota'])
    if 'variacoes' in elem:
        del(elem['variacoes'])
    del(elem['nome'])
    del(elem['género'])
    del(elem['plural'])



def check_atributo(regex,elem,obj, f):
    if l := re.findall(regex,elem):
        for value in l: 
            if type(value) == tuple:
                for x in value:
                    if (f(x,obj)):
                        elem = re.sub(regex,'',elem)
            else:
                if (f(value,obj)):
                    elem = re.sub(regex,'',elem)
    return elem



def atributo_genero(value,atributos):
    at = ""
    if value == "m":
        at = "masculino"
    elif value == "f":
        at =  "feminino"
    elif value == "s":
        at = "variação"
    elif value == "pl":
        atributos["multiplicade"] = "plural"
        return True
    else:
        return False
    atributos["género"]=at
    return True


def atributo_forma(value,atributos):
    at=""
    if value=="arc":
        at = "arcaica"
    elif value == "col":
        at = "coloquial"
    elif value == "pop":
        at = "popular"
    elif value == "cult":
        at = "culta"
    elif value == "lit":
        at = "literária"
    elif value == "loc":
        at = "locução"
    elif value == "ant":
        at = "antiga"
    else:
        return False
    atributos["forma"] = at
    return True

def atributo_representacao(value,atributos):
    at=""
    if value=="abrev":
        at = "abreviatura"
    elif value == "sb":
        at = "símbolo"
    elif value == "sg":
        at = "sigla"
    else:
        return False
    atributos["representação"] = at
    return True


def atributo_variacao_lingua(value,atributos):
    at=""
    if value=="Pt":
        at = "Português de Portugal"
    elif value == "Br":
        at = "Portugues do Brasil"
    elif value == "EE. UU.":
        at = "Inglês dos EUA"
    else:
        return False
    atributos["origem linguística"] = at
    return True
    



def check_for_atributos(elem):
    atributos = { }
    elems = elem.split(';')
    if len(elems) > 1:
        termo = []
        for item in elems:
            if item.strip() != '':
                termo+= check_for_atributos(item)
        return termo
    else:
        before = elem
        elem = elem.strip()
        elem = check_atributo(r'\((pl|[smf])( pl)?\)',elem,atributos,atributo_genero)
        elem = check_atributo(r'[\[\(](\w+)\.?[\]\)]',elem,atributos,atributo_forma) 
        elem = check_atributo(r'[\[\(](Br|Pt|EE\. UU\.)\.?[\]\)]',elem,atributos,atributo_variacao_lingua) 
        elem = check_atributo(r'\((\w+)\.?\)',elem,atributos,atributo_representacao)
        #elem = check_atributo(r'(\[|\(Pt\.?(\]|\))',elem,atributos,'Portugal')
        #elem = check_atributo(r'\[EE\. UU\.\]',elem,atributos,'EUA')

        elem = elem.strip()
        if elem != '':
            termo = {"palavra" : elem, "atributos": atributos}  
            return [termo]
    return []
    
    
def write_file(filename,data):
    with open(filename, 'w') as outfile:
        for elem in data:
            outfile.write("---\n")
            for key, value in elem.items():
                if key == "traducoes":
                    for key2, value2 in value.items():
                        for termo in value2:
                            outfile.write(f"{key2.strip()}: {termo['palavra']}\n")
                            for k, v in termo.items():
                                if k != "atributos" and k != "palavra":
                                    outfile.write(f"+{k}: {v}\n")
                            for key3, value3 in termo['atributos'].items():
                                outfile.write(f"+{key3}: {value3}\n")
                else:
                    outfile.write(f"_{key}: {value}\n")
                
for elem in completas:
    ga = check_for_atributos(elem['nome'])
    build_ga(elem, ga[0])
    elem['categoria'] = "[ " + " , ".join(elem['categoria']) + " ]"
    for key,value in elem['traducoes'].items():
        elem['traducoes'][key] = []
        for item in value:
            termo = check_for_atributos(item)
            termo = [x for x in termo if x != []]
            elem['traducoes'][key] += termo
    elem['traducoes']['ga'] = ga
    if 'sinonimos' in elem:
        print(elem['sinonimos'])
        for item in elem['sinonimos']:
            termo = check_for_atributos(item)
            termo = [x for x in termo if x != []]
            elem['traducoes']['ga']+= termo
        del(elem['sinonimos'])

#with open("medicina_completas.json", 'w') as outfile:
#    json.dump(completas, outfile, indent=4, ensure_ascii=False)
    
write_file("medicina_completas.txt",completas)


    
        


