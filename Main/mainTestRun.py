from tokenizer import *
from ngram import *
from util import *

#change data to sampletext to get a longer text
input = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/sampletext.txt",encoding="UTF-8").read() 

#tokenize text
tok = selectTokenizer("regxUltra",input)
print("***tok*** ",tok)



#get unigram bigram trigram from text
unigram(20,tok)
print("------------------------------")
bigram("nb",None,tok)
print("------------------------------")

trigram("nb",None,tok)

""" #Named engitiy recognition
tok2 = selectTokenizer("spaBasic_Doc",input)

for item in tok2:
    if item.ent_type_:
        print(item, item.ent_type_)
print("--------------------------------------------")
for item in tok:
    if item.ent_type_:
        print(item, item.ent_type_) """