import time
from transformers import logging
from transformers import pipeline
from Pcanclean import cleanDup
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from parrot import Parrot
import warnings
import torch
warnings.filterwarnings("ignore")


# def paraphraser(phrase):
#     #Init models (make sure you init ONLY once if you integrate this to your code)
#     parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
#
#     print("dddd",phrase)
#     res = parrot.augment(input_phrase=phrase,
#                                 use_gpu=False,
#                                 max_return_phrases = 3,
#                                 max_length=32,
#                                 fluency_threshold = 0.5,
#                                 adequacy_threshold = 0.6
#                                 )
#     print("--<>",res)
#     return(res[2][0])

# def paraphrase(input_sentence):
#     model = AutoModelForSeq2SeqLM.from_pretrained('Vamsi/T5_Paraphrase_Paws')
#     tokenizer = AutoTokenizer.from_pretrained('Vamsi/T5_Paraphrase_Paws')
#     device = torch.device('cpu')
#
#     # Prepare the input
#     input_ids = tokenizer.encode(input_sentence, return_tensors='pt').to(device)
#
#     # Generate the paraphrased sentence
#     output_ids = model.generate(input_ids=input_ids,
#                                 max_length=len(input_sentence),
#                                 do_sample = False,
#                                 top_k=200
#                                 )
#
#     # Decode the output
#     output_sentence = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#
#     return output_sentence

def printPartial(sen):
  a = sen.split()
  print(" ".join(a[0:int(len(a)/2)]))
  return " ".join(a[0:int(len(a)/2)])

def getCandidate(sentence,maskedSentence,classifier,word):

    logging.set_verbosity_error()
    # para = paraphrase(sentence)
    # print(para)
    cat = sentence+"."+" "+maskedSentence
    res = classifier(cat)
    predictedList = {}
    
    for i,item in enumerate(res):
        predictedList[res[i]["token_str"].lower().strip()] = res[i]["score"]

    final = sorted([[key, value] for key,value in predictedList.items()], key=lambda x:x[1], reverse=True)

    final = cleanDup(final)
    for i,item in enumerate(final):
        if item[0] == word:
            final.pop(i)
    final.insert(0,[word,1.0])
    return(final)
        
def fillNextWord(maskedSentence, classifier,k):

    logging.set_verbosity_error()

    res = classifier(maskedSentence)
    predictedList = {}
    
    
    for i,item in enumerate(res):
        predictedList[res[i]["token_str"].lower().strip()] = res[i]["score"]

    final = sorted([[key, value] for key,value in predictedList.items()], key=lambda x:x[1], reverse=True)

    return (final[:k])





