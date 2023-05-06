#!/usr/bin/env python3

import sys
import fileinput
import re
text = ""

reserved = ["Sra","Sr","Prof","Srs","Sras"]


def reserved_words(input):
    global reserved
    reserved += input.split(",")
    reserved = [f"(?<!{x})" for x in reserved]

i = 1
while i < len(sys.argv): 
    arg = sys.argv[i]
    print(arg)
    if arg == "-r":
        reserved = []
        reserved_words(sys.argv[i+1])
        i+=1
    elif arg == "-ra":
        reserved_words(sys.argv[i+1])
        i+=1
    else:
        print("Argumento inválido:",sys.argv[i])
        exit()
    i+=1


print("Reserved words:",reserved)

for line in fileinput.input():
    text += line

# 0 Quebra de página ✅
# 1 Separar pontuação❓
# 2 Marcar Capítulos ✅
# 3 Separar por parágrafos ✅
# 4 Juntar linhas da mesma frase ✅
# 5 Uma frase por linha ✅




regex_cap =r".*(CAP[ÍI]TULO +\w+).*\n(.*)"

text = re.sub(regex_cap, r"\n# \1 - \2", text)

regex_nl = r"(.*)\n\n+(.*)"

text = re.sub(regex_nl, r"\1\n\2", text)

array_poema = []

def guarda_poema(match):
    array_poema.append(match.group(1))
    return f">>{(len(array_poema)-1)}<<"
    

regex_poema = r"<poema>(.*?)</poema>"
text = re.sub(regex_poema,guarda_poema, text,flags=re.S)


def remove_empty_lines(text):
    return re.sub(r"^\s*\n","", text, flags=re.MULTILINE)




regex_linha = fr"""(?<!\.){''.join(reserved)}\.(?!\.)"""


def getAverageSize(text):
    value = 0
    lines = text.split("\n")
    for line in lines:
        if len(line) > 0:
            value += len(line)
    return value/len(lines)

regex_par = r"(.*[!?.:])(?!\.\.)\n(?!#)"

average = getAverageSize(text)
MAX = average * 1.5 - average/10
#print(MAX)
def check_par(match):
    length = len(match.group(1))
    if length < MAX and length > 0:
        return match.group(1) + "\n\t"
    else:
        return match.group(1) + "\n"

text = re.sub(regex_par,check_par, text)


regex_merge_lines_par = r"\n([^\t#].*)\n"

text = re.sub(regex_merge_lines_par,r" \1 ", text)

text = re.sub(rf"(?<!\.){''.join(reserved)}([!?.:])(?![\n\.,]| [–\-])",r"\1\n", text)

#trim lines
text = re.sub(r"^ +","", text, flags=re.MULTILINE)


for i in range(len(array_poema)):
    text= re.sub(">>"+str(i)+"<<",f"<poema>{array_poema[i]}</poema>",text)

print(text)



