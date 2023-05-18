import time
import pandas as pd
import ranky as rk
import inter_values
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import RobertaTokenizer,RobertaForMaskedLM
from sentence_transformers import SentenceTransformer

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
start = time.time()
from transformers import pipeline 
from sentence_transformers import CrossEncoder
from PtestFillMask import *
from Pcanclean import *
from Pscorer import *
from PgetMorph import *
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)


end = time.time()
print("(Import) Elapsed time: ", end - start, "DELTA T=", 8.1634-(end-start), "Avg. loading time= 8.1634")
use = "cpu"
print("preparing SentenceTransformers")
lmv6  = SentenceTransformer("sentence-transformers/stsb-roberta-base-v2", device = use)
mnli  = SentenceTransformer("textattack/roberta-base-MNLI", device = use)
dbt = CrossEncoder('cross-encoder/nli-roberta-base', device=use)
limit = 15 #(final output display limit)
classifierLimit = 60 #recommened = 60
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
    res = sorted([[key, value] for key, value in out.items()], key=lambda x: x[1], reverse=False)
    return(checkLev(res)) # !REVERSE MUST BE FALSE!

def loadClassifier(MAX):

    print("Loading classifier...")

    #Cmodel = RobertaForMaskedLM.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
    #Ctokenizer = RobertaTokenizer.from_pretrained("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/rbtaX3_500k")
    
    return (pipeline("fill-mask", model = "roberta-base", top_k=MAX, framework="pt", device = -1))
classifier = loadClassifier(classifierLimit)

print("(Classifier) Elapsed time: ", end - start, "DELTA T=", 15-(end-start))




testData = [
                ["Steve Jobs likes White color, so everything in the factory is White.","Steve Jobs likes White color, so everything in the <mask> is White.","factory"],
                ["Samsung Galaxy watch is the best Android Wearable on the marketright now","Samsung Galaxy watch is the best Android Wearable on the <mask> right now","market"],
                ["I drive MG car to London", "I <mask> MG car to London","drive"],
                ["Apple Park is a circular building worth millions of dollar.", "Apple Park is a circular <mask> worth millions of dollar.", "building"],
                ["Rich people can escape the a long jail sentence when commiting a crime", "Rich <mask> can escape the a long jail sentence when commiting a crime", "people"],
                ["Apple, Inc. is founded by Steve Job.", "Apple, Inc. is <mask> by Steve Job.", "founded"],
                ["Sir Jonathan Ive is the chief designer at Apple","Sir Jonathan Ive is the <mask> designer at Apple","chief"],
                ["I don't like Spotify service because it is expensive","I don't like Spotify <mask> because it is expensive","service"],
                ["Global climate change has become a major problem lately","Global climate change has become a major <mask> lately","problem"],
                ["The micro processor from Apple called Apple Silicon beats those from Intel","The micro <mask> from Apple called Apple Silicon beats those from Intel","processor"],
                ["Electric vehicles from Tesla can drive autonomously","Electric vehicles from Tesla can drive <mask>","autonomously"],
                ["How can a teacher teach better in online classes during the pandemic","How can a teacher teach better in online <mask> during the pandemic","classes"],
                ["Sir James Dyson invented a turbo charger","Sir James Dyson <mask> a turbo charger","invented"],
                ["The professor said our work is wrong, but our friend's work is right","The professor said our <mask> is wrong, but our friend's work is right","work"],
                ["This chemical is the base of all nuclear reaction including nuclear fission","This chemical is the base of all nuclear <mask> including nuclear fission","reaction"],
                ["This chemical helps lower the activation energy of the reaction","This <mask> helps lower the activation energy of the reaction","chemical"],
                ["In reality, time travel is not possible although in theory it is","In reality, time <mask> is not possible although in theory it is","travel"],
                ["Do you believe that if rich people commit a crime, they can get away easier beacuse they are rich?","Do you believe that if rich <mask> commit a crime, they can get away easier beacuse they are rich?","people"],
                ["In the case of Ethan Couch, he was drunk drive and killing 4 people, but he came from a rich family, he can escape the laws","In the case of Ethan Couch, he was drunk drive and killing 4 people, but he came from a rich <mask>, he can escape the laws","family"],
                ["I want to buy a new computer, which one should I get","I want to buy a new <mask>, which one should I get","computer"],
                ["Most kpop fan don't like ballad song because they are boring","Most kpop <mask> don't like ballad song because they are boring","fan"],
                ["Our project is about the application of Machine Learning","Our <mask> is about the application of Machine Learning","project"],
                ["How to write a better essay in English writing class?","How to write a better <mask> in English writing class?","essay"],
                ["HP Omen is a gaming laptop with external cooling pipe to keep the laptop cool","HP Omen is a gaming laptop with external cooling pipe to keep the <mask> cool","laptop"],
                ["x"]
                ]



def makeOutput(fmp):
    print("makeOutput started...")

    sentence = fmp[0]
    maskedSentence = fmp[1]
    word = fmp[2]

    print("getting candidate...")

    start = time.time()
    candidate = getCandidate(sentence, maskedSentence, classifier, word)
    ogLen = len(candidate)
    # removedMorph = removeMorph(maskedSentence, candidate)
    # deepClean = deepCleanX(removedMorph)
    cleanedMorph = removeMorph(maskedSentence, candidate)
    deepCleans = deepCleanX(cleanedMorph)
    # print("deepclean (s)", deepCleans)
    deepClean = [x[0] for x in deepCleans]
    # print("deepclean no s",deepClean)
    end = time.time()
    print("(get candidate + clean) elapse time=", end - start)

    # print("DEEPCLEAN X", deepClean)
    print("verifying...")

    ST_outputMNLI = sentenceSimilarity(maskedSentence, deepClean, model=mnli, mode=0)
    ST_outputLMV6 = sentenceSimilarity(maskedSentence, deepClean, model=lmv6, mode=0)
    entail = entailment(maskedSentence, deepClean, model1=mnli, model2=dbt)
    rerank = rankAll(deepCleans, ST_outputMNLI, ST_outputLMV6, entail)
    data = {
        "OG rank": deepCleans[:limit],
        "ST MNLI": ST_outputMNLI[:limit],
        "ST LMV6": ST_outputLMV6[:limit],
        "Entailment_score": entail[:limit],
        "rerank": rerank[:limit]}
    df = pd.DataFrame(data)
    print(df)
    # print("*****DEEPCLEAN:", candidate)
    # print("///////REMOVE MORPH:", removedMorph )
    print(">>>> OG SEN:", sentence)
    print(">>>> MASKED WORD:", word)
    print(">>>> MASKED SEN:", maskedSentence)
    # print("---- PARA SEN:", paraphrase(sentence))
    print(">>>> OG:Final ratio = {}/{}".format(ogLen, len(rerank)))
    print("-" * 100)

    wordlist = []
    # for n in range(1, 10):
    #     wordlist.append(data["rerank"][n][0])
    for word_out in data["rerank"]:
        if word_out[1] <= 10:
            if word_out[0] == word:
                continue
            wordlist.append(word_out[0])
        else:
            break

    inter_values.suggested_words.append(wordlist)
#makeOutput(testData[0])
