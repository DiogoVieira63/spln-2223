# TPC 2

The goal of this homework was to normalize the JSON from the previous homework, create a easier structure than JSON so regular people can  modify it, and do a grammar to parse it.

### Part 1 - JSON Normalization

First of all, we will normalize the JSON file from the previous homework (**medicina.json**).
The current structure of an entry is:

    {
        "nome": "abdución",
        "género": "f",
        "plural": "no",
        "indíce": "7",
        "categoria": [
            "Fisioloxía",
            "Anatomía"
        ],
        "sinonimos": [
            "separación"
        ],
        "nota": "Evítese “abducción”.",
        "traducoes": {
            " es ": [
                "abducción",
                "separación"
            ],
            " en ": [
                "abduction"
            ],
            " pt ": [
                "abdução",
                "separação"
            ],
            " la ": [
                "abductio"
            ]
        }
    }

This entry is too focused on galego, we want to make galego just another language. 
To make a more scalable structure,the goal is to defenie entry as follows:
    
    {
        atributos:{
            "categoria": [ "Anatomia" ],
            "indíce": "7"
        }
        linguas:{
            "es": [
                {
                    "palavra": "abducción",
                    atributos: {}
                }
            ]
        }
    }

First, we create the **galego**. All the categories that are related to the galego, instead of the term as a whole (these will be put on the main atributos list), will be put on the **atributos** (e.g.género,plural,nota).
The synonym will be treated as another word of **galego**.

Now, to all the words related each language, we will search for more attributes that were not taken into account previously.

The attributes can be one of five categories:

- **género**:
    - **f**: feminina
    - **m**: masculina
    - **s**: variação

- **multiplicidade**,:
    - **pl**: plural
    - singular

- **forma**:
    - **arc**: arcaica
    - **col**: coloquial
    - **pop**: popular
    - **cult**: culta
    - **lit**: literária
    - **loc**: locução
    - **ant**: antiga

- **representação**:
    - **abrev**: abreviatura
    - **sb**: símbolo
    - **sg**: sigla

- **origem linguística**:
    - **Pt**: Português de Portugal
    - **Br**: Portugues do Brasil
    - **EE. UU.**: Inglês dos EUA 

After this parsing, we have the structure ready to be written.

### Part 2 - New Structure

In this new structure, we want to make sure that everyone can edit it. So, it should be easy to understand.
At this point, we will only care about complete entries, all the remissives will be dealt with later.

This is an example of structure:

    ---
    _indíce: 7
    _categoria: [ Fisioloxía , Anatomía ]
    es: abducción
    es: separación
    en: abduction
    pt: abdução
    pt: separação
    la: abductio
    +nota: Evítese “abducción”.
    ga: abdución
    +género: feminino
    +multiplcidade: singular
    ga: separación

All the entries start with **"---"**.
All the attribites related to the term as a whole start with "**_**".
If there's no special character on the beginning of the line, then it's a translation.
All the attributes related to that translation, will be on the following lines and start with "**+**".
The resulting file is **medicina_completas.txt**

### Part 3 - Grammar

Now, we want to make a grammar able to parse this new structure.
It will be used **lark**, and the parsing wil be done on **grammar,py**.
This is the grammar to parse the new structure.

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

Most of the grammar was inspired by the one done in the class.
The rule for **WORD** was hard to come up with, and there's probably a more simpler way to do it. 
For the Transformer was created the class MedicinaTransform, that builds the dictionary with the terms.

The conversion from the structure back to a JSON is on **data.json**.












