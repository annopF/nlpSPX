import time
from transformers import logging

def getCandidate(sentence,maskedSentence,classifier):

    logging.set_verbosity_error()


    cat = sentence+" "+maskedSentence

    res = classifier(cat)


    predictedList = []
    for i in range(len(res)):
        predictedList.append(res[i]["token_str"].strip())

    return predictedList

