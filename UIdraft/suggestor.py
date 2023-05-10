from Putil import isStopword
from tokenizer import selectTokenizer
from PmainLoop import makeOutput
from tkinter import Button, Label
import inter_values
from inter_values import replacement


class NgramIndex():
    def __init__(self):
        self.word = []
        self.start = []
        self.end = []

    def list_child(self):
        print("Word:")
        for obj in self.word:
            print(obj)
        print("Start:")
        for obj in self.start:
            print(obj)
        print("End:")
        for obj in self.end:
            print(obj)


# CONTINUE: Change highlight color on click
def on_highlight_click(textbox, suggestionbox, event, parser):
    print("----------------------------------HIGHLIGHT CLICK----------------------------------")
    # destroy all buttons if any
    inter_values.suggested_words.clear()
    inter_values.suggestion_clear(suggestionbox)
    textbox.tag_remove("highlight-clicked", 1.0, "end-1c")

    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('highlight'))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            # return string between tag start and end
            word = event.widget.get(start, end)
            print("INPUT --> ", word, start, end)

            textbox.tag_add("highlight-clicked", start, end)

            inter_values.original_word = word

            word_output = text_split(word, str(start))
            word_output.list_child()

            def tclToInt(tcl):
                return int(str(tcl)[slice(2, len(str(tcl)))])

            def getPrevious(start, i):
                tcl = int(str(start).split(".")[0])
                previous = event.widget.get(f"{tcl - 1}.0", f"{tcl - 1}.0 lineend")
                count = i
                if previous != "":
                    return (count)
                else:
                    count += 1
                    return (getPrevious(tcl - 1, count))

            count = getPrevious(start, 0)

            def whatGram(input):
                return (parser.getGram(len(str(input).split(" "))))

            for xg in whatGram(word):
                out = []

                a = xg.getParentSentence(parser.cvtIndex(start, count), str(word).lower().strip(), count)
                if a:

                    print("!!---> a.sentID, start, end", a.sentId, a.start, a.end)

                    senOG = list(parser.doc.sents)[a.sentId]
                    for i in range(xg.type):
                        if not isStopword(xg.getGram(i + 1)):
                            out.append([str(senOG).strip(),
                                        selectTokenizer("wsp", str(senOG)).replaceAt(a.geti(i + 1), None),
                                        xg.getGram(i + 1)])

                if len(out) != 0:
                    print(out)
                    print("calling suggestor makeOutput()")
                    makeOutput(out)
                    Label(suggestionbox, bg="white", text="Word 1", font="18").grid(row=1, column=0, sticky="we")
                    for idx, suggested_word in enumerate(inter_values.suggested_words[0]):
                        # May change to idx+1 since there's temp ignore all button placed
                        Button(suggestionbox, text=suggested_word,
                               command=lambda w=suggested_word,
                                              s=word_output.start[0],
                                              e=word_output.end[0]: selected_word(w, s, e)) \
                            .grid(row=idx + 2, column=0, sticky="s")
                        print("Created button for word 1: ", suggested_word)

                    if len(inter_values.suggested_words) == 2:
                        Label(suggestionbox, bg="white", text="Word 2", font="18").grid(row=1, column=1, sticky="we")
                        for idx, suggested_word in enumerate(inter_values.suggested_words[1]):
                            # May change to idx+1 since there's temp ignore all button placed
                            Button(suggestionbox, text=suggested_word,
                                   command=lambda w=suggested_word,
                                                  s=word_output.start[1],
                                                  e=word_output.end[1]: selected_word(w, s, e)) \
                                .grid(row=idx + 2, column=1, sticky="s")
                            print("Created button for word 2: ", suggested_word)

                else:
                    print("EMPTY!")
                    # inter_values.suggested_words.append([])


def selected_word(word, start, end):
    print("Replace ", inter_values.original_word, " with ", word, " to position --> ", start, end)
    replacement.add_replace(word, start, end)
    return


def text_split(input_word, start):
    output = NgramIndex()
    # print(start)
    words = input_word.split()
    start = start.split(".")
    # print(start)

    line = start[0]
    current_idx = int(start[1])

    for word in words:
        output.word.append(word)
        output.start.append(".".join([line, str(current_idx)]))  # Putting [] outside join means it sets itself
        current_idx += len(word)
        output.end.append(".".join([line, str(current_idx)]))
        current_idx += 1  # Space bar
    return output
