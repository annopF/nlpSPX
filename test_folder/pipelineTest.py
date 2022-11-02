from transformers import TFAutoModelForMaskedLM, AutoTokenizer
import tensorflow as tf


tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
model = TFAutoModelForMaskedLM.from_pretrained("distilbert-base-cased")

sequence = ["The essay is very [MASK] but very informative and instesting"]

inputs = tokenizer(sequence, return_tensors="tf")
print(inputs)
mask_token_index = tf.where(inputs["input_ids"] == tokenizer.mask_token_id)[0,1]
print ("is tensor ", tf.is_tensor(inputs["input_ids"]))


token_logits = model(**inputs).logits
mask_token_logits = token_logits[0, mask_token_index, :]

print("debug_____________________________________________________________")
print ("input.key ",inputs.keys())
print(inputs)
tf.print("inputs_ids ",inputs.input_ids, summarize=20)
tf.print("attention_mask ",inputs.attention_mask, summarize=20)

print ("mask_token_index ",mask_token_index)
print ("mask_token_id ",tokenizer.mask_token_id)
tf.print("token_logits[0][0] ",token_logits[0][0], summarize=10)
print ("size of token_logits[0][0] ", len(token_logits[0][0]))
print("token logit size ",len(token_logits[0]))
print("mask_token_logit ", mask_token_logits)
print("masked token index", mask_token_index )
print("debug_____________________________________________________________")

top_5_tokens = tf.math.top_k(mask_token_logits, 5).indices.numpy()

for token in top_5_tokens:
    print( tokenizer.decode([token]))
    print()