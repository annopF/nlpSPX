from tokenizer import selectTokenizer
import spacy
from ngram import *
import matplotlib.pyplot as plt


def cleanToken(token):
    punk = ".,'()?!"
    for i in token:
        if i in punk:
            token.remove(i)

    return token


def cat(token):
    return (" ".join(token))

def convertToDocObject(input):
    nlp = spacy.load("en_core_web_trf")
    return (nlp(cat(input)))

def plotFreq():
    fig, plot = plt.subplots()


    plot.barh(y_pos,word_count)
    plot.set_yticks(y_pos)
    plot.set_yticklabels(vocab)
    plot.invert_yaxis()  # labels read top-to-bottom
    plot.set_xlabel('occurrence')
    plot.set_ylabel('vocab')

    plot.set_title("Most repeated words in the document")


    plt.show()