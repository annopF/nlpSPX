
import datetime
print("*******************************TIMESTAMP: Origin ", datetime.datetime.now().time())


from transformers import pipeline
from transformers import RobertaTokenizer, RobertaModel, RobertaForMaskedLM
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import pandas as pd
import time
from transformers import logging
from canclean import *

print("*******************************TIMESTAMP: Origin 2 ", datetime.datetime.now().time())

pd.set_option('display.max_colwidth', None)
logging.set_verbosity_error()

def sim(sentenceOG, sentenceList, predictedList):
    
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device = "cuda")

    #Compute embedding for both lists
    embeddings1 = model.encode(sentenceOG, convert_to_tensor=True)
    embeddings2 = model.encode(sentenceList, convert_to_tensor=True)
    ##print("embd1 size=",embeddings1.size())
    score = []
    #Compute cosine-similarities
    for i in range(len(sentenceList)):
        cosine_scores = util.cos_sim(embeddings1, embeddings2[i])
        score.append([predictedList[i], cosine_scores.flatten().tolist()])
        print("#",i," ", sentenceOG, " <--> ", sentenceList[i], cosine_scores)

    return score


print("*******************************TIMESTAMP: Start ", datetime.datetime.now().time())

tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaModel.from_pretrained("roberta-base")

sentence = "Google cloud is one of the most popular services in the industry"
maskedSentence = "Google cloud is one of the most <mask> services in the industry"
target = "popular"
print("*******************************TIMESTAMP: Before Pipeline ", datetime.datetime.now().time())

classifier = pipeline("fill-mask", model = "roberta-base", top_k=40, batch_size = 16, framework="pt", device = 0)

print("*******************************TIMESTAMP: After Pipeline ", datetime.datetime.now().time())

cat = sentence+" "+maskedSentence
print("*******************************TIMESTAMP: Before inference ", datetime.datetime.now().time())

start = time.time()
res = classifier(cat)

print("*******************************TIMESTAMP: After inference ", datetime.datetime.now().time())

predictedList = []
for i in range(len(res)):
    predictedList.append(res[i]["token_str"].strip())

print("*******************************TIMESTAMP: Before clean ", datetime.datetime.now().time())

cleaned = cleanAll(predictedList)

print("*******************************TIMESTAMP: After clean ", datetime.datetime.now().time())

sentenceList = []


for i in cleaned:
    replacedSentence = (maskedSentence.replace("<mask>", str(i)))
    sentenceList.append(replacedSentence)

#simSpa(sentence,sentenceList,predictedList)
print("*******************************TIMESTAMP: Before sent transformer ", datetime.datetime.now().time())

scoreList = sorted(sim(sentence,sentenceList,cleaned), key=lambda x:x[1], reverse=True)

print("*******************************TIMESTAMP: After sent transformer ", datetime.datetime.now().time())

#print("SCORE LIST 0:", scoreList[0][0])
stop = time.time()

data = {"sentence-transformer": scoreList}
df = pd.DataFrame(data)

print(df)

print("Elapsed time ", stop-start)


