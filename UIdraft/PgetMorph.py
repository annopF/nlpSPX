import spacy
from nltk.corpus import wordnet
from Putil import cleanDup 
from lemminflect import getAllInflections
from nltk import word_tokenize, pos_tag

nlp = spacy.load('en_core_web_lg') # just keep tagger for lemmatization

def getMorph(maskedSentence, candidateList):

    morphList = []
    for item in candidateList:
        word = item[0]
        doc = nlp(maskedSentence.replace("<mask>", word))
        for token in doc:
            if str(token) == word:

                morphList.append([item,str(token.tag_)])

    #print("---------******--------",morphList)
    return (morphList)

        

def getAntonym(word):

    antonyms = []
    for item in wordnet.synsets(word):
        for lm in item.lemmas():
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name())
    
    return (antonyms)

def getRelatedForm(word):
    forms = []
    for item in wordnet.synsets(word):
        for lm in item.lemmas():
            if lm.derivationally_related_forms():
                forms.append(str(lm.derivationally_related_forms()[0].name()))
    return (cleanDup(forms))

def getPertainym(word):
    pertains = []
    for item in wordnet.synsets(word):
        for lm in item.lemmas():
            if lm.derivationally_related_forms():
                pertains.append(str(lm.derivationally_related_forms()[0].name()))
    return (cleanDup(pertains))


def lemmatizer(input):

    doc = nlp(input)
    for token in doc:
        return token.lemma_

def getInflect(word):
    out = []
    final = []
    res = getAllInflections(word)

    for key, value in res.items():
        for item in value:
            out.append([item, key])
   
    for item in out:
        target = item[0]
        if target not in final and target != word:
            final.append(target)

    
    return (cleanDup(final))



