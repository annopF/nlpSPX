from tokenizer import selectTokenizer
import spacy
from ngram import *

input = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/sampletext.txt",encoding="UTF-8").read() 


token = selectTokenizer("spaX",input)

nlp = spacy.load("en_core_web_trf")


cat = (" ".join(token))
punk = "./;\"'"
for i in token:
    if i in punk:
        token.remove(i)

bigram("sc",20,token)

