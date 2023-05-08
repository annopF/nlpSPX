from Putil import isStopword
from tokenizer import selectTokenizer
from PmainLoop import makeOutput
from tkinter import Button, Label
import inter_values


# CONTINUE: Change highlight color on click
def on_highlight_click(suggestionbox, event,parser):
    # destroy all buttons if any
    inter_values.suggested_words.clear()
    inter_values.suggestion_clear(suggestionbox)

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
            word_output = text_split(word, str(start))
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
                
                a = xg.getParentSentence(parser.cvtIndex(start,count), str(word).lower().strip(),count)
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
                    for idx, suggested_word in enumerate(inter_values.suggested_words[0]):
                        # May change to idx+1 since there's temp ignore all button placed
                        Button(suggestionbox, text=suggested_word,
                               command=lambda x=suggested_word, y=word_output[0][0], z=word_output[0][1]: selected_word(x, y, z)) \
                            .grid(row=idx + 2, column=0, sticky="s")

                    if len(inter_values.suggested_words) == 2:
                        Label(suggestionbox, bg="white", text="Word 2", font="18").grid(row=1, column=1, sticky="we")
                        for idx, suggested_word in enumerate(inter_values.suggested_words[1]):
                            # May change to idx+1 since there's temp ignore all button placed
                            Button(suggestionbox, text=suggested_word,
                                   command=lambda x=suggested_word, y=word_output[1][0], z=word_output[1][1]: selected_word(x, y, z))\
                                .grid(row=idx + 2, column=1, sticky="s")

                else:
                    print("EMPTY!")


def selected_word(word, start, end):
    print("Replace ", word, " to position --> ", start, end)
    inter_values.replacement.clear()
    inter_values.replacement.append(word)
    inter_values.replacement.append(start)
    inter_values.replacement.append(end)
    print(type(inter_values.replacement))
    print(inter_values.replacement)
    return


def text_split(input_word, start):
    # print(start)
    words = input_word.split()
    start = start.split(".")
    # print(start)

    line = start[0]
    start_idx = int(start[1])

    words_idx = []

    for word in words:
        idx = [".".join([line, str(start_idx)])]
        start_idx += len(word)
        idx.append(".".join([line, str(start_idx)]))
        words_idx.append(idx)
        start_idx += 1

    return words_idx
