from tokenizer import selectTokenizer
import spacy
import textract as tt
from ngram import *
from Putil import nicePrint
print("start")
nlp = spacy.load("en_core_web_lg")
print("done")

class sentenceObj():
    doc = None
    def __init__(self, sentence):
        self.sentence = sentence
        
    @classmethod
    def createDocObject(self):
        doc = nlp(self.sent_str.replace("\n"," ").replace("\r",""))
        return (doc)
    
    def createTok(self):
        tok = selectTokenizer("wsp",self.sentence)
        return (tok)

    def 






sentPro = sentenceObj("p")
sentPro.sent_str = "i like apple. I like banaan. I like orange."

print(sentPro.sent_str)