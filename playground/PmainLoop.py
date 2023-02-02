import time
import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 200)


start = time.time()
print("importing modules...")
import networkx as nx
from transformers import pipeline 
from PtestFillMask import *
from Pcanclean import *
from Pscorer import *
from PgetMorph import *
from Putil import *
end = time.time()
print("(Import) Elapsed time: ", end - start, "DELTA=",8.1634-(end-start))



start = time.time()
print("Loading classifier...")
classifier = pipeline("fill-mask", model = "roberta-base", top_k=100, batch_size = 4, framework="pt", device = -1)

end = time.time()
print("(Classifier) Elapsed time: ", end - start)

while True:
    G = nx.DiGraph()

    sentence = input("enter a sentence: ")
    if sentence == "x":
        print("Terminated")
        break
    else:
        maskedSentence = input("enter a masked sentence: ")
        word = input("enter a word: ")
        
        candidate = getCandidate(sentence, maskedSentence, classifier)
        print(candidate)

        if word not in candidate:
            candidate.insert(0, word)
        

        removedDup = cleanDup(candidate)
        morph = getMorph(maskedSentence, candidate)
        cleanedMorph = removeMorph(morph)
        deepClean = deepCleanX(cleanedMorph)

        
        
        sentenceSim_score_roberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="roberta")
        sentenceSim_score_disroberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="disroberta")

        sentenceSim_score_lmv6 = sentenceSimilarity(maskedSentence, deepClean, selectedModel="lmv6")
    
        coSyn_score = crossSimilarity(sentenceSim_score_roberta.copy(),G)

        data = {"SentenceTransformer Roberta":sorted([[key,value] for key, value in sentenceSim_score_roberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer Roberta_distil":sorted([[key,value] for key, value in sentenceSim_score_disroberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer lmv6":sorted([[key,value] for key, value in  sentenceSim_score_lmv6.items()], key=lambda x: x[1], reverse=True),
                "Co-Synonym":sorted([[key,value] for key, value in coSyn_score.items()], key=lambda x: x[1], reverse=True)}
        df = pd.DataFrame(data)

        print(df)

        edgeLabel = nx.get_edge_attributes(G,"weight")
        nx.draw_networkx(G, pos=nx.shell_layout(G),node_size=1000, font_size=7, font_color="white")

        nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G),edge_labels=edgeLabel, font_size=7, font_color="black")
        plt.axis("off")
        plt.show()
        G.clear()
        