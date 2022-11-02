import tensorflow_hub as hub
import tensorflow_text as text
import numpy as np
import sys
#print all members of embedding
#np.set_printoptions(threshold=sys.maxsize)

prepModel = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
model =  hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

text = ["i don't like apple because it sucks so much in the night", 
"google pixel is good but it sucks so much as hell"]
modelInput = tokenizer
#preprocessing
preprocessed = prepModel(text)
print(preprocessed.keys())
print(preprocessed["input_word_ids"])

#real processing
res = model(preprocessed)
print(res["pooled_output"])