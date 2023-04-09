import spacy
import sys
sys.path.append("./playground")
from tokenizer import *
from createNgram import *



class parse():
    def __init__(self):
         self.doc = None
         self.ug = None
         self.bg = None
         self.tg = None

    def setUp(self,text):
        def findWord(self):

            for sentId, sentence in enumerate(self.doc.sents):
                    piece = (selectTokenizer("wsp", str(sentence))).returnList()
                    for bg in self.bg:
                        #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
                                    
                        for i,target in enumerate(piece):
                            if piece[i].lower() == bg.gram2.lower() and piece[i-1].lower() == bg.gram1.lower():
                                #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                                bg.sentenceObj.append(sentenceX(sentId,i-1, i, None, sentence.start_char, sentence.end_char))

        nlp = spacy.load("en_core_web_lg")
        doc = nlp(text.replace("\n", " ").replace("\r", ""))
        toks = selectTokenizer("wsp", str(doc)).returnList() 
        self.ug = createUnigram(toks,10)
        self.bg = createBigram(toks,10)
        self.tg = createTrigram(toks,10)
        print("BGX  =", self.bg)
        self.doc = doc
        findWord(self)

    def getRes(self,start):
        
        for item in self.bg:
            a = item.getParentSentence(start)
            if a:
                return(list(self.doc.sents)[a.getSentId()])
            else:
                 return 0
      
    def getBg(self):
         return self.bg
    def getDoc(self):
         return self.doc

    def scantexts(self):
        for i in self.bg:
             i.printData()

        toks = []
        topwords = [(x.gram1+" "+x.gram2,x.count) for x in self.bg]
        return toks, topwords

         

# testunit = scantexts()
# print(testunit)
# print(type(testunit))
# print(testunit[0])
