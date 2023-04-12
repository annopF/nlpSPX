import spacy

# import sys
# sys.path.append("./playground")

from tokenizer import *
from createNgram import *
from Putil import isStopword


class parse():
    def __init__(self):
         self.doc = None
         self.entIndex = None
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
        def findEnt(self):
            
            for ent in doc.ents:
                 self.entIndex.append(ent.start_char)

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
                 
        nlp = spacy.load("en_core_web_lg")
        
        doc = nlp(text.replace("\n", "").replace("\r", ""))
        self.entIndex = doc.ents
        self.doc = doc
        text = str(doc)
        text = re.sub("\(.*?\)|\[.*?\]|\{.*?\}","",text)
        for i in self.entIndex:
            text = re.sub(fr"\b{i}\b","",text)

        toks = selectTokenizer("wsp", text.lower()).returnList() 
       
        self.ug = createUnigram(toks,40)
        self.bg = createBigram(toks,40)
        self.tg = createTrigram(toks,40)
        
        findWord(self)
        checkSafe(self)


    def getRes(self,start):
        
        for item in self.bg:
            a = item.getParentSentence(start)
            if a:
                return(list(self.doc.sents)[a.getSentId()])
            else:
                 return 0
      
    
    def scantexts(self):
        toks = []
        
        topwords = [(x.gram1+" "+x.gram2,x.count) for x in self.bg if x.safe]
        return toks, topwords

         

# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
