from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import time
import json
import networkx as nx
import matplotlib.pyplot as plt

raw = open("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/words_map.json")
data = json.load(raw)
G = nx.DiGraph()
#INPUT Type: list, Shape: ["word0","word1","word2"]
#OUTPUT Type: dict(unsorted), Shape: {"word0: 0.66", "word1": 0.89}
#DESC: Get input list, substitute <mask>, and calculate sentenece similarity.
#      This function convert input list to dictionary -> {"word":score}
def sentenceSimilarity(maskedSentence, inputList, selectedModel, log):
    
    def choosenModel(selectedModel):
        match selectedModel:
            case "roberta":
                return SentenceTransformer("sentence-transformers/stsb-roberta-base-v2", device = "cpu"  )
            case "lmv6":

                return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device = "cpu"  )

            case "disroberta":
                return SentenceTransformer("sentence-transformers/all-distilroberta-v1", device = "cpu" )
    sentenceList = [maskedSentence.replace("<mask>", word) for word in inputList ]
    
    #Compute embedding for both lists
    embeddings = choosenModel(selectedModel).encode(sentenceList, convert_to_tensor=True, batch_size=16)
    ##print("embd1 size=",embeddings1.size())
    #score = []
    score = {}
    #Compute cosine-similarities
    for i, word in enumerate(inputList):
        cosine_scores = util.cos_sim(embeddings[0], embeddings[i])
        #score.append([word, cosine_scores.flatten().tolist()])
        score[word]=round(cosine_scores.flatten().tolist()[0],4)
        if log == 1:
            print("#",i," ", sentenceList[0], " <--> ", sentenceList[i], cosine_scores)
    return (score)
    #sorted(score, key=lambda x:x[1], reverse=True)

#search through the list for any shared words 
#REVISED VERSION, FIXED infinite loop, FIXED recursion level issues 
def coSyn(inputList):

    inputListOG = inputList
    print("INPUT LIST:", inputList)

    for word in inputList:
        #print("--> WORD:", word)
        res = []

        G.add_node(word)
        for key, value in data.items():
            #print("  --> KEY:", key, "VALUE:", value)
            if key == word:
                for (key1, value1) in value.items():
                    #print("     --> KEY1: ", key1, "VALUE1:", value1)
                    if G.has_edge(key,key1):
                        return()

                    elif type(value1) != str and key1 in inputListOG and key1 != None:
                        G.add_edge(key,key1,weight=value1)
                        #print("      --> ADDED:", key, key1, value1)
                        res.append(key1)

                        
            
                        
                        
            
    #print("--------------end recursion--------------")
    return(coSyn(res))

#INPUT Type: dict, Shape: {"word0: 0.66", "word1": 0.89}
#OUTPUT Type: dict Shape: {"word0: 0.66", "word1": 0.89}
#DESC: Add score to the dict from sentenceSimilarity().
#      Score is the in_degree of each node(word in the input dict).
def crossSimilarity(inputList, maskedSentence, modelName, log):

    def updateScore(fromSentenceSim, nodeData):

        for word, score in fromSentenceSim.items():
            if word in nodeData:
                
                edgeScoreIn = nodeData[word][0] #nodeData shape {"word":[score_indegree, score_outdegree]}
                edgeScoreOut = nodeData[word][1]
                fromSentenceSim[word] = [["total=",score],["OG=",score],["in_deg=",0],["out_deg=",0]]

                if (type(edgeScoreIn) == float or type(edgeScoreIn) == int) and (type(edgeScoreOut) == float or type(edgeScoreOut) == int):

                    fromSentenceSim[word] = [["total=",score],["OG=",score],["in_deg=",edgeScoreIn],["out_deg=",edgeScoreOut]]
                    fromSentenceSim[word][0][1] += edgeScoreIn
                    fromSentenceSim[word][0][1] += edgeScoreOut


                fromSentenceSim[word]

        return (fromSentenceSim)

    def calNodeWeight(inputList):

        nodeData = {}
        for word in inputList:
            inDeg = G.in_degree(word, weight="weight")
            outDeg = G.out_degree(word, weight="weight")
            nodeData[word] = [inDeg, outDeg]
            
        return (nodeData)

    
    def calNodeDegree(inputList):
        nodeData = {}
        for word in inputList:
            inDeg = G.in_degree(word)
            outDeg = G.out_degree(word)
            nodeData[word] = (inDeg, outDeg)
           
        return (nodeData)
    
    pre = sentenceSimilarity(maskedSentence, inputList, modelName, log)
    coSyn(pre)

    result = calNodeDegree(inputList)
    edgeLabel = nx.get_edge_attributes(G,"weight")
    nx.draw_networkx(G, pos=nx.shell_layout(G),node_size=1000, font_size=7, font_color="white")

    nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G),edge_labels=edgeLabel, font_size=7, font_color="black")
    plt.axis("off")

    print("debug graph nodes")
    for i in G.nodes():
        print(i)
    plt.show() 
    G.clear()
    return( updateScore(pre, result))

        