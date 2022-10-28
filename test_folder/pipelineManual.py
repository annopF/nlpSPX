from sys import maxsize
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


    original_output = raw_model(tokenizer.encode(sentence, return_tensors="pt"))
    input_embeds = original_output[2][1]

    target_token_id = tokenizer.encode(" "+target)[1]
    input_ids = tokenizer.encode(" " + sentence)
    mask_position = input_ids.index(target_token_id)

    #print("lm model ",lm_model)
    #print("raw_model ", raw_model)
    print("input embed ", torch.Tensor.size(input_embeds))
    #print("input embed 0 5 ",torch.Tensor.size(input_embeds[0,5]))
    
    print("maskPosition,", mask_position)
   
    dropRate = round(1*768)

    dropout_indices = np.random.choice(768,dropRate,False)
    input_embeds[0,mask_position,dropout_indices] = 0
    #print(input_embeds[0,5])

    with torch.no_grad():
        res = lm_model(inputs_embeds=input_embeds)

    logits = res[0].squeeze()
    maskLogit = logits[mask_position]
    out = torch.topk(maskLogit, k=10, dim=0)[1]
    for i in out:
        a = tokenizer.decode(i)
        print(a)
    print (out)
    
testTorch("i like apple juice because it is very tasty","very")

