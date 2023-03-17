import time
import pandas as pd
import ranky as rk
import torch
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
start = time.time()
import networkx as nx
from transformers import pipeline 
from transformers import RobertaForMaskedLM, RobertaTokenizer
import sentence_transformers
from sentence_transformers import CrossEncoder
from PtestFillMask import *
from Pcanclean import *
from Pscorer import *
from PgetMorph import *
from Putil import *
from Pparse import getPackage
end = time.time()
print("(Import) Elapsed time: ", end - start, "DELTA T=", 8.1634-(end-start))

print("preparing SentenceTransformers")
lmv6  = SentenceTransformer("sentence-transformers/stsb-roberta-base-v2", device = "cuda")
mnli  = SentenceTransformer("textattack/roberta-base-MNLI", device = "cuda")
dbt = CrossEncoder('cross-encoder/nli-roberta-base', device="cuda")

def rankAll(a,b,c,d):

    print(a)
    dick = dict.fromkeys([x[0] for x in a])

    print(dick)
    temp = []
    for word in dick:
        #for i,(a,b,c) in enumerate(zip(roberta,mnli,distil)):
        temp.append([word, [[x[0] for x in a].index(word), 
                            [x[0] for x in b].index(word), 
                            [x[0] for x in c].index(word), 
                            [x[0] for x in d].index(word)]])

    print(temp)
    for word in dick:
        for item in temp:
            if item[0] == word:
                dick[word] = item[1]

    df = pd.DataFrame.from_dict(dick, orient="index")
    out = rk.borda(df, reverse=True, axis=1)
    out.to_dict()

    return(sorted([[key, value] for key, value in out.items()], key=lambda x: x[1], reverse=False)) # !REVERSE MUST BE FALSE!

start1 = time.time()
print("Loading classifier...")

Cmodel = RobertaForMaskedLM.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
Ctokenizer = RobertaTokenizer.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
classifier = pipeline("fill-mask", model = Cmodel, tokenizer=Ctokenizer, top_k=70, framework="pt", device = -1)
end1 = time.time()

print("(Classifier) Elapsed time: ", end - start, "DELTA T=", 15-(end-start))
_testData = [["Apple, Inc. is founded by Steve Job.", "Apple, Inc. is <mask> by Steve Job.", "founded"],
            ["Apple, Inc. is founded by Steve Job.", "Apple Inc is <mask> by Steve Job", "founded"],
            ["x"]
            ]
testData = getPackage()
choice = int(input("choose mode: 2-from list(no concat), 1-from list, 0-manual"))
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
            print("----------->->->->->-----------GETTING CANDIDATE")
            print(candidate)
            removedMorph = removeMorph(maskedSentence, candidate) 
            deepClean = deepCleanX(removedMorph)  

            cleanedMorph = removeMorph(maskedSentence, candidate)
            deepCleans = deepCleanX(cleanedMorph)
            deepClean = [x[0] for x in deepCleans]

            #print("DEEPCLEAN X", deepClean)
            print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
            t = torch.cuda.get_device_properties(0).total_memory
            r = torch.cuda.memory_reserved(0)
            a = torch.cuda.memory_allocated(0)
            f = r-a  # free inside reserved
            print("TOTAL",t)
            print("ALLOCATED",r)
            print("RESERVED",a)
            print("FREE",f)
            print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
            ST_outputMNLI = sentenceSimilarity(maskedSentence, deepClean, model=mnli,mode=0)
            ST_outputLMV6 = sentenceSimilarity(maskedSentence, deepClean, model=lmv6,mode=0)
            entail = entailment(maskedSentence, deepClean, model1=mnli, model2=dbt)
            rerank = rankAll(deepCleans,ST_outputMNLI,ST_outputLMV6,entail)
            print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
            t = torch.cuda.get_device_properties(0).total_memory
            r = torch.cuda.memory_reserved(0)
            a = torch.cuda.memory_allocated(0)
            f = r-a  # free inside reserved
            print("TOTAL",t)
            print("ALLOCATED",r)
            print("RESERVED",a)
            print("FREE",f)
            print("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/")
            limit = 15
            data = {
                    "OG rank": deepCleans[:limit],
                    "ST MNLI": ST_outputMNLI[:limit],
                    "ST LMV6": ST_outputLMV6[:limit],
                    "Entailment_score": entail[:limit],
                    "rerank": rerank[:limit]}          
            df = pd.DataFrame(data)
            print(df) 
            print("SEN:",sentence,"WORD:",word)
            print("------------------------------------------------------------------------------------------------------------------------------------------------------------")        