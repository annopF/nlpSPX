import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *
from collections import Counter
from Putil import isStopword, cleanToken

class ngram():
    def __init__(self, gram1, gram2, gram3, count):
        self.gram1 = gram1
        self.gram2 = gram2
        self.gram3 = gram3
        self.count = count
        
    
class unigram(ngram):
    def __init__(self,gram1, count):
        super().__init__(gram1,None, None, count)
        self.concat = gram1
       
class bigram(ngram):
    def __init__(self,gram1, gram2, count):
        super().__init__(gram1, gram2, None, count)
        self.concat = gram1+" "+gram2
      
 
class trigram(ngram):
    def __init__(self,gram1, gram2, gram3, count):
        super().__init__(gram1, gram2,gram3, count)
        self.concat = gram1+" "+gram2+" "+gram3
       
   
class createNgram():
    

    def __init__(self,num,tok):
        self.num  = num
        self.tok = tok
       
    #find and count bigrams in text
    
    def bigram(self):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.tok) #call bigramFinder from nltk library
        finder.apply_freq_filter(3) #filter out anything less than 3 occurrenees
        bg_rf =  finder.score_ngrams(bigram_measures.raw_freq) #use raw frequency as a measurement score
        fdist = nltk.FreqDist(bigrams(self.tok)) #count frequency of each bigram
        bg_ct_toList= [(k,v) for k,v in fdist.items()] #convert fdist(frequency distribution of ngram) to list
        bg_ct = (sorted(bg_ct_toList, key=lambda x:x[1], reverse=True)) #sort frequency in deceending order
        return ([bigram(item[0][0],item[0][1],fdist[item[0]]) for item in bg_rf][:self.num])             
        
    
    def trigram(self):
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finderT = TrigramCollocationFinder.from_words(self.tok)
        finderT.apply_freq_filter(3)
        tg_rf =  finderT.score_ngrams(trigram_measures.likelihood_ratio)
        fdist = nltk.FreqDist(trigrams(self.tok))
        tg_ct_toList= [(k,v) for k,v in fdist.items()]
        tg_ct = (sorted(tg_ct_toList, key=lambda x:x[1], reverse=True))[:self.num] 
        return ([trigram(item[0][0],item[0][1],item[0][2],fdist[item[0]]) for item in tg_rf][:self.num])             

    def unigram(self):
        clean = cleanToken(self.tok) #remove common word such as I you we were was is are etc.
        
        count = Counter(clean) #count frequency

        res = list(sorted(count.items(), key = lambda t: t[1], reverse=True))[:self.num] #sort frequency in descending order
        return ([unigram(word,count) for (word, count) in res.items()])   
    
    #just loop and print
    def showList(self, mode):
        if mode == "all":
            for item in self.ngramList:
                print(item.gram1, item.gram2, item.count)
                

        if mode == "some":
            for item in self.ngramList:
                
                if isStopword(item.gram1) == 0 or isStopword(item.gram2)==0:

                    print(item.gram1, item.gram2)

  