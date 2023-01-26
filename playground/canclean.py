import spacy
from spacy.morphology import Morphology



def cleanAll(inputList):
  nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) # just keep tagger for lemmatization

  def removeDup():
    return list(dict.fromkeys([x.lower() for x in inputList]))

  def removeMorph(morphList):
    morphForm = [item[1] for item in morphList]
    out = []
    for i in range(len(morphList)):
      if morphForm[i] == morphForm[0]:
        print("MORPH LIST [i]: ",morphList[i])
        out.append(morphList[i][0])
    return (out)

  def lemmatizer():
    out  =[]
    for tokens in inputList:
      out.append(" ".join([token.lemma_ for token in nlp(tokens)]))
    return out

  def morphAll():
    out = []
    for tokens in inputList:
        res = [token.morph for token in nlp(tokens)]
        out.append([tokens,str(res)])
    return (out)

  inputList = removeDup()
  
  return (removeMorph(morphAll()))

   