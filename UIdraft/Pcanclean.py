from Putil import levDistance, cleanDup
from PgetMorph import *
from Levenshtein import ratio

#removes word with similar pos tag and morphology from the list
#arg1: morphList: list of tagged word [['autonom', 'NNS', 'NOUN'],['effortlessly', 'RB', 'ADV']]
#arg2: target: original word of the masked position
#return: ["safely",]

  
#[[["word":0.88],"VBD"],[["word":0.88],"VBD"]....]
def removeMorph(maskedSentence, candidateList):

  morphList = getMorph(maskedSentence, candidateList)

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
  
  for i in wordList:
    li = []
    for j in wordList:
      r = ratio(i[0],j[0])
      if  r >= 0.80 and r != 1:
        li.append(j[0])

    if len(li) != 0:
      out[i[0]] = li

  print(out)
  
def deepCleanX(wordList):
    from PgetMorph import getAntonym, getRelatedForm
    word = wordList[0][0]
    #print("-----WORD-----",word)
    antonyms = getAntonym(word)
    #print("ANTONYM ", antonyms)
    relatedForm = getRelatedForm(word)
    #print("RELATED FORM ", relatedForm)
    derivedForm = getInflect(word)

    #print("-------*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*X*-------",wordList)
    out = [] 

    for item in wordList:
      a = item[0]
      if a not in antonyms and ratio(word,a) < 0.79 and a not in relatedForm and a not in derivedForm:
        out.append(item)

   
    out.insert(0,wordList[0])

    checkLevRatio(wordList)

    return (cleanDup(out))
   

  
