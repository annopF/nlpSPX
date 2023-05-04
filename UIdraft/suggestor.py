from Putil import isStopword
from tokenizer import selectTokenizer 
from PmainLoop import makeOutput
import tkinter
from tkinter import Button, Label
import inter_values


# CONTINUE: Change highlight color on click
def callback(suggestionbox, event,parser):
    # destroy all buttons if any
    inter_values.suggested_words.clear()
    for widget in suggestionbox.winfo_children():
        if isinstance(widget, tkinter.Button):
            widget.destroy()

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
            def tclToInt(tcl):
                return int(str(tcl)[slice(2,len(str(tcl)))])
            
            def getPrevious(start,i):
                tcl = int(str(start).split(".")[0])
                previous = event.widget.get(f"{tcl-1}.0",f"{tcl-1}.0 lineend")
                count = i
                if previous != "":
                    return(count)
                else:
                    count +=1
                    return (getPrevious(tcl-1,count))
                    
            count = getPrevious(start,0)

            def whatGram(input):
                return (parser.getGram(len(str(input).split(" "))))
            
            for xg in whatGram(word):
                out = []
                
                a = xg.getParentSentence(parser.cvtIndex(start,count), str(word).lower().strip())
                if a:

                    print("!!---> a.sentID, start, end", a.sentId, a.start, a.end)
                    
                    senOG = list(parser.doc.sents)[a.sentId]
                    for i in range(xg.type):
                        if not isStopword(xg.getGram(i+1)):
                            out.append([str(senOG).strip(),
                                        selectTokenizer("wsp",str(senOG)).replaceAt(a.geti(i+1),None),
                                        xg.getGram(i+1)])
                            
                if len(out)!=0:
                    print(out)
                    print("calling suggestor makeOutput()")
                    makeOutput(out)
                    Label(suggestionbox, bg="white", text="Word 1", font="18").grid(row=1, column=0, sticky="we")
                    for idx, word in enumerate(inter_values.suggested_words[0]):
                        # May change to idx+1 since there's temp ignore all button placed
                        Button(suggestionbox, text=word).grid(row=idx+2, column=0, sticky="s")

                    if len(inter_values.suggested_words) == 2:
                        Label(suggestionbox, bg="white", text="Word 2", font="18").grid(row=1, column=1, sticky="we")
                        for idx, word in enumerate(inter_values.suggested_words[1]):
                            # May change to idx+1 since there's temp ignore all button placed
                            Button(suggestionbox, text=word).grid(row=idx + 2, column=1, sticky="s")

                else:
                    print("EMPTY!")
