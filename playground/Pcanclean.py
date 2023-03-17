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
      
  print(show)
  return (out)


def deepCleanX(wordList):
    from PgetMorph import getAntonym, getRelatedForm
    word = wordList[0][0]
    print("-----WORD-----",word)
    antonyms = getAntonym(word)
    print("ANTONYM ", antonyms)
    relatedForm = getRelatedForm(word)
    print("RELATED FORM ", relatedForm)
    derivedForm = getInflect(word)

    out = [] 
    for item in wordList:
      if item[0] not in antonyms:

        out.append(item)

  
    for item in wordList:
      if ratio(word,item[0]) >= 0.8 and item[0] !=word and item in out:
        out.remove(item)   
    
    for item in wordList:
      if item[0] in out:
        out.remove(item)

   
    return (cleanDup(out))
   

  
