import numpy as np
import matplotlib.pyplot as plt

def cleanToken(token):
    stopword = ["Is","Am","Are","Was","Were","I","You","The","A","An","Of","Then","to"
    ,"As","That","It","My","This","There","So","Me","They","Do","Does","Did","Be","These",
    "Not","At","Have","Has","Had","Her","Or",""]
    stopwordLow = [x.lower() for x in stopword]
    
    return [x for x in token if x not in stopword and x not in stopwordLow]

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
  return list(dict.fromkeys([x.lower().strip() for x in inputList]))

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
