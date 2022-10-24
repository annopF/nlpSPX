from transformers import logging
from transformers import pipeline
import sys
import time
from semanticSim import sim

print("---------------------------------------------------- start")
startTime = time.time()
logging.set_verbosity_error()
inputText = "iphone 4 has a good camera system."
repeatWord = "system"


#choose model:
model1 = "bert-base-uncased"
model2 = "bert-large-cased-whole-word-masking"

maskedText = inputText.replace(repeatWord,"[MASK]")
print("original sentence:", maskedText)
concatText = inputText+" "+maskedText

model = pipeline("fill-mask", model = model1, top_k=10,targets=None )
print("model:: ", model)

result = model(concatText)

for i in range(len(result)):
    replacedText = inputText.replace(repeatWord,result[i]["token_str"])
    print ("replaced text: ", replacedText)

    print(result[i]["token_str"], sim(inputText,replacedText))

print("---------------------------------------------------- elapsed time: ", time.time()- startTime)