#THIS IS TOKENIZER 
#USING SPACY
import spacy
from spacy.symbols import ORTH
from spacy.matcher import Matcher
import re

#read input text file
text0 = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/sampletext.txt",encoding="UTF-8").read() 

#crete nlp model 
nlp = spacy.load("en_core_web_trf")

#add exception so tokenizer won't split into ex. "don't" -> "do", "n't"
def addSpecialCase():

    #list of contractions
    """ contraction = ["I'd","I'll","I've","I'm","She'd","She'll","They",
    "They're","They've","We'd","We'll","We're","It's","It'll","That's","There's","Where's",
    "Let's","Can't","Couldn't","Didn't","Doesn't","Don't","Hadn't","Hasn't","Isn't","Shouldn't",
    "Wasn't","Won't","Wouldn't","Could've","Might've","Must've","Should've","Would've","Ain't"] 

    for ex in contraction:
        nlp.tokenizer.add_special_case(ex,[{ORTH:ex}])
        nlp.tokenizer.add_special_case(ex.lower(),[{ORTH:ex.lower()}])
 """
    
#add exception so tokenizer won't split into ex. "bert-base" -> "bert","-","base"
def addSpecialCase2():

    matcher = Matcher(nlp.vocab)
    matcher.add("HYPHEN",[[{"ORTH":{"REGEX":"\w+"}},{"ORTH":{"REGEX":"-"}},{"ORTH":{"REGEX":"\w+"}}]])

    span = []
    with doc.retokenize() as retokenizer:
        for match_id, start, end in matcher(doc):
            span.append([start,end])

            print("span ",span)
            retokenizer.merge(doc[start:end])

infix_re = re.compile(r"\w+[']\w{1,2}")

nlp.tokenizer.infix_finditer = infix_re.finditer

doc = nlp(text0)



print([t.text for t in doc])
