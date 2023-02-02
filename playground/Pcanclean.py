from Putil import levDistance, cleanDup
from PgetMorph import *
from Levenshtein import ratio

#removes word with similar pos tag and morphology from the list
#arg1: morphList: list of tagged word [['autonom', 'NNS', 'NOUN'],['effortlessly', 'RB', 'ADV']]
#arg2: target: original word of the masked position
#return: ["safely",]

  

def removeMorph(morphList):
  out = []
  show = []

  for i, word in enumerate(morphList):
    originalForm = morphList[0][1]
    candidateForm = morphList[i][1]

    if originalForm == candidateForm:
      out.append([word][0][0])
      show.append([word])
      
  print("************SHOW")
  for i in show:
    print(i)
  return (cleanDup(out))


def deepCleanX(wordList):
    from PgetMorph import getAntonym, getRelatedForm
    word = wordList[0]
    antonyms = getAntonym(word)
    print("ANTONYM ", antonyms)
    relatedForm = getRelatedForm(word)
    print("RELATED FORM ", relatedForm)
    derivedForm = getInflect(word)

    out = [] 
    for item in wordList:
      if item not in antonyms:
        out.append(item)

  
    for item in wordList:
      if ratio(word,item) > 0.876 and item !=word and item in out:
        print("Lev ratio ",item)
        out.remove(item)   
    
    for item in derivedForm:
      if item in out:
        out.remove(item)


    print("----------OUT ",out)        
    return (cleanDup(out))
   

  
