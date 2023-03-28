#!/usr/bin/env python3
"""Module to tokenize a text file into sentences."""

__version__ = "0.31"

import fileinput
import re
import sys

#Global variables

def display_error(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)



def load_reserved_words(config_file, lingua=""):
    dic_abrev = {}
    current = ""
    with open(config_file) as file:
        for line in file:
            if line[0].startswith("#"):
                current = line[1:].strip()
                if lingua == "":
                    lingua = current
                dic_abrev[current] = []
            else:
                if line.strip():
                    dic_abrev[current].append(line.strip())
    if lingua in dic_abrev:
        return dic_abrev[lingua]
    else:
        raise Exception(f"Language '{lingua}' not found on config file '{config_file}'.")

def reserved_words(reserved):
    return [f"(?<!{x})" for x in reserved]


# - 0 Quebra de página ✅
# - 1 Separar pontuação✅
# - 2 Marcar Capítulos ✅
#   - Titulo do capítulo na linha seguinte✅
#   - Keywords para procurar capítulos
# - 3 Separar por parágrafos ✅
# - 4 Juntar linhas da mesma frase ✅
# - 5 Uma frase por linha ✅



def mark_capitulos(text):
    regex_cap =r".*(CAP[ÍI]TULO +\w+).*\n(.*)"
    return re.sub(regex_cap, r"\n# \1 - \2", text, flags=re.IGNORECASE)

def remove_empty_lines(text):
    regex_nl = r"([a-z0-9,;])\n\n([a-z0-9,;])"
    return re.sub(regex_nl, r"\1\n\2", text)

array_poema = []

def guarda_poema(match):
    array_poema.append(match.group(1))
    return f">>{(len(array_poema)-1)}<<"
    

regex_poema = r"<poema>(.*?)</poema>"


def remove_empty_lines(text):
    return re.sub(r"^\s*\n","", text, flags=re.MULTILINE)




#regex_linha = fr"""(?<!\.){''.join(reserved)}\.(?!\.)"""


def getAverageSize(text):
    value = 0
    lines = text.split("\n")
    for line in lines:
        if len(line) > 0:
            value += len(line)
    return value/len(lines)

regex_par = r"(.*[!?.:])(?!\.\.)\n(?!#)"


MAX =0

def check_par(match):
    length = len(match.group(1))
    if length < MAX and length > 0:
        return match.group(1) + "\n\t"
    else:
        return match.group(1) + "\n"



regex_merge_lines_par = r"\n([^\t#].*)\n"


import argparse

def build_parser():
    parser = argparse.ArgumentParser(description='Tokenize a text file into sentences.')
    parser.add_argument('-l', '--language',help='Language of reserved words')
    parser.add_argument('-cr', '--config-reserved',help='Config file with reserved words', default="conf/abrev.txt")
    parser.add_argument('-i','--input',nargs="+", help='Input file')
    parser.add_argument('-o','--output', help='Output file')
    parser.add_argument("--chapter", help="Mark chapters", default="cap[ií]tulo")
    return parser


input_file = []
output_file = ""
reserved = ""


def parse_args(parser):
    args = parser.parse_args()
    global reserved
    if args.language:
        try:
            reserved = load_reserved_words(args.config_reserved,args.language)
        except Exception as e:
            display_error(e)
    else:
        reserved = load_reserved_words(args.config_reserved)
    reserved = reserved_words(reserved)
    global input_file
    global output_file

    if args.output:
        output_file = args.output

    if args.input:
        input_file = args.input
    else:
        display_error("No input file provided.")
    return args

def tokenizer():
    parser = build_parser()
    parse_args(parser)

    text= ""
    for line in fileinput.input(input_file):
        text += line
    text = re.sub(regex_poema,guarda_poema, text,flags=re.S)
    average = getAverageSize(text)
    global MAX
    MAX = average * 1.5 - average/10
    text = re.sub(regex_par,check_par, text)
    text = re.sub(regex_merge_lines_par,r" \1 ", text)
    print(reserved)
    text = re.sub(rf"(?<!\.){''.join(reserved)}([!?.:])(?![\n\.,]|[–\-])",r" \1 \n", text, flags=re.IGNORECASE) 
    text = re.sub(r"^ +","", text, flags=re.MULTILINE)
    for i in range(len(array_poema)):
        text= re.sub(">>"+str(i)+"<<",f"<poema>{array_poema[i]}</poema>\n",text)
    text = re.sub(r"\t","\n\t",text)
    if output_file == "":
        print(text)
    else:
        with open(output_file, "w") as file:
            file.write(text)

if __name__ == "__main__":
    tokenizer()
