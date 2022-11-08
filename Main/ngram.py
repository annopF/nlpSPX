import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
import spacy
from tokenizer import tokenizerX, selectTokenizer

#global

exclude = ["is","am","are","was","were",".","the","a","an","to","this","that","there"]
repeat = {}

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


def showList(list):
    for i in range(len(list)):
        print(list[i])


def bigram(mode, num, tok):
    
    finder = BigramCollocationFinder.from_words(tok)

    finder.apply_freq_filter(3)
    score =  finder.score_ngrams(bigram_measures.pmi)
    nbest =  finder.nbest(bigram_measures.pmi,num)
    if mode == "sc":
        showList(score)
    elif mode == "nb":
        showList(nbest)


def trigram(mode, num, tok):

    finder = TrigramCollocationFinder.from_words(tok)

    finder.apply_freq_filter(3)
    score =  finder.score_ngrams(trigram_measures.pmi)
    nbest =  finder.nbest(trigram_measures.pmi,num)
    if mode == "sc":
        showList(score)
    elif mode == "nb":
        showList(nbest)


def unigram(tok):
    repeat = {}
    for word in tok:
        if word not in exclude:
            if word not in repeat:
                repeat[word]=0
            repeat[word]+=1
    
    res = [(a,b) for a,b in repeat.items()]
    res_list = sorted(res,key=lambda x:x[1], reverse=True)
    showList(res_list[0:10])

