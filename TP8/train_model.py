# type: ignore
from gensim.models import Word2Vec  
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import re

#sentences = [[ 'this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec' ],
#             [ 'this', 'is', 'the', 'second', 'sentence' ],
#             [ 'yet', 'another', 'sentence' ],
#             [ 'one', 'more', 'sentence' ],
#             [ 'and', 'the', 'final', 'sentence' ]]



def tokenize_file(filename):
    txt =""


    with open(filename, "r") as f:
        txt = f.read()


    stop_w = stopwords.words('portuguese')
    #tokenize sentences
    sentences = sent_tokenize(txt)

    punct = list(string.punctuation) + ['\n',"—" ,"–","..."]
    str_punct = "".join(punct)

    data = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word.lower() for word in words]
        array = []
        for word in words:
            if word not in stop_w and word not in punct :
                #word = re.sub(rf'[{str_punct}]','',word)
                array.append(word)
        data.append(array)
    return data

def train_model(data, output):
    model = Word2Vec(data, vector_size=300, window=5, min_count=1,sg=1,epochs=5, workers=3)
    model.save(output)
    return model


import os 

def tokenize_dir(dir_name):
    data = []
    for file in os.listdir(dir_name):
        data += tokenize_file(f"{dir_name}/{file}")
        print(len (data))
    return data


def train_books(dir):
    data = tokenize_dir(dir)
    with open("data.txt", "w") as f:
        f.write(str(data))
    model = train_model(data, "models/livros.model")
    return model




import sys

if len (sys.argv) != 2:
    print("Usage: python3 aula.py <dir>")
    exit(1)
else:
    dir = sys.argv[1]

train_books(dir)

