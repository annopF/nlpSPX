class sentenceX():
    def __init__(self, sentId, i1,i2,i3, start, end):
        self.sentId = sentId
        self.start = start
        self.end = end
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        

  

    def geti(self,idx):
        match idx:
            case 1:
                return self.i1
            case 2:
                return self.i2
            case 3:
                return self.i3
    
class ngram():

    def __init__(self, gram1, gram2, gram3, count):
        self.gram1 = gram1
        self.gram2 = gram2
        self.gram3 = gram3
        self.count = count
        self.sentenceObj = []
        self.type = None
        self.concat = None
        self.safe = True #True if not all grams are stopword (they are -> False, is the -> False, the rule -> True, the people -> True)

    def printData(self):
        for i in self.sentenceObj:
            print("gram1",self.gram1, "gram2",self.gram2, "count",self.count,"sentID",i.getSentId(),"geti1",i.geti(1), "geti2",i.geti(2),"start",i.getStart(),"end",i.getEnd())

    def getGram(self,idx):
        match idx:
            case 1:
                return self.gram1
            case 2:
                return self.gram2
            case 3:
                return self.gram3
    def getConcat(self):
        return(self.concat)
    def getSentObj(self):
        return self.sentenceObj
    
    def getParentSentence(self,start,gram1, gram2):
        for item in self.sentenceObj:
            if self.gram1 == gram1 and self.gram2 == gram2 and start in range(item.start, item.end):
                return(item)
        return(0)

    
class unigram(ngram):
    def __init__(self,gram1, count):
        super().__init__(gram1,None, None, count)
        self.concat = gram1
        self.type = 1
    def show(self):
        print(self.gram1, self.count)

class bigram(ngram):
    def __init__(self,gram1, gram2, count):
        super().__init__(gram1, gram2, None, count)
        self.concat = gram1+" "+gram2
        self.type = 2
    def show(self):
        print(self.gram1, self.gram2, self.count)

class trigram(ngram):
    def __init__(self,gram1, gram2, gram3, count):
        super().__init__(gram1, gram2,gram3, count)
        self.concat = gram1+" "+gram2+" "+gram3
        self.type = 3   

    def show(self):
        print(self.gram1, self.gram2, self.gram3, self.count)


  