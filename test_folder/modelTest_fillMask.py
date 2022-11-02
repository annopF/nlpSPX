from transformers import logging
from transformers import pipeline
import sys
import time
from semanticSim import sim

print("---------------------------------------------------- start")
startTime = time.time()
logging.set_verbosity_error()
inputText = """i like apple juice because it is <mask> tasty"""

repeatWord = "very"
maskedText = inputText.replace(repeatWord,"[MASK]")
fakeText = "nice good wonderful powerful solid  ."
textPlus = """civilization art experience skill people accomplishment"""

#choose model:
model1 = "roberta-base"
model2 = "bert-large-cased-whole-word-masking"

print("original sentence:", maskedText)
concatText = inputText

model = pipeline("fill-mask", model = model1, top_k=10,targets=None )
print("model:: ", model)

result = model(inputText)

for i in range(len(result)):
    replacedText = inputText.replace(repeatWord,result[i]["token_str"])

    print(result[i]["token_str"])

print("---------------------------------------------------- elapsed time: ", time.time()- startTime)