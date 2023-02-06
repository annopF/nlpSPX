import time
import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)



start = time.time()
print("importing modules...")
print("-----importing netowrkx...")
import networkx as nx
print("-----importing transformers...")
from transformers import pipeline 
print("-----importing PtestFillMask...")
from PtestFillMask import *
print("-----importing Pcanclean...")
from Pcanclean import *
print("-----importing Pscorer...")
from Pscorer import *
print("-----importing PgetMorph...")
from PgetMorph import *
print("-----importing Putil...")
from Putil import *
end = time.time()
print("(Import) Elapsed time: ", end - start, "DELTA T=", 8.1634-(end-start))



start1 = time.time()
print("Loading classifier...")
classifier = pipeline("fill-mask", model = "roberta-base", top_k=50, batch_size = 8, framework="pt", device = -1)
end1 = time.time()

print("(Classifier) Elapsed time: ", end - start, "DELTA T=", 15-(end-start))
testData = [["Our project is about the application of machine translation","Our <mask> is about the application of machine translation","project"],
            ["The software is optimized for low-powered devices such as smartphone","The <mask> is optimized for low-powered devices such as smartphone","software"],
            ["Our approach is correct but my professor said it is not correct","Our approach is <mask> but my professor said it is not correct","correct"],
            ["The mask detecting software is optimized for surgical mask only","The <mask> detecting software is optimized for surgical mask only","mask"],
            ["Sodium Hydroxide is very sensitive to sunlight","Sodium Hydroxide is very <mask> to sunlight","sensitive"],
            ["Background removal is getting better with the help of artificial intelligence","Background <mask> is getting better with the help of artificial intelligence","removal"],
            ["This processor is made by Samsung Semiconductor","This <mask> is made by Samsung Semiconductor","processor"],
            ["I drive Tesla model X to London, but my friend drive MG XS","I <mask> Tesla model X to London, but my friend drive MG XS","drive"],
            ["This research is intended to help teachers in the classroom","This research is <mask> to help teachers in the classroom","intended"],
            ["I made this pasta with tuna cream sauce","I <mask> this pasta with tuna cream sauce","made"],
            ["Mr. John said our work need to be fixed","Mr. John <mask> our work need to be fixed","said"],
            ["Water pollution is one of the most studied topics","Water pollution is one of the most <mask> topics","studied"],
            ["Most of the professional grade software is not available online","Most of the professional grade software is not <mask> online","available"],
            ["Apple M2 Pro allows professional video editor to export faster","Apple M2 Pro allows <mask> video editor to export faster","professional"],
            ["Microsoft sponsored OpenAI which allows them to make Chat GPT project","Microsoft <mask> OpenAI which allows them to make Chat GPT project","sponsored"],
            ["x"]

            ]

for item in testData:

    sentence = item[0]
    if sentence == "x":
        print("'EOL REACHED' Terminated")
        break
    else:
        maskedSentence = item[1]
        word = item[2]
        
        candidate = getCandidate(sentence, maskedSentence, classifier)
        print(candidate)

        if word not in candidate:
            candidate.insert(0, word)
        

        removedDup = cleanDup(candidate)
        morph = getMorph(maskedSentence, candidate)
        cleanedMorph = removeMorph(morph)
        deepClean = deepCleanX(cleanedMorph)

        print("DEEPCLEAN X", deepClean)
        
        sentenceSim_score_roberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="roberta", log=0)
        sentenceSim_score_disroberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="disroberta", log=0)

        sentenceSim_score_lmv6 = sentenceSimilarity(maskedSentence, deepClean, selectedModel="lmv6",log= 0)
    
        coSyn_score = crossSimilarity(deepClean, maskedSentence, modelName="lmv6", log=0)

        

        data = {"SentenceTransformer Roberta":sorted([[key,value] for key, value in sentenceSim_score_roberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer Roberta_distil":sorted([[key,value] for key, value in sentenceSim_score_disroberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer lmv6":sorted([[key,value] for key, value in  sentenceSim_score_lmv6.items()], key=lambda x: x[1], reverse=True),
                "Co-Synonym":sorted([[key,value] for key, value in coSyn_score.items()], key=lambda x: x[1][0], reverse=True)}
        df = pd.DataFrame(data)

        print(df)

        

        print("input sentence: ",sentence)

        
       
        command = input("hit enter to continue ")
        