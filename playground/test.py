from tokenizer import selectTokenizer
import spacy
import textract as tt
from ngram import *
from Putil import nicePrint

filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/pdfFile/f14.pdf"
text = tt.process(filePath)
texts = text.decode("utf8")


nlp = spacy.load("en_core_web_lg")

doc = nlp(texts.replace("\n"," ").replace("\r",""))
for token in doc:
    if token.ent_type_ != "":
        print(token.text, token.ent_type_)