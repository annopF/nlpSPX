import time
import pandas as pd
import ranky as rk
import torch
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
start = time.time()
from transformers import pipeline 
from transformers import RobertaForMaskedLM, RobertaTokenizer
from sentence_transformers import CrossEncoder
from PtestFillMask import *
from Pcanclean import *
from Pscorer import *
from PgetMorph import *
from Putil import *
from Pparse import runParse

end = time.time()
print("(Import) Elapsed time: ", end - start, "DELTA T=", 8.1634-(end-start), "Avg. loading time= 8.1634")
use = "cpu"
print("preparing SentenceTransformers")
lmv6  = SentenceTransformer("sentence-transformers/stsb-roberta-base-v2", device = use)
mnli  = SentenceTransformer("textattack/roberta-base-MNLI", device = use)
dbt = CrossEncoder('cross-encoder/nli-roberta-base', device=use)

def rankAll(a,b,c,d):

    #print(a)
    dick = dict.fromkeys([x[0] for x in a])

    #print(dick)
    temp = []
    for word in dick:
        #for i,(a,b,c) in enumerate(zip(roberta,mnli,distil)):
        temp.append([word, [[x[0] for x in a].index(word), 
                            [x[0] for x in b].index(word), 
                            [x[0] for x in c].index(word), 
                            [x[0] for x in d].index(word)]])

    #print(temp)
    for word in dick:
        for item in temp:
            if item[0] == word:
                dick[word] = item[1]

    df = pd.DataFrame.from_dict(dick, orient="index")
    out = rk.borda(df, reverse=True, axis=1)
    out.to_dict()

    return(sorted([[key, value] for key, value in out.items()], key=lambda x: x[1], reverse=False)) # !REVERSE MUST BE FALSE!

def loadClassifier(MAX):

    print("Loading classifier...")

    #Cmodel = RobertaForMaskedLM.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
    #Ctokenizer = RobertaTokenizer.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
    return (pipeline("fill-mask", model = "roberta-base", top_k=MAX, framework="pt", device = -1))
classifier = loadClassifier(20)

print("(Classifier) Elapsed time: ", end - start, "DELTA T=", 15-(end-start))


def generateData(mode,parseMode):
    testData = [["Apple, Inc. is founded by Steve Job.", "Apple, Inc. is <mask> by Steve Job.", "founded"],
                ["Apple, Inc. is founded by Steve Job.", "Apple Inc is <mask> by Steve Job", "founded"],
                ["x"]
                ]
    if mode == 1:
        return(testData)
    else:
        return(runParse(parseMode))

while True:
    choice = int(input("choose mode: 2=from list(no concat), 1=from list, 0=manual, -1=quit"))
    if choice == -1:
        print("***** ENDED *****")
        exit()
    mode = int(input("which gram?: 1=unigram, 2=bigram, 3=trigram"))
    testData = generateData(0,mode) 

    if choice == 0:
        inp = str(input("type sentence with <mask>"))

    elif choice == 2:
        print("*-*-*-*-*-*-*-*-* USING No concat method *-*-*-*-*-*-*-*-*")
        for item in testData:
            candidate_noConcat = fillNextWord(item[1],classifier, 5)
            for can in candidate_noConcat:
                print(item[1].replace("<mask>",can[0]))
    else:
        print("*-*-*-*-*-*-*-*-* USING OG method *-*-*-*-*-*-*-*-*")

        for i,item in enumerate(testData):
            sentence = item[0]
            
            if sentence == "x":
                print("'EOL REACHED' Terminated")
                break

            else:
                maskedSentence = item[1]
                word = item[2]
            

                candidate = getCandidate(sentence, maskedSentence, classifier, word)
                
                removedMorph = removeMorph(maskedSentence, candidate) 
                deepClean = deepCleanX(removedMorph)  

                cleanedMorph = removeMorph(maskedSentence, candidate)
                deepCleans = deepCleanX(cleanedMorph)
                deepClean = [x[0] for x in deepCleans]

                #print("DEEPCLEAN X", deepClean)
                limit = 25
                ST_outputMNLI = sentenceSimilarity(maskedSentence, deepClean, model=mnli,mode=0)
                ST_outputLMV6 = sentenceSimilarity(maskedSentence, deepClean, model=lmv6,mode=0)
                entail = entailment(maskedSentence, deepClean, model1=mnli, model2=dbt)
                rerank = rankAll(deepCleans,ST_outputMNLI,ST_outputLMV6,entail)
        
                data = {
                        "OG rank": deepCleans[:limit],
                        "ST MNLI": ST_outputMNLI[:limit],
                        "ST LMV6": ST_outputLMV6[:limit],
                        "Entailment_score": entail[:limit],
                        "rerank": rerank[:limit]}          
                df = pd.DataFrame(data)
                print(df) 
                print(">>>> OG SEN:",sentence)
                print(">>>> MASKED WORD:",word)
                print(">>>> MASKED SEN:",maskedSentence)



                print("------------------------------------------------------------------------------------------------------------------------------------------------------------")        