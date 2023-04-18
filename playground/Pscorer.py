from sentence_transformers import SentenceTransformer,CrossEncoder
from sentence_transformers import util

import time
import json
import networkx as nx
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
def paraphrase(input_sentence):
    model = AutoModelForSeq2SeqLM.from_pretrained('ramsrigouthamg/t5_sentence_paraphraser')
    tokenizer = AutoTokenizer.from_pretrained('ramsrigouthamg/t5_sentence_paraphraser')
    device = torch.device('cpu')
    
    # Prepare the input
    input_ids = tokenizer.encode(input_sentence, return_tensors='pt').to(device)

    # Generate the paraphrased sentence
    output_ids = model.generate(input_ids=input_ids,
                                do_sample = True,
                                max_length = 32,
                                num_beams = 10,
                                length_penalty = 5.0,
                                no_repeat_ngram_size = 3,
                                early_stopping = True,
                                encoder_no_repeat_ngram_size = 2,
                                repetition_penalty = 15.0
                                )
    
    # Decode the output
    output_sentence = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return output_sentence
#INPUT Type: list, Shape: ["word0","word1","word2"]
#OUTPUT Type: dict(unsorted), Shape: {"word0: 0.66", "word1": 0.89}
#DESC: Get input list, substitute <mask>, and calculate sentenece similarity.
#      This function convert input list to dictionary -> {"word":score}
def sentenceSimilarity(maskedSentence, inputList, model, mode):
    
    
    sentenceList = [maskedSentence.replace("<mask>", word) for word in inputList ]

    

    #Compute embedding for both lists

    start = time.time()
    
    embeddings = (model.encode(sentenceList, convert_to_tensor=True))
    
    
    ##print("embd1 size=",embeddings1.size())
    #score = []
    score = {}
    #Compute cosine-similarities
    for i, word in enumerate(inputList):
        cosine_scores = util.cos_sim(embeddings[0], embeddings[i])
        #score.append([word, cosine_scores.flatten().tolist()])
        score[word]=round(cosine_scores.flatten().tolist()[0],6)
        #if log == 1:
            #print("#",i," ", sentenceList[0], " <--> ", sentenceList[i], cosine_scores)

    end = time.time()
    print("elapsed time:", end-start)
    #print("Pscorer-sentenceSimilarity-> elapsed time:", end - start)
    if mode ==1:
        return (score)
    elif mode ==0:
        return(sorted([[key,value] for key, value in score.items()], key= lambda x: x[1], reverse=True))
    #sorted(score, key=lambda x:x[1], reverse=True)


def entailment(maskedSentence, inputList, model1, model2):
    start = time.time()
    fromSentenceSim = sentenceSimilarity(maskedSentence, inputList, model=model1, mode=1)

    inputList = [key for key in fromSentenceSim]
    for i, word in enumerate(inputList):

        ogSen = maskedSentence.replace("<mask>",inputList[0])
        targetSen = maskedSentence.replace("<mask>",inputList[i])

        entail_score = model2.predict([(ogSen, targetSen)])
        
        #Convert scores to labels
        labels = [score_max for score_max in entail_score.argmax(axis=1)]
     
        if labels[0] == 0:
            fromSentenceSim[word] -= entail_score.flatten()[labels[0]]
        else:
            fromSentenceSim[word] += entail_score.flatten()[labels[0]]

    end = time.time()
    print("elapsed time:", end-start)

    return(sorted([[key,value] for key, value in fromSentenceSim.items()], key= lambda x: x[1], reverse=True))

def simMax(maskedSentence, inputList, model, mode):
    
    G = nx.DiGraph()
    G.add_nodes_from(inputList)
    start = time.time()
    sentenceList = [maskedSentence.replace("<mask>", word) for word in inputList ]
    embeddings = (model.encode(sentenceList, convert_to_tensor=True))
    
    
    ##print("embd1 size=",embeddings1.size())
    #score = []
    #Compute cosine-similarities
    for i,ref in enumerate(sentenceList):
        for j,word in enumerate(sentenceList):
            if i !=j:
                cosine_scores = util.cos_sim(model.encode(ref, convert_to_tensor=True), model.encode(word, convert_to_tensor=True))
                #score.append([word, cosine_scores.flatten().tolist()])
                score = round(cosine_scores.flatten().tolist()[0],6)
                if score > 0.9 and score !=1:
                    #print("i,j: ",inputList[i],inputList[j],score)
                    G.add_edge(inputList[i],inputList[j],weight = score)

        #if log == 1:
            #print("#",i," ", sentenceList[0], " <--> ", sentenceList[i], cosine_scores)

    li = sorted([(i,G.in_degree(i, weight = "weight")) for i in inputList], key=lambda x:x[1], reverse=True)
    end = time.time()
    print("elapsed time:", end-start)

    return(li)

    
    



