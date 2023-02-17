from tokenizer import selectTokenizer
import PyPDF2 as pdf 
import spacy
from ngram import bigram, unigram, trigram
import textract as tt

filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/fortuneteller.pdf"
text = tt.process(filePath)
texts = text.decode("utf8")


print(texts)
nlp = spacy.load("en_core_web_lg")

doc = nlp(texts)

for i,sentence in enumerate(doc.sents):
    print("#",i,sentence)
    