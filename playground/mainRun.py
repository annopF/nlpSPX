# import required module
from encodings import utf_8
import os
from ngram import *
# assign directory

directory = "F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/ieltsText/"
 
# iterate over files in
# that directory
for filename in os.scandir(directory):
    text = open("F:/Work Folder/KMUTT/SeniorProject/nlpSPX/dataset/ieltsText/",encoding="UTF-8").read()
    tok = selectTokenizer("spa",text)
    bigram("nb",10) 
 