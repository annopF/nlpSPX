import spacy
from spacy.tokenizer import Tokenizer

text0 = open("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/testPro.txt",encoding="UTF-8").read()

""" 

nlp = spacy.load("en_core_web_sm")
doc = (nlp(text0)) """

li = [x.text for x in spacy.load("en_core_web_sm")(text0)]

print(li)

