# type: ignore
from gensim.models import Word2Vec  
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string


def load_model(filename):
    model = Word2Vec.load(filename)
    return model

import sys

if len (sys.argv) != 2:
    print("Usage: python3 aula.py <model>")
    exit(1)
else:
    model_path = sys.argv[1]

model = load_model(model_path)

#print(model.wv.most_similar(positive=["harry"],topn=10))



with open("analogias.txt", "r") as f:
    data = f.read()

for line in data.split("\n"):
    words = line.split(" ")
    if len (words) == 3:
        print(model.wv.most_similar(positive=[words[0],words[2]],negative=[words[1]],topn=10))


"""
with open("similares.txt", "r") as f:
    data = f.read()

for line in data.split("\n"):
    words = line.split(" ")
    if len (words) == 3:
        first = model.wv.similarity(words[0],words[1])
        second = model.wv.similarity(words[0],words[2])
        print(f"{words[0]} {words[1]} {first}")
        print(f"{words[0]} {words[2]} {second}")



with open("odd_one.txt", "r") as f:
    data = f.read()

for line in data.split("\n"):
    words = line.split(" ")
    odd = model.wv.doesnt_match(words)
    print(f"{words} {odd}")

"""