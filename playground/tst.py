import spacy
import textract as tt
import re

import textract as tt

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
text = """I like likeness like,
food

goodl food"""

""" s = re.finditer(r"\blie\b", text)
print(s)
doc = nlp(text)
if s == None:
    print("NONENNEONEOEN")
out = [i.start() for i in s]
print(out, len(out))
 """
 
for i in text:
    if i == "\n":
        print("fucker")