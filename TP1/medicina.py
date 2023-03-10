
import re

file2 = open("medicina.xml", "r")

texto_xml = file2.readlines()

texto_xml = texto_xml[23:-1]


texto_xml = "".join(texto_xml)


def write_to_file(texto,file):
    file = open(file, "w")
    file.write(texto)
    file.close()

def remove_header_footer(texto):
    texto = re.sub(r"<text.*>ocabulario</text>",'###',texto)
    texto = re.sub(r".*\n###\n.*\n",r'',texto)
    return texto

texto_xml = remove_header_footer(texto_xml)

def remove_irrelevant(texto):
    texto = re.sub(r"<.*font=\"(.*)\">(.*)<.*>",r"#\1#\2",texto)
    texto = re.sub(r"</?page+.*\n","",texto)
    texto = re.sub(r" *<fontspec+.*\n","",texto)
    texto = re.sub(r"#.*# +\n","",texto)
    texto = re.sub(r"#(\d+)#(.*)\n#(14|15)#(.*)\n",r'#\1#\2\3\n',texto)
    return texto


texto_xml = remove_irrelevant(texto_xml)



def remove_spaces_tags(texto):
    texto = re.sub(r"<i>(.*)</i>\n",r"\1\n",texto)
    texto = re.sub(r"<b>(.*)</b>\n",r"\1\n",texto)
    texto = re.sub(r"#[^3]# *\n",r"",texto)
    texto = re.sub(r" +",r" ",texto)
    texto = re.sub(r"#.*# *\n",r"",texto)
    return texto


texto_xml = remove_spaces_tags(texto_xml)

def fix_definition_numbers(texto):
    texto = re.sub(r"#2#(.*)\n#(.*)#(.*)",r'#\2#\1\3',texto)
    texto = re.sub(r"#12#(.*)\n#(.*)#(.*)",r'#\2#\1\3',texto)
    return texto

texto_xml = fix_definition_numbers(texto_xml)

def mark_defs(texto):
    texto = re.sub(r"#3#(.*)\n#13#(.*)",r"#3#\1\2",texto)
    while re.search(r"#3#(.*)\n#3#(.*)",texto):
        texto = re.sub(r"#3#(.*)\n#3#(.*)",r'#3#\1\2',texto)
    texto = re.sub(r"#3#(.*)\n#10#(.*)\n#3#(.*)",r"#3#\1\2\3",texto)
    texto = re.sub(r"#11#(.*)",r'#3#\1',texto)
    texto = re.sub(r"#10#(.*)",r'#3#\1',texto)
    texto = re.sub(r"#3#(.*)",r'###\1',texto)
    return texto

texto_xml = mark_defs(texto_xml)
write_to_file(texto_xml,"defs.txt")

def mark_categorias(texto):
    texto = re.sub(r"###(.*)\n#.*#(.*)\n",r'###\1\n\2\n',texto)
    return texto

texto_xml = mark_categorias(texto_xml)

def mark_translations(texto):
    texto = re.sub(r"#7#(.*)\n",r'-\1\n',texto)
    texto = re.sub(r"-(.*)\n-(.*)",r'-\1 \2',texto)
    texto = re.sub(r"-(.*)\n#.*# *; *",r'-\1',texto)
    texto = re.sub(r"#.*#(.*)\n-(.*)",r"@@@\1\n-\2",texto)
    return texto

texto_xml = mark_translations(texto_xml)
write_to_file(texto_xml,"translations.txt")



def mark_SYN_VID(texto):
    while re.search(r"#[56]#(.*)\n#[56]#(.*)",texto):
        texto = re.sub(r"#[56]#(.*)\n#[56]#(.*)",r'#5#\1\2',texto)
    texto = re.sub(r"#5#(.*)\n",r'\1\n',texto)
    texto = re.sub(r"VAR(.*)\n",r'\nVAR\1\n',texto)
    return texto

texto_xml = mark_SYN_VID(texto_xml)
write_to_file(texto_xml,"syn_vid.txt")

def mark_notas(texto):
    while re.search(r"#9#(.*)\n#9#(.*)",texto):
        texto = re.sub(r"#9#(.*)\n#9#(.*)",r'#9#\1\2',texto)
    texto = re.sub(r"#9#(.*)\n",r'\1\n',texto)
    return texto

