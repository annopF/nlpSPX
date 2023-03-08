import spacy
import textract as tt
from termcolor import colored, cprint
from spacy.matcher import Matcher
from tokenizer import selectTokenizer
from ngram import bigram, trigram, unigram
import re
# from Putil import nicePrint
import niceprint


def scantexts(inputtext):
    # change file path here
    # filepath = "C:/Users/thana/Documents/GitHub/nlpSPX/UIdraft/textdata/never.pdf"
    # text = tt.process(filepath)
    # text = inputtext.decode("utf8")
    text = inputtext
    nlp = spacy.load("en_core_web_lg")

    doc = nlp(text.replace("\n", " ").replace("\r", ""))
    toks = selectTokenizer("regxUltra", str(doc))            # all words' here
    topwords = unigram(10, toks)

    # for i in ngram:
    #     print(i)

    return toks, topwords


# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
