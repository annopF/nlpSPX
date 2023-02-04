import spacy
from nltk.corpus import wordnet
from Putil import cleanDup 
from lemminflect import getAllInflections
from nltk import word_tokenize, pos_tag

nlp = spacy.load('en_core_web_lg') # just keep tagger for lemmatization

def getMorph(maskedSentence, candidateList):

    morphList = []

    for word in candidateList:
        doc = nlp(maskedSentence.replace("<mask>", word))
        for token in doc:
            if str(token) == word:

                morphList.append([word,str(token.tag_)])
    
   
    for i in morphList:
        print(i)
    return (morphList)

def getMorphB(maskedSentence, candidateList):
    morphList = []
    for word in candidateList:
        doc = pos_tag(word_tokenize(maskedSentence.replace("<mask>",word)))
        for token in doc:
            if token[0] == word:
                morphList.append([word,token[1]])
    
    print(morphList)
    return(morphList)
        
def getMorphSingle(inputList):
    out = []
    for tokens in inputList:
        res = [token.morph for token in nlp(tokens)]
        out.append([tokens,str(res)])

    
    return (out)

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
    print ("INFLECTED: ",out)
   
    for item in out:
        target = item[0]
        if target not in final and target != word:
            final.append(target)

    
    return (cleanDup(final))

