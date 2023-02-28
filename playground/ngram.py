import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
from collections import Counter
from util import *

#initialize nltk assoc measure
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

#just loop and print
def showList(list):
    for i in range(len(list)):
        print(list[i])

#find and count bigrams in text
def bigram(num, tok):
    finder = BigramCollocationFinder.from_words(tok) #call bigramFinder from nltk library
    finder.apply_freq_filter(3) #filter out anything less than 3 occurrenees
    bg_rf =  finder.score_ngrams(bigram_measures.raw_freq) #use raw frequency as a measurement score
    fdist = nltk.FreqDist(bigrams(tok)) #count frequency of each bigram
    bg_ct_toList= [(k,v) for k,v in fdist.items()] #convert fdist(frequency distribution of ngram) to list
    bg_ct = (sorted(bg_ct_toList, key=lambda x:x[1], reverse=True))[:num] #sort frequency in deceending order
    return (bg_ct)
    

def trigram(num, tok):

    finderT = TrigramCollocationFinder.from_words(tok)
    finderT.apply_freq_filter(3)
    tg_rf =  finderT.score_ngrams(trigram_measures.raw_freq)
    fdist = nltk.FreqDist(trigrams(tok))
    tg_ct_toList= [(k,v) for k,v in fdist.items()]
    tg_ct = (sorted(tg_ct_toList, key=lambda x:x[1], reverse=True))[:num] 
    return(tg_ct)

def unigram(max,tok):
    clean = cleanToken(tok) #remove common word such as I you we were was is are etc.
    
    count = Counter(clean) #count frequency

    res = list(sorted(count.items(), key = lambda t: t[1], reverse=True))[:max] #sort frequency in descending order
    return (res)   