##working code for dropout
from sys import maxsize
from regex import F
import tokenizers
from transformers import AutoTokenizer, RobertaForMaskedLM, RobertaModel
import torch
import numpy as np
np.set_printoptions(threshold=maxsize)
def testTorch(sentence,target):
    torch.set_printoptions(threshold=maxsize) 

    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    lm_model = RobertaForMaskedLM.from_pretrained("roberta-base")
    raw_model = RobertaModel.from_pretrained("roberta-base", output_hidden_states=True, output_attentions=True)

    #tokenize sentene
    original_output = raw_model(tokenizer.encode(sentence, return_tensors="pt")) #this is !tensor

    input_embeds = original_output[2][1] #this is tensor

    target_token_id = tokenizer.encode(" "+target)[1] #get id of target word

    input_ids = tokenizer.encode(" " + sentence) #encode sentence (!tensor)

    mask_position = input_ids.index(target_token_id)

    print("tgar token id ",target_token_id)
    print("masked target id ", target_token_id)
    print("mask token <mask>  ", tokenizer.mask_token_id)
    #print("lm model ",lm_model)
    #print("raw_model ", raw_model)
    print("input embed ", torch.Tensor.size(input_embeds))
    #print("input embed 0 5 ",torch.Tensor.size(input_embeds[0,5]))
    print("maskPosition,", mask_position)
   
    dropRate = round(1*768)

    dropout_indices = np.random.choice(768,dropRate,False)
    for i in range(10):

        input_embeds[0,2,i] = 0

    print(input_embeds[0,2])

    with torch.no_grad():
        res = lm_model(inputs_embeds=input_embeds)

    logits = res[0].squeeze()
    maskLogit = logits[mask_position] #this is tensor
    for i in range (2):

        print("mask logit ",maskLogit[i])
        print("mask logit size ",type(maskLogit))

    out = torch.topk(maskLogit, k=10, dim=0)[1]
    for i in out:
        a = tokenizer.decode(i)
        print (i)
        print(a)
    print (out)
    
testTorch("i really like apple because it is really good","really")

