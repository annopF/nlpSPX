from sentence_transformers import SentenceTransformer,CrossEncoder
from sentence_transformers import util

import time
import json
import networkx as nx
import matplotlib.pyplot as plt


raw = open("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/words_map.json")
data = json.load(raw)
G = nx.DiGraph()
inDegWeight = 1
outDegWeight = 1

#INPUT Type: list, Shape: ["word0","word1","word2"]
#OUTPUT Type: dict(unsorted), Shape: {"word0: 0.66", "word1": 0.89}
#DESC: Get input list, substitute <mask>, and calculate sentenece similarity.
#      This function convert input list to dictionary -> {"word":score}
def sentenceSimilarity(maskedSentence, inputList, model, mode):
    
    
    sentenceList = [maskedSentence.replace("<mask>", word) for word in inputList ]

    

    #Compute embedding for both lists

    start = time.time()
    
    embeddings = (model.encode(sentenceList, convert_to_tensor=True))
    

    
    ##print("embd1 size=",embeddings1.size())
    #score = []
    score = {}
    #Compute cosine-similarities
    for i, word in enumerate(inputList):
        cosine_scores = util.cos_sim(embeddings[0], embeddings[i])
        #score.append([word, cosine_scores.flatten().tolist()])
        score[word]=round(cosine_scores.flatten().tolist()[0],6)
        #if log == 1:
            #print("#",i," ", sentenceList[0], " <--> ", sentenceList[i], cosine_scores)

    end = time.time()
    print("elapsed time:", end - start)
    if mode ==1:
        return (score)
    elif mode ==0:
        return(sorted([[key,value] for key, value in score.items()], key= lambda x: x[1], reverse=True))
    #sorted(score, key=lambda x:x[1], reverse=True)


def entailment(maskedSentence, inputList, model1, model2):

    fromSentenceSim = sentenceSimilarity(maskedSentence, inputList, model=model1, mode=1)

    inputList = [key for key in fromSentenceSim]
    for i, word in enumerate(inputList):

        ogSen = maskedSentence.replace("<mask>",inputList[0])
        targetSen = maskedSentence.replace("<mask>",inputList[i])

        entail_score = model2.predict([(ogSen, targetSen)])
        
        #Convert scores to labels
        labels = [score_max for score_max in entail_score.argmax(axis=1)]
     
        if labels[0] == 0:
            fromSentenceSim[word] -= entail_score.flatten()[labels[0]]
        else:
            fromSentenceSim[word] += entail_score.flatten()[labels[0]]


    return(sorted([[key,value] for key, value in fromSentenceSim.items()], key= lambda x: x[1], reverse=True))
