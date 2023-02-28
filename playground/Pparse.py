import spacy
import textract as tt
from termcolor import colored, cprint
from spacy.matcher import Matcher
from tokenizer import selectTokenizer
from ngram import bigram, trigram, unigram
import re
from Putil import nicePrint



def getPackage():

    def findWord(word):
        sent = []
        targetIdx = []
        for sentId, sentence in enumerate(doc.sents):
            piece = (selectTokenizer("wsp", str(sentence)))

            for i,target in enumerate(piece):
                if target.lower() == word.lower():
                    targetIdx.append(i)
                    
            
            start = sentence.start
            end = sentence.end
            if len(targetIdx) != 0:
                sent.append([piece,start, end, sentId,targetIdx])
                targetIdx = []

        return(sent)
    
    def findWordM2(word):
        sent = []
        targetIdx = []
        for sentId, sentence in enumerate(doc.sents):
            for token in sentence:
                if str(token).lower() == word.lower():
                    targetIdx.append(i)
                    
            
            start = sentence.start
            end = sentence.end
            if len(targetIdx) != 0:
                sent.append([piece,start, end, sentId,targetIdx])
                targetIdx = []

        return(sent)

    #change file path here
    filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/pdfFile/f14.pdf"
    text = tt.process(filePath)
    texts = text.decode("utf8")
    nlp = spacy.load("en_core_web_lg")


    doc = nlp(texts.replace("\n"," ").replace("\r",""))


    #doc = nlp("i could do that and could do cake could do this but couldn't do that")



    tok = selectTokenizer("regxUltra", str(doc))
    ngram = unigram(10, tok)

    for i in ngram:
        print (i)

    xWord = input("Enter word to search for: ")

    res = findWord(xWord)

    package = []

    for idx,i in enumerate(res):
       
        if i[0] != None:
            sen = list(doc.sents)[i[3]]

            print("-------------------------------------------------------------------")
            print("---> sentence #",idx)
            nicePrint(xWord,str(sen),0)
            print("\r")
            if len(i[-1]) > 1:
                print(i[-1])
                print("shit! more than one mask found fuck u")
                pos = int(input("Choose which word to mask: "))
                i[0][pos] = "<mask>"
                print("-----> new sentence: "," ".join(i[0]))
            else:
                i[0][i[-1][0]] = "<mask>"

            package.append([[sen],[" ".join(i[0])],xWord])


    return(package)


s = getPackage()

print("***************************************************************************************************")
for i in s:
    nicePrint("<mask>",i[1][0],1)
    print("\n")


    