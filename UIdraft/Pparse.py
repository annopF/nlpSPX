import spacy
from tokenizer import *
from createNgram import *
from Putil import isStopword
from spacy import displacy
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
import time

start = time.time()
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-large-finetuned-conll03-english")
classifier = pipeline("ner", model=model, tokenizer=tokenizer)
end = time.time()
print("elapsed time (AtMForTokenClassification)", end - start)

class parse():
    def __init__(self):
         self.doc = None
         self.entIndex = None
         self.DoNotHighLight = None
         self.ug = None
         self.bg = None
         self.tg = None

    def setUp(self,text):
        def findWord(self):

            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence).lower())).returnList()
                    for bg in self.bg:
                        #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
                                    
                        for i,target in enumerate(piece):
                            if piece[i].lower() == bg.gram2.lower() and piece[i-1].lower() == bg.gram1.lower():
                                #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                                bg.sentenceObj.append(sentenceX(sentId,i-1, i, None, sentence.start_char, sentence.end_char))

            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence).lower())).returnList()
                    for tg in self.tg:
                        #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
                                    
                        for i,target in enumerate(piece):
                            if piece[i].lower() == tg.gram3.lower() and piece[i-1].lower() == tg.gram2.lower() and piece[i-2].lower() == tg.gram1.lower():
                                #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                                tg.sentenceObj.append(sentenceX(sentId,i-2,i-1, i, sentence.start_char, sentence.end_char))

            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence).lower())).returnList()
                    for ug in self.ug:
                        #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
                                    
                        for i,target in enumerate(piece):
                            if piece[i].lower() == ug.gram1.lower():
                                #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                                ug.sentenceObj.append(sentenceX(sentId,i,None,None, sentence.start_char, sentence.end_char))
        
        def checkSafe(self):
            for bigram in self.bg:
                if isStopword(bigram.gram1) and isStopword(bigram.gram2):
                    bigram.safe = False

            for trigram in self.tg:
                if isStopword(trigram.gram1) and isStopword(trigram.gram2) and isStopword(trigram.gram3):
                    trigram.safe = False

            for unigram in self.ug:
                if isStopword(unigram.gram1):
                    unigram.safe = False

        nlp = spacy.load("en_core_web_trf")
        doc = nlp(text.replace("\n", "").replace("\r", ""))
        self.entIndex = doc.ents
        s = classifier(str(doc))
        self.DoNotHighLight = [i["start"] for i in s]
        self.doc = doc
        text = str(doc)
        text = re.sub("\(.*?\)|\[.*?\]|\{.*?\}", "", text)
        print("-------this is self no hilight")
        print(self.DoNotHighLight)
        print("-------this is entIndex")
        print(self.entIndex)
        for i in self.entIndex:

            text = re.sub(fr"\b{i}\b", "", text)

        toks = selectTokenizer("wsp", text.lower()).returnList()

        self.ug = createUnigram(toks, 10)
        self.bg = createBigram(toks, 10)
        self.tg = createTrigram(toks, 10)
        findWord(self)
        checkSafe(self)

    def getGram(self, gram):
        if gram == 1:
            return(self.ug)
        elif gram == 2:
            return(self.bg)
        else:
            return(self.tg)

    def scantexts(self):
        toks = []
        topwords = []
        topwords.append([(ug.concat, ug.count) for ug in self.ug if ug.safe][:3])
        topwords.append([(bg.concat, bg.count) for bg in self.bg if bg.safe][:3])
        topwords.append([(tg.concat, tg.count) for tg in self.tg if tg.safe][:3])

        return toks, [word for container in topwords for word in container]

# Test comment sar
# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
