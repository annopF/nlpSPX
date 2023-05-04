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
         self.newline = []

    def setUp(self,text):
        def findWord(self):

            def getTar(sent,target,count):
                s = re.finditer(fr"\b{target}\b",str(sent))
                print("XXX--XXX: sent.start=",sent.start_char)
                out = [sent.start_char + i.start() for i in s]
                
                if len(out) != 0:
                    return out[count]
                else:
                    return 1
                
            start = time.time()
            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence).lower())).returnList()
                    
                    for bg in self.bg:
                        count = 0
                        for i,target in enumerate(piece):
                        
                            if piece[i].lower() == bg.gram2.lower() and piece[i-1].lower() == bg.gram1.lower():
                                count+=1
                                
                                bg.sentenceObj.append(sentenceX(sentId,i-1, i, None, 
                                                                sentence.start_char, 
                                                                sentence.end_char,
                                                                getTar(sentence,bg.concat,count-1)))
                    for tg in self.tg:
                        count = 0
                        for i,target in enumerate(piece):
                            
                            if piece[i].lower() == tg.gram3.lower() and piece[i-1].lower() == tg.gram2.lower() and piece[i-2].lower() == tg.gram1.lower():
                                count+=1
                                tg.sentenceObj.append(sentenceX(sentId,i-2,i-1, i, 
                                                                sentence.start_char, 
                                                                sentence.end_char,
                                                                getTar(sentence,tg.concat,count-1)))
                    for ug in self.ug:
                        count = 0
                        for i,target in enumerate(piece):

                            if piece[i].lower() == ug.gram1.lower():
                                count+=1
                                print("---->>>>sentence",sentence, "#POS ",i, "#SentID ",sentId, "ug ", ug.gram1, "count ",count)
                            
                                ug.sentenceObj.append(sentenceX(sentId,i,None,None, 
                                                                sentence.start_char, 
                                                                sentence.end_char,
                                                                getTar(sentence,ug.concat,count-1)))
            end = time.time()
            print("------------------><><><><><<><><><> elapsed time",end-start)

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
        
        nlp = spacy.load("en_core_web_sm")
        for x,i in enumerate(text):
            if i == "\n":
                self.newline.append(x+1)
            
            
        doc = nlp(text.replace("\r", ""))
        for i in doc.sents:
            print("---S->",i)
        self.entIndex = doc.ents
        s = classifier(str(doc))
        self.DoNotHighLight = [i["start"] for i in s]
        self.doc = doc
        text = str(doc)
        text = re.sub("\(.*?\)|\[.*?\]|\{.*?\}", "", text)
     
        for i in self.entIndex:

            text = re.sub(fr"\b{i}\b", "", text)

        toks = selectTokenizer("wsp", text.lower()).returnList()
        self.ug = createUnigram(toks, 15)
        self.bg = createBigram(toks, 15)
        self.tg = createTrigram(toks, 15)
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
        topwords.append([(ug.concat, ug.count) for ug in self.ug if ug.safe][:5])
        topwords.append([(bg.concat, bg.count) for bg in self.bg if bg.safe][:5])
        topwords.append([(tg.concat, tg.count) for tg in self.tg if tg.safe][:5])

        return toks, [word for container in topwords for word in container]
    
    def cvtIndex(self,tk,x):
        print(">>>>LOG -tcl input:", tk)
        line = int(str(tk).split(".")[0])
        col = int(str(tk).split(".")[1])
        
        if line != 1:
            print(">>>> line={}, col={}, x={}, line-(x+2)={}".format(line,col,x, line-(x+2)))

            out = col + self.newline[line-(x+2)]
            print("out=", out)
            print("newline",self.newline)
            return(out)
        else:
            return(col)
    
    
# Test comment sar
# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
