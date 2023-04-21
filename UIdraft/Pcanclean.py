from Putil import levDistance, cleanDup
from PgetMorph import *
from Levenshtein import ratio
from itertools import combinations

#removes word with similar pos tag and morphology from the list
#arg1: morphList: list of tagged word [['autonom', 'NNS', 'NOUN'],['effortlessly', 'RB', 'ADV']]
#arg2: target: original word of the masked position
#return: ["safely",]

  
#[[["word":0.88],"VBD"],[["word":0.88],"VBD"]....]
def removeMorph(maskedSentence, candidateList):

  morphList = getMorph(maskedSentence, candidateList)
  print(morphList)
  out = []
  show = []

  for i, word in enumerate(morphList):
    originalForm = morphList[0][1]
    candidateForm = morphList[i][1]


    if originalForm == candidateForm:
      out.append(word[0])
      show.append([word])
      
  #print(show)
  return (out)
def checkLevRatio(wordList):
  out = {}
  
  all = combinations(wordList,2)
  

  print(list(all))

def levRatCheck(input):
    
    wordList = [x[0] for x in input ]
    dix = {}
    for i in wordList:
        
        related = getRelatedForm(i)
    
        print(i,related,len(related))
        
        if len(related) > 0:
            a= [x for x in related if ratio(i,x) > 0.78 and x != i and x in wordList] 
            if len(a) != 0:
                dix[i] = a
    print(dix)
    return dix

def deepCleanX(wordList):
    from PgetMorph import getAntonym, getRelatedForm
    word = wordList[0][0]
    #print("-----WORD-----",word)
    antonyms = getAntonym(word)
    #print("ANTONYM ", antonyms)
    relatedForm = getRelatedForm(word)
    print("x",relatedForm)
    #print("RELATED FORM ", relatedForm)
    derivedForm = getInflect(word)
    print("X",derivedForm)

    #print("-------*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*-------",wordList)
    out = [] 

    for item in wordList:
      a = item[0]
      if a not in antonyms and a not in relatedForm and a not in derivedForm:
        out.append(item)

   
    out.insert(0,wordList[0])

    levRatCheck(wordList)

    return (cleanDup(out))
   