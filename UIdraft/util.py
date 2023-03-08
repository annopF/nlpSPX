from tokenizer import selectTokenizer
from ngram import *
import numpy as np
import matplotlib.pyplot as plt
#clean token by removing words listed here
#return a list of cleaned tokenized text 
def cleanToken(token):
    stopword = ["Is","Am","Are","Was","Were","I","You","The","A","An","Of","Then","to"
    ,"As","That","It","My","This","There","So","Me","They","Do","Does","Did","Be","These",
    "Not","At","Have","Has","Had","Her","Or",""]
    stopwordLow = [x.lower() for x in stopword]
    
    return [x for x in token if x not in stopword and x not in stopwordLow]

def plotFreq(word_count,vocab):

    y_pos = np.arange(len(vocab))
    fig, plot = plt.subplots()


    plot.barh(y_pos,word_count)
    plot.set_yticks(y_pos)
    plot.set_yticklabels(vocab)
    plot.invert_yaxis()  # labels read top-to-bottom
    plot.set_xlabel('occurrence')
    plot.set_ylabel('vocab')

    plot.set_title("Most repeated words in the document")


    plt.show()

