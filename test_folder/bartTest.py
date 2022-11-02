from transformers import BartForConditionalGeneration as Bart, BartTokenizer

import torch

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

model = Bart.from_pretrained('facebook/bart-base')

sentence = """at the end of the day, he wins. <mask> <mask> <mask> he wins"""

token_ids = tokenizer.encode(sentence, return_tensors='pt')

# print(token_ids)

token_ids_tk = tokenizer.tokenize(sentence, return_tensors='pt')

print(token_ids_tk)

masked_position = (token_ids.squeeze() == tokenizer.mask_token_id).nonzero()

masked_pos = [mask.item() for mask in masked_position ]

print (masked_pos)

with torch.no_grad():

    output = model(token_ids)

last_hidden_state = output[0].squeeze()

print ("\n\n")

print ("sentence : ",sentence)

print ("\n")

list_of_list =[]

for mask_index in masked_pos:

    mask_hidden_state = last_hidden_state[mask_index]

    idx = torch.topk(mask_hidden_state, k=15, dim=0)[1]

    words = [tokenizer.decode(i.item()).strip() for i in idx]

    list_of_list.append(words)

    print (words)

    

best_guess = ""

for j in list_of_list:

    best_guess = best_guess+" "+j[0]