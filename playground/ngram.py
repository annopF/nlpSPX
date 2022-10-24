import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
import spacy
#global
input = open("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/ieltsText/ie10.txt",encoding="UTF-8").read()

exclude = ["is","am","are","was","were",".","the","a","an","to","this","that","there"]
repeat = {}

def selectTokenizer(name):
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
        case "spa":
            print("-------------------------------------------------using spacy tokenizer")
            nlp = spacy.load("en_core_web_sm")
            return([x.text for x in nlp(input)])
            



def showList(list):
    for i in range(len(list)):
        print(list[i])


def bigram(mode, num):
    
    finder = BigramCollocationFinder.from_words(tok)

    finder.apply_freq_filter(3)
    score =  finder.score_ngrams(bigram_measures.raw_freq)
    nbest =  finder.nbest(bigram_measures.pmi,num)
    if mode == "sc":
        showList(score)
    elif mode == "nb":
        showList(nbest)


def trigram(mode, num):

    finder = TrigramCollocationFinder.from_words(tok)

    finder.apply_freq_filter(3)
    score =  finder.score_ngrams(trigram_measures.raw_freq)
    nbest =  finder.nbest(trigram_measures.pmi,num)
    if mode == "sc":
        showList(score)
    elif mode == "nb":
        showList(nbest)


def unigram():
    repeat = {}
    for word in tok:
        if word not in exclude:
            if word not in repeat:
                repeat[word]=0
            repeat[word]+=1
    
    res = [(a,b) for a,b in repeat.items()]
    res_list = sorted(res,key=lambda x:x[1], reverse=True)
    showList(res_list[0:10])

tok = selectTokenizer("wsp")

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

unigram()
print("------------------------------")
bigram("sc",None)
print("------------------------------")

trigram("sc",None)