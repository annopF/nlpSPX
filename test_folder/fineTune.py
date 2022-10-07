import numpy as np
import pandas as pd
import tensorflow as tf
import transformers

max_length = 128  # Maximum length of input sentence to the model.
batch_size = 32
epochs = 2

# Labels in our dataset.
labels = ["contradiction", "entailment", "neutral"]

train = pd.read_csv("F:/Work Folder/KMUTT/SeniorProject/dataset/SNLI_Corpus/snli_1.0_train.csv", nrows=100000)
valid = pd.read_csv("F:/Work Folder/KMUTT/SeniorProject/dataset/SNLI_Corpus/snli_1.0_dev.csv")
test = pd.read_csv("F:/Work Folder/KMUTT/SeniorProject/dataset/SNLI_Corpus/snli_1.0_test.csv")

# Shape of the data
print(f"Total train samples : {train.shape[0]}")
print(f"Total validation samples: {valid.shape[0]}")
print(f"Total test samples: {valid.shape[0]}")