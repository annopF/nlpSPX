# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"[A-Z]\.?(\w+\.){1,}|(\w+-)+\w+|\w+('s|'t|'ve|'re|'ll|'d)|[A-Za-z0-9]+"
test_str = open("F:/Work Folder/KMUTT/NLP/codingAssNLP/simpletext.txt",encoding="UTF-8").read() 

matches = re.finditer(regex, test_str, re.MULTILINE)

x = [ match.group() for matchNum, match in enumerate(matches, start=1)]

print (x)
    
    
 

