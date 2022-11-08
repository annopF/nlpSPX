from tokenizer import *
from ngram import *
from util import *

input = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/simpletext.txt",encoding="UTF-8").read() 

#tokenize text
tok = selectTokenizer("spaX",input)
print("***tok*** ",tok)

#clean fullstop and apostrophe for now (more in the future)
clean = cleanToken(tok)
print("***CLEAN*** ",clean)

#get unigram bigram trigram from text
unigram(clean)
print("------------------------------")
bigram("nb",None,clean)
print("------------------------------")

trigram("nb",None,clean)

#Named engitiy recognition
tok2 = selectTokenizer("spaBasic_Doc",input)

for item in tok2:
    if item.ent_type_:
        print(item, item.ent_type_)
