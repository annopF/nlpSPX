#THIS IS TOKENIZER 
#USING SPACY
import spacy
from spacy.symbols import ORTH
import re
import time
import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *


def tokenizerX(input):
    nlp = spacy.load("en_core_web_trf")
    contraction = ["I'd","I'll","I've","I'm","She'd","She'll","They",
        "They're","They've","We'd","We'll","We're","It's","It'll","That's","There's","Where's",
        "Let's","Can't","Couldn't","Didn't","Doesn't","Don't","Hadn't","Hasn't","Isn't","Shouldn't",
        "Wasn't","Won't","Wouldn't","Could've","Might've","Must've","Should've","Would've","Ain't"] 

    for ex in contraction:
        nlp.tokenizer.add_special_case(ex,[{ORTH:ex}])
        nlp.tokenizer.add_special_case(ex.lower(),[{ORTH:ex.lower()}])

        
    infix_re = re.compile(r"(\w+-)+\w+")

    nlp.tokenizer.infix_finditer = infix_re.finditer
    #start = time.time()
    doc = nlp(input)
    return doc


def selectTokenizer(name, input):
    match name:
        case "w": 
            print("-------------------------------------------------using word tokenizer")
            return (nltk.word_tokenize(input))
        case "wsp": 
            print("-------------------------------------------------using whitesapce tokenizer")
            return (input.split())
        case "pun":
            print("-------------------------------------------------using punctuation tokenizer")
            return (nltk.wordpunct_tokenize(input))
        case "reg":
            print("-------------------------------------------------using regex tokenizer")
            return (nltk.regexp_tokenize(input,"\w+"))
        case "spaBasic":
            print("-------------------------------------------------using spacy tokenizer")
            nlp = spacy.load("en_core_web_trf")
            return([x.text for x in nlp(input)])
        case "spaBasic_Doc":
            print("-------------------------------------------------using spacy tokenizer")
            nlp = spacy.load("en_core_web_trf")
            return nlp(input)
        
        case "spaX":
            return([x.text for x in tokenizerX(input)])
    
        