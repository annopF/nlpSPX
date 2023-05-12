import spacy
from tokenizer import *
from createNgram import *
from Putil import isStopword, stopword, cleanDup
from spacy import displacy
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
import time

start = time.time()
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
classifier = pipeline("ner", model=model, tokenizer=tokenizer,grouped_entities=True)
nlp = spacy.load("en_core_web_lg")
end = time.time()
print("elapsed time (loading spacy+atm)", end - start)

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
        startX = time.time()
        def findWord(self):

            def getTar(sent,target,count):
                s = re.finditer(fr"\b{target}\b",str(sent).lower())
            
                out = [sent.start_char + i.start() for i in s]

                if len(out) != 0:
                    return out[count]
                else:
                    return 1
                
            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence).lower())).returnList()
                    
                    for bg in self.bg:
                        count = 0
                        for i,target in enumerate(piece):
                        
                            if piece[i].lower() == bg.gram2.lower() and piece[i-1].lower() == bg.gram1.lower():
                                count+=1
                                #print("---->>>>sentence",sentence, "#POS ",i, "#SentID ",sentId, "bg ", bg.gram1,bg.gram2, "count ",count)

                                #print("count:",count)
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
                                #print("---->>>>sentence",sentence, "#POS ",i, "#SentID ",sentId, "ug ", ug.gram1, "count ",count)
                            
                                ug.sentenceObj.append(sentenceX(sentId,i,None,None, 
                                                                sentence.start_char, 
                                                                sentence.end_char,
                                                                getTar(sentence,ug.concat,count-1)))
    
        def checkSafe(self):
            for bigram in self.bg:
                if isStopword(bigram.gram1) or isStopword(bigram.gram2):
                    bigram.safe = False

            for trigram in self.tg:
                if isStopword(trigram.gram1) or isStopword(trigram.gram2) or isStopword(trigram.gram3):
                    trigram.safe = False

            for unigram in self.ug:
                if isStopword(unigram.gram1):
                    unigram.safe = False
           
        

        start = time.time()
        for x,i in enumerate(text):
            if i == "\n":
                self.newline.append(x+1)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (find newline)",end-start)

        start = time.time()
        doc = nlp(text.replace("\r", ""))
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (replace /r)",end-start)


        start = time.time()
        s = classifier(str(doc))
        #print(s)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (NER)",end-start)

        start = time.time()
        self.entIndex = cleanDup([value for x in s for key, value in x.items() if key == "word"])
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (clean NER)",end-start)

        #print(self.entIndex)
        
        self.DoNotHighLight = [(i["start"],i["end"]) for i in s]
        #print(self.DoNotHighLight)
        self.doc = doc
        text = str(doc)
        start = time.time()
        text = re.sub("\(.*?\)|\[.*?\]|\{.*?\}", "", text)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (replace parentheses)",end-start)

        start = time.time()
        for i in self.entIndex:

            text = re.sub(fr"\b{i}\b", "", text)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (replace entity)",end-start)


        toks = selectTokenizer("wsp", text.lower()).returnList()
        self.ug = createUnigram(toks, 15)
        self.bg = createBigram(toks, 15)
        self.tg = createTrigram(toks, 15)
        start = time.time()
        findWord(self)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (findword)",end-start)

        start = time.time()
        checkSafe(self)
        end = time.time()
        print("/*/*/*/*/*/ Elapsed time (checksafe)",end-start)
        endX = time.time()
        print("<><><><><><><><><><><><><> Elapsed time (setup)",endX-startX)
            
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
        #print(">>>>LOG -tcl input:", tk)
        line = int(str(tk).split(".")[0])
        col = int(str(tk).split(".")[1])
        
        if line != 1:
            #print(">>>> line={}, col={}, x={}, line-(x+2)={}".format(line,col,x, line-(x+2)))

            out = col + self.newline[line-(x+2)]
            #print("out=", out)
            #print("newline",self.newline)
            return(out)
        else:
            return(col)
    def highlightAble(self, start):
        for i in self.DoNotHighLight:
            if start in range(i[0],i[1]):
                print("HAB:",start,i[0],i[1])
                return 0
        return 1
    
# Test comment sar
# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
