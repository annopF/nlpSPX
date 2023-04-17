import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
from collections import Counter
from ngram import *
from Putil import isStopword, cleanToken

def createBigram(tok,num):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tok) #call bigramFinder from nltk library
    finder.apply_freq_filter(3) #filter out anything less than n occurrenees
    bg_rf =  finder.score_ngrams(bigram_measures.raw_freq) #use raw frequency as a measurement score
    fdist = nltk.FreqDist(bigrams(tok)) #count frequency of each bigram
    bg_ct_toList= [(k,v) for k,v in fdist.items()] #convert fdist(frequency distribution of ngram) to list
    #bg_ct = (sorted(bg_ct_toList, key=lambda x:x[1], reverse=True)) #sort frequency in deceending order
    return ([bigram(item[0][0],item[0][1],fdist[item[0]]) for item in bg_rf][:num])             
    

def createTrigram(tok,num):
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finderT = TrigramCollocationFinder.from_words(tok)
    finderT.apply_freq_filter(3)
    tg_rf =  finderT.score_ngrams(trigram_measures.likelihood_ratio)
    fdist = nltk.FreqDist(trigrams(tok))
    tg_ct_toList= [(k,v) for k,v in fdist.items()]
    #tg_ct = (sorted(tg_ct_toList, key=lambda x:x[1], reverse=True))[:num] 
    return ([trigram(item[0][0],item[0][1],item[0][2],fdist[item[0]]) for item in tg_rf][:num])             


def createUnigram(tok,num):
    clean = cleanToken(tok) #remove common word such as I you we were was is are etc.
    
    count = Counter(clean) #count frequency

    res = list(sorted(count.items(), key = lambda t: t[1], reverse=True))[:num] #sort frequency in descending order
    return ([unigram(word,count) for (word, count) in res])   
    

