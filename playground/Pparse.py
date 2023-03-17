import spacy
import textract as tt
from tokenizer import selectTokenizer
from ngram import *
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
                sent.append(sentenceObj(piece, sentId, start, end, targetIdx))
                targetIdx = []

        return(sent)
    

    #change file path here
    def generateText(mode):
        if mode == 1:
            filePath = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/pdfFile/f13.pdf"
            text = tt.process(filePath)
            texts = text.decode("utf8")
            return(texts)
        else:
            sentence = "I don't like apple because I hate banana. john chao rai I like banana due tol. I like apple becasue john chao rai i don't like banana. I like apple john chao rai becasue like apple of john chao rai iphone I like, I like. hate banana, hate banana I am sam, I am donny, I am danny I am cracker I am dark"
            return(sentence)

    texts = generateText(0)
    #texts = open(filePath, encoding="UTF-8").read()


    doc = nlp(texts.replace("\n"," ").replace("\r",""))


    #doc = nlp("i could do that and could do cake could do this but couldn't do that")



    tok = selectTokenizer("regxUltra", str(doc))

    gram = createNgram(30, tok)
    bg = gram.bigram()

    for i in bg:
        print (i.gram1, i.gram2, i.count)

    xWord = input("Enter word to search for: ")

    allMatch = findWord(xWord)

    package = []

    for idx,senObj in enumerate(allMatch):
       
        if senObj.piece != None:
            sen = list(doc.sents)[senObj.sentId]

            print("-------------------------------------------------------------------")
            print("---> sentence #",idx)
            # nicePrint(xWord,str(sen),0)
            nicePrint(xWord,str(sen),0)
            print("\r")
            if len(senObj.targetIdx) > 1:
                print(senObj.targetIdx)
                print("more than one mask found")
                pos = int(input("Choose which word to mask: "))
                senObj.piece[pos] = "<mask>"
                print("-----> new sentence: "," ".join(senObj.piece))
            else:
                senObj.piece[senObj.targetIdx[0]] = "<mask>"

            package.append([str(sen)," ".join(senObj.piece),xWord])


    return(package)


s = getPackage()

print("***************************************************************************************************")
for i in s:
    nicePrint("<mask>",i[1][0],1)
    print("\n")


    