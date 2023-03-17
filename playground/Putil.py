import numpy as np
import matplotlib.pyplot as plt
import re
from termcolor import cprint


stopword = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 
                'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 
                'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
                'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 
                'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 
                'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 
                'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 
                'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 
                'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than',
                "can't","couldn't" "don't", "doesn't","isn't","won't","aren't","weren't","wouldn't","wasn't","shouldn't",""]
    
def cleanToken(token):
    
    return [x for x in token if x.lower() not in stopword and x not in stopword]
def isStopword(token):
    if token.lower() in stopword:
        return (1)
    else:
        return (0)
    
def levDistance(str1,str2):

    array = [[0]*(len(str2)+1) for i in range(len(str1)+1)]

    for i in range(len(str1) + 1):
        array[i][0] = i

    for j in range(len(str2) + 1):
        array[0][j] = j

    for i in range(1,len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j - 1]:
                array[i][j] = array[i-1][j-1]
            else:
                array[i][j] = 1 + min(array[i - 1][j], array[i][j - 1], 1+array[i-1][j-1])


    return (array[-1][-1])

def cleanDup(inputList):
    out  =[]

    for item in inputList:
        if item not in out:
            out.append(item)

    return out

def plotFreq(word_count,vocab):

    y_pos = np.arange(len(vocab))
    fig, plot = plt.subplots()


    plot.barh(y_pos,word_count)
    plot.set_yticks(y_pos)
    plot.set_yticklabels(vocab)
    plot.invert_yaxis()  # labels read top-to-bottom
    plot.set_xlabel('occurrence')
    plot.set_ylabel('vocab')

    plot.set_title("Most repeated words in the document")


    plt.show()


#highlight selected words in the text and print out nicely

#INPUT arg1: word = word to highlight
#      arg2: sen = sentence containing the words to highlight
#      arg3: mode: 0=when use with normal word, 1=when use with <mask>
def nicePrint(word, sen, mode):
    li = []

    if mode == 0:
        for m in re.finditer(fr"(?i)\b{word}\b",sen): #use literal string inplace of r" " --> {var}
            start = m.start()
            end = m.end()
            li.append([start,end])
    elif mode == 1:
        for m in re.finditer(r"<mask>",sen): #use literal string inplace of r" " --> {var}
            start = m.start()
            end = m.end()
            li.append([start,end])

  
    idx=0
    liCounter = 0
    while idx < len(sen):  
       
        
        if len(li) == 0:
            return
        else:
            if idx == li[liCounter][0]-1:
                print("", end=" ")
                cprint(word, "green",end="")
                idx+=(li[liCounter][1]-li[liCounter][0])+1
                if liCounter != len(li)-1:
                    liCounter+=1

            else:
                print(sen[idx], end="")
                idx+=1

        