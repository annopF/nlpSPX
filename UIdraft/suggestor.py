from Pparse import parse
from Putil import isStopword
from tokenizer import selectTokenizer 
import sys

sys.path.append("./playground")
from PmainLoop import makeOutput

def callback(event,parser):
    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('highlight'))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            # return string between tag start and end
            word = event.widget.get(start,end).split(" ")
            gram1 = word[0]
            gram2 = word[1]
            print("PACK GRAM ",gram1,start, gram2,end)

            ###### CALL SUGGESTION FUNCTION ######
            def tclToInt(tcl):
                return int(str(tcl)[slice(2,len(str(tcl)))])

            print("start:", start)
            
            for bg in parser.bg:
                out = []
                a = bg.getParentSentence(tclToInt(start), gram1.lower(), gram2.lower())
                if a:
                    senOG = list(parser.doc.sents)[a.sentId]
                    print("doc sent-->",senOG)
                    
                    for i in range(bg.type):
                        if not isStopword(bg.getGram(i+1)):
                            out.append([str(senOG).strip(),selectTokenizer("wsp",str(senOG)).replaceAt(a.geti(i+1),None),bg.getGram(i+1)])
                if len(out)!=0:
                    print(out)
                    print("calling suggestor makeOutput()")
                    makeOutput(out)
