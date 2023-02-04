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
classifier = pipeline("fill-mask", model = "roberta-base", top_k=50, batch_size = 8, framework="pt", device = -1)

end = time.time()
print("(Classifier) Elapsed time: ", end - start)
testData = [["Our approach is correct but my professor said it is not correct","Our approach is <mask> but my professor said it is not correct","correct"],
            ["The mask detecting software is optimized for surgical mask only","The <mask> detecting software is optimized for surgical mask only","mask"],
            ["Sodium Hydroxide is very sensitive to sunlight","Sodium Hydroxide is very <mask> to sunlight","sensitive"],
            ["The software is optimized for low-powered devices such as smartphone","The <mask> is optimized for low-powered devices such as smartphone","software"],
            ["Our project is about the application of machine translation","Our <mask> is about the application of machine translation","project"],
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
    G = nx.DiGraph()

    sentence = item[0]
    if sentence == "x":
        print("Terminated")
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

        
        
        sentenceSim_score_roberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="roberta", log=0)
        sentenceSim_score_disroberta = sentenceSimilarity(maskedSentence, deepClean, selectedModel="disroberta", log=0)

        sentenceSim_score_lmv6 = sentenceSimilarity(maskedSentence, deepClean, selectedModel="lmv6",log= 0)
    
        coSyn_score = crossSimilarity(deepClean,G,maskedSentence, modelName="lmv6", log=0)

        

        data = {"SentenceTransformer Roberta":sorted([[key,value] for key, value in sentenceSim_score_roberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer Roberta_distil":sorted([[key,value] for key, value in sentenceSim_score_disroberta.items()], key= lambda x: x[1], reverse=True),
                "SentenceTransformer lmv6":sorted([[key,value] for key, value in  sentenceSim_score_lmv6.items()], key=lambda x: x[1], reverse=True),
                "Co-Synonym":sorted([[key,value] for key, value in coSyn_score.items()], key=lambda x: x[1][0], reverse=True)}
        df = pd.DataFrame(data)

        print(df)

        edgeLabel = nx.get_edge_attributes(G,"weight")
        nx.draw_networkx(G, pos=nx.shell_layout(G),node_size=1000, font_size=7, font_color="white")

        nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G),edge_labels=edgeLabel, font_size=7, font_color="black")
        plt.axis("off")
        attr = G.node_attr_dict_factory()
        print(attr)

        """ 
        for item in G.edges():
            print(item)
            print("----------->",item,G.get_edge_data(item[0], item[1])) """
        plt.show()

        G.clear()
        