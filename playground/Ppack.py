import spacy
import textract as tt
from tokenizer import selectTokenizer
from ngram import *
from Putil import nicePrint, isStopword



    
#change file path here
def generateText(mode):
    if mode == 1:
        filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/pdfFile/f14.pdf"
        text = tt.process(filePath)
        texts = text.decode("utf8")
        return(texts)
    else:
        sentence = """
        I don't like Apple iPhone very much due to its price, but I don't like Apple iPhone more. 
        This apple iphone is awesome. 
        Tim like macbook pro but don't like Apple iPhone. 
        Steve job also don't like Apple iPhone. 
        Bill gate really don't like Apple product but like Samsung."""
        return(sentence)
    
    

def findWord(ug_list, bg_list, tg_list,doc):
   
   for sentId, sentence in enumerate(doc.sents):
        piece = (selectTokenizer("wsp", str(sentence))).returnList()
        for bg in bg_list:
            #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
                        
            for i,target in enumerate(piece):
                if piece[i].lower() == bg.gram2.lower() and piece[i-1].lower() == bg.gram1.lower():
                    #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                    bg.sentenceObj.append(sentenceX(sentId,i-1, i, None))

        for tg in tg_list:
            #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)
            for i,target in enumerate(piece):
                if piece[i].lower() == tg.gram3.lower() and piece[i-1].lower() == tg.gram2.lower() and piece[i-2].lower() == tg.gram1.lower():
                    #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                    tg.sentenceObj.append(sentenceX(sentId,i-2,i-1, i))

        for ug in ug_list:
            #print("---> bg1=",bg.gram1, "bg2=",bg.gram2)            
            for i,target in enumerate(piece):
                if piece[i].lower() == ug.gram1.lower():
                    #print("sentence",sentence, "#POS ", i-1, i, "#SentID ",sentId)
                    ug.sentenceObj.append(sentenceX(sentId,i,None,None))




#argument, doc = spacy doc object
def reCon(xg, sentObj ,doc):
    senOG = list(doc.sents)[sentObj.getSentId()]

    res = []
    for i in senOG:
        if i.ent_type_ != "":
            res.append(str(i))
    print("\nEntity/Stopword in this sentence:",res)


    out = []
    for i in range(xg.type):
        if not isStopword(xg.getGram(i+1)):
            if xg.getGram(i+1) not in res:
                out.append([str(senOG).strip(),selectTokenizer("wsp",str(senOG)).replaceAt(sentObj.geti(i+1),None),xg.getGram(i+1)])

    for i in out:
        print(i)
    print("---------------------------------------------------------")
    return (out)

def makeFMP(mode,xg):
    package = []
    if mode == 0:
        exit()
    elif mode == 1:
        print("--/\--/\--/\--/\--/\--/\-- MOST REPEATED WORDS --/\--/\--/\--/\--/\--/\--")
        for i in xg:
            print(i.gram1, i.count)
        
        select = input("enter unigram to search (CaSe SeNsItIvE):")


        for IDX,i in enumerate(xg):
            if i.gram1 == select:
                for j in i.sentenceObj:
                    package.append(reCon(i,j))

        return(y for x in package for y in x)

    elif mode == 2:
        print("--/\--/\--/\--/\--/\--/\-- MOST REPEATED WORDS --/\--/\--/\--/\--/\--/\--")
        for i in xg:
            print(i.gram1, i.gram2, i.count)
        
        select = input("enter bigram to search (CaSe SeNsItIvE):")
        a = select.split()


        for IDX,i in enumerate(xg):
            if i.gram1 == a[0] and i.gram2 == a[1]:
                for j in i.sentenceObj:
                    package.append(reCon(i,j))
        return(y for x in package for y in x)
    
    elif mode == 3:
        print("--/\--/\--/\--/\--/\--/\-- MOST REPEATED WORDS --/\--/\--/\--/\--/\--/\--")
        for i in xg:
            print(i.gram1, i.gram2, i.gram3, i.count)
        
        select = input("enter trigram to search (CaSe SeNsItIvE):")
        a = select.split()


        for IDX,i in enumerate(xg):
            if i.gram1 == a[0] and i.gram2 == a[1] and i.gram3 == a[2]:
                for j in i.sentenceObj:
                    package.append(reCon(i,j))
        return(y for x in package for y in x)


