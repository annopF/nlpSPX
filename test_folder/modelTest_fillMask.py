from transformers import logging
from transformers import pipeline
import sys
import time
from semanticSim import sim

print("---------------------------------------------------- start")
startTime = time.time()
logging.set_verbosity_error()
inputText = "the weather is good today."
repeatWord = "good"
print("john")

#choose model:
model1 = "bert-base-uncased"
model2 = "bert-large-cased-whole-word-masking"

maskedText = inputText.replace(repeatWord,"[MASK]")
print("original sentence:", maskedText)
concatText = inputText+" "+maskedText

model = pipeline("fill-mask", model = model2, top_k=20) 

result = model(concatText)

for i in range(len(result)):
    replacedText = inputText.replace(repeatWord,result[i]["token_str"])
    print ("replaced text: ", replacedText)

    print(result[i]["token_str"], sim(inputText,replacedText))

print("---------------------------------------------------- elapsed time: ", time.time()- startTime)