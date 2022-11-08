import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
from nltk.corpus import stopwords


print (stopwords)

text0 = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/simpleTest.txt",encoding="UTF-8").read() 

text2 = "rer weor sd aw eiafj saoiefj  sao df a8ief sdi adkjfoa fas8d fsifa sod 8adjf0a dia da sd0 fje0a9 sdifj apsd pf adf"
text = "I do not like green eggs and ham, I do not like them Sam I am!"


bigram_measures = nltk.collocations.BigramAssocMeasures()

tokens = nltk.word_tokenize(text0)
finder = BigramCollocationFinder.from_words(tokens)
scored = finder.score_ngrams(bigram_measures.raw_freq)
print(sorted(bigram for bigram, score in scored))
