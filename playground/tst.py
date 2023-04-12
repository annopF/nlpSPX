import spacy
import textract as tt
import re


def generateText(mode):
    if mode == 1:
        filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/Rich Kids essay real one.pdf"
        text = tt.process(filePath)
        texts = text.decode("utf8")
        return (texts)
    else:
        sentence = """
        I don't like Apple iPhone very much due to its price, but I don't like Apple iPhone more. 
        This apple iphone is awesome. 
        Tim like macbook pro but don't like Apple iPhone. 
        Steve job also don't like Apple iPhone. 
        Bill gate really don't like Apple product but like Samsung."""
        return (sentence)


nlp = spacy.load("en_core_web_lg")
doc = nlp(generateText(1).replace("\n", " ").replace("\r", ""))
text = str(doc)

ent = doc.ents

text = re.sub("\(.*?\)|\[.*?\]|\{.*?\}", "", text)

for i in ent:
    text = re.sub(fr"\b{i}\b", "", text)

print(text)
