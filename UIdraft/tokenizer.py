#THIS IS TOKENIZER 
import re
import nltk
from nltk.collocations import *
from nltk.tokenize import *
from nltk import *

class tok():
    def __init__(self,token):
        self.token = token

    def replaceAt(self,idx, new):
        temp = self.token

        for i in range(len(temp)):

            if i == idx:
                if new != None:
                    temp[i] = new
                else:
                    temp[i] = "<mask>"
                
                return(" ".join(temp))
    
    def returnList(self):
        return(self.token)
    
#using pure regex tokenizer (use www.regex101.com to test)
def tokenizerXUltra (input):

    #regex = r"[A-Z]\.?(\w+\.){1,}|(\w+-)+\w+|\w+('s|'t|'ve|'re|'ll|'d)|[A-Za-z0-9]+" #regex V1.0
    regex = r"\W?\d+\.?\d+|[A-Z]\.?(\w+\.){1,}|(\w+-)+\w+|\w+('s|'t|'ve|'re|'ll|'d)|[\w\d]+" #regex V1.1 (support for decimal and $sign)

    matches = re.finditer(regex, input, re.MULTILINE)

    return [ match.group() for matchNum, match in enumerate(matches, start=1)]

def selectTokenizer(name, input):
    match name:
        case "w": 
            print("-------------------------------------------------using word tokenizer")
            return (nltk.word_tokenize(input))

        case "wsp": 
            #print("-------------------------------------------------using whitesapce tokenizer")
            sd  = input.split()
            out = [x.rstrip(".").rstrip(",") for x in sd]
            return (tok([x for x in out if x != '']))

        case "pun":
            print("-------------------------------------------------using punctuation tokenizer")
            return (nltk.wordpunct_tokenize(input))

        case "regxBasic":
            print("-------------------------------------------------using regex tokenizer")
            return (nltk.regexp_tokenize(input,"\w+"))

        case "regxUltra":
            # print("-------------------------------------------------using regxUltra tokenizer")

            return(tokenizerXUltra(input))

