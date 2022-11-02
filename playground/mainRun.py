from sys import maxsize
from regex import F
import tokenizers
from transformers import AutoTokenizer, RobertaForMaskedLM, RobertaModel
from transformers import BartForConditionalGeneration as Bart, BartTokenizer
import torch
import numpy as np
np.set_printoptions(threshold=maxsize)
def testTorch(sentence,mask_position):
    torch.set_printoptions(threshold=maxsize) 

    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
    lm_model = Bart.from_pretrained("facebook/bart-large")
    raw_model = Bart.from_pretrained("facebook/bart-large", output_hidden_states=True, output_attentions=True)

    #tokenize sentene
    original_output = raw_model(tokenizer.encode(sentence, return_tensors="pt")) #this is !tensor

    input_embeds = original_output[2][1] #this is tensor

    input_ids = tokenizer.encode(" " + sentence) #encode sentence (!tensor)

    #target_token_id = tokenizer.encode(" "+"<mask>")[1] #not working because it is masksed
    # the input should be a word, since it will be partially masked (dropout), so whole word must be taken as an input, 
    # so can't pass sentence with <mask> token in it as an input.
    # !! need to get the exact index of the word to dropout in case a sentence has multiple instances of the same word.
    # e.g. i really want a car because it is really cool --> 2 really in the text.  

    dropRate = round(0.32*768) #set drop rate in %

    dropout_indices = np.random.choice(768,dropRate,False)
    input_embeds[0,mask_position,dropout_indices]

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
    
testTorch("i really like apple", 2)

