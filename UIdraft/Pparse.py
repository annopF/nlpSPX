import spacy
import sys 
sys.path.append("./playground")
from tokenizer import *
from ngram import *


def scantexts(inputtext):
    # change file path here
    # filepath = "C:/Users/thana/Documents/GitHub/nlpSPX/UIdraft/textdata/never.pdf"
    # text = tt.process(filepath)
    # text = inputtext.decode("utf8")
    text = inputtext
    nlp = spacy.load("en_core_web_lg")

    doc = nlp(text.replace("\n", " ").replace("\r", ""))
    toks = selectTokenizer("wsp", str(doc))            # all words' here
    gram = createNgram(80, toks.returnList())
    ug = gram.unigram()
    bg = gram.bigram()
    tg = gram.trigram()
        # for i in ngram:
    #     print(i)
    topwords = [(x.gram1+" "+x.gram2,x.count) for x in bg]
    return toks, topwords


# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