texto_xml = mark_notas(texto_xml)
write_to_file(texto_xml,"notas.txt")


def remove_rest(texto):
    #while re.search(r"#\d+#",texto):
    texto = re.sub(r"#(\d+)#(.*)\n#\1#(.*)",r'#\1#\2\3',texto)
    texto = re.sub(r"#\d+#",r'',texto)
    texto = re.sub(r" +",r" ",texto)
    texto = re.sub(r"\n +",r"\n",texto)
    texto = re.sub(r"\n+",r"\n",texto)
    return texto

texto_xml = remove_rest(texto_xml)
write_to_file(texto_xml,"rest.txt")



defs_array = texto_xml.split("###")

completas = []
remissivas = []

last = 0

defs_array = defs_array[1:]

def parse_completa(result):
    global last
    entrada = {
        "nome": result.group(2).strip(),
        "g??nero": result.group(3),
        "plural": "yes" if result.group(4) else "no",
        "ind??ce": result.group(1),
    }
    last += 1
    completas.append(entrada)
    return entrada


def parse_remissivas(defs,result):
    first = defs[0]
    for index in range(1,len(defs)):
        if "Vid." not in defs[index]:
            first += defs[index]
        else:
            break
    defs = [first] + defs[index:]
    defs[1] =" ".join([s.strip() for s in defs[1:]])
    if result:= re.match(r" *Vid.-?(.*)",defs[1]):
        res = result.group(1).strip()
        referencia = {defs[0].strip(): res} 
    remissivas.append(referencia)

for defs in defs_array:
    defs = defs.split("\n")
    result = re.search(r"^ *(\d+) *(.*) *([^pl ])( pl)? *$",defs[0])
    entrada = {}
    if result: 
        entrada = parse_completa(result)
    else:
        parse_remissivas(defs,result)
        continue
    traducoes = {}
    categoria = []
    index = 1
    while not any(x in defs[index] for x in ["SIN","VAR","@@@"]):
        for elem in defs[index].split(" "):
            if elem:
                if elem[0].isupper():
                    categoria.append(elem)
                else:
                    categoria[-1] += " " + elem
        index +=1
    entrada["categoria"] = categoria
    while index < len(defs) :
        l = []
        if result:= re.match(r"@@@(.*)",defs[index]):
            lang = result.group(1) 
            index +=1
            while result:= re.match(r"-(.*)",defs[index]):
                l.append(result.group(1))
                index +=1
            traducoes[lang] = l
            continue
        elif result:= re.match(r" *SIN.-(.*)",defs[index]):
            entrada["sinonimos"] = result.group(1).strip().split(";")
        elif result:= re.match(r" *VAR.-(.*)",defs[index]):
            entrada["variacoes"] = result.group(1).strip().split(";")
        elif result:= re.match(r" *Nota.-?(.*)",defs[index]):
            entrada["nota"] = result.group(1).strip()
        else:
            if defs[index].strip():
                print(f"{defs[0]}-N??o encontrado: " + "".join(defs[index]))
        index +=1
    if traducoes:
        entrada["traducoes"] = traducoes


# def completas_dict():
#     for k,v in d.items():
#         completas[v["nome"]] = k


# def link_remissivas():
#     for k,v in d.items():
#         if "remissivas" in v:
#             for remissiva in v["remissivas"]:
#                 for k2,v2 in remissiva.items():
#                     if v2 in completas:
#                         remissiva[k2] = (completas[v2],v2)
#                     else:
#                         print("Remissiva n??o encontrada: ")
#                         print(k,k2,v2)

#completas_dict()
#link_remissivas()


d = {"completas": completas, "remissivas": remissivas}

def stats():
    l = len(completas)
    r = len(remissivas)
    total = l + r
    print("Total de completas: " + str(l))
    print("Total de remissivas: " + str(r))
    print("Total de entradas: " + str(total))

stats()


def check_if_all_defs_exist():
    for i in range(1,5393):
        if i not in completas:
            print("Missing def: " + str(i))


#check_if_all_defs_exist()

import json

def writeJson():
    with open('medicina.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

writeJson()

while True:
    print("Enter a number to search for a definition: ")
    n = input()
    if n == "exit":
        break
    if int(n) in completas:
        print(completas[int(n)])
    else:
        print("Definition not found")