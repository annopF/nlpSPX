from Putil import isStopword
from tokenizer import selectTokenizer 
from PmainLoop import makeOutput


# CONTINUE: Change highlight color on click
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
            word = event.widget.get(start,end)
            print("------> ", word, start, end)
           
            ###### CALL SUGGESTION FUNCTION ######
            def tclToInt(tcl):
                return int(str(tcl)[slice(2,len(str(tcl)))])
            
            def whatGram(input):
                return (parser.getGram(len(str(input).split(" "))))
            
            for xg in whatGram(word):
                out = []
                
                a = xg.getParentSentence(tclToInt(start), str(word).lower().strip())
                if a:
                    senOG = list(parser.doc.sents)[a.sentId]
                    for i in range(xg.type):
                        print(i)
                        if not isStopword(xg.getGram(i+1)):
                            out.append([str(senOG),
                                        selectTokenizer("wsp",str(senOG)).replaceAt(a.geti(i+1),None),
                                        xg.getGram(i+1)])
                            
                if len(out)!=0:
                    print(out)
                    print("calling suggestor makeOutput()")
                    makeOutput(out)
