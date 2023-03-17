import time
from transformers import logging
from transformers import pipeline
from Pcanclean import cleanDup



def getCandidate(sentence,maskedSentence,classifier,word):

    logging.set_verbosity_error()

    cat = sentence+"."+" "+maskedSentence
    res = classifier(cat)
    predictedList = {}
    
    for i,item in enumerate(res):
        predictedList[res[i]["token_str"].lower().strip()] = res[i]["score"]

    final = sorted([[key, value] for key,value in predictedList.items()], key=lambda x:x[1], reverse=True)

    final = cleanDup(final)
    for i,item in enumerate(final):
        if item[0] == word:
            final.pop(i)
    final.insert(0,[word,1.0])
    return(final)
        
def fillNextWord(maskedSentence, classifier,k):

    logging.set_verbosity_error()

    res = classifier(maskedSentence)
    predictedList = {}
    
    for i,item in enumerate(res):
        predictedList[res[i]["token_str"].lower().strip()] = res[i]["score"]

    final = sorted([[key, value] for key,value in predictedList.items()], key=lambda x:x[1], reverse=True)

    return (final[:k])





