from Putil import isStopword
from tokenizer import selectTokenizer
from PmainLoop import makeOutput
from tkinter import Button, Label, Frame
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

            print("what gram: ", whatGram(word))
            out = []
            for xg in whatGram(word):

                a = xg.getParentSentence(parser.cvtIndex(start, count), str(word).lower().strip(), count)
                if a:

                    print("!!---> a.sentID, start, end", a.sentId, a.start, a.end)

                    senOG = list(parser.doc.sents)[a.sentId]
                    # print("sendOG", senOG)
                    # print(range(0, xg.type))
                    for i in range(0, xg.type):
                        # print("ROUND: ", i)
                        if not isStopword(xg.getGram(i + 1)):
                            out.append([str(senOG).strip(),
                                        selectTokenizer("wsp", str(senOG)).replaceAt(a.geti(i + 1), None),
                                        xg.getGram(i + 1)])
                            print(out)
                            print("calling suggestor makeOutput()")
                            makeOutput(out[i])     # Check similar word and append list
                        else:
                            out.append([])
                            inter_values.suggested_words.append([])     # Append empty list
                        # print(inter_values.suggested_words)
                        # print(len(inter_values.suggested_words))
                        # print("ENDED ROUND: ", i)

            if len(out) != 0:
                row_count1 = {}
                row_count2 = {}
                row_count3 = {}
                print(len(inter_values.suggested_words))
                print("SUGGESTED WORD LIST", inter_values.suggested_words)
                if len(inter_values.suggested_words[0]) != 0:
                    Label(suggestionbox, bg="white", text="Word 1", font="18").grid(row=1, column=0,
                                                                                    padx=10, sticky="w")
                    word1_frame = Frame(suggestionbox, bg="red")
                    word1_frame.grid_columnconfigure(0, weight=1)
                    word1_frame.grid(row=2, column=0, sticky="we")
                    wrap_btn_place(word1_frame, inter_values.suggested_words, word_output, row_count1, 0)
                # for idx, suggested_word in enumerate(inter_values.suggested_words[0]):
                #     # May change to idx+1 since there's temp ignore all button placed
                #     Button(suggestionbox, text=suggested_word,
                #            command=lambda w=suggested_word,
                #                           s=word_output.start[0],
                #                           e=word_output.end[0]: selected_word(w, s, e)) \
                #         .grid(row=2, column=idx, sticky="w")
                #     print("Created button for word 1: ", suggested_word)

                if len(inter_values.suggested_words) >= 2:
                    if len(inter_values.suggested_words[1]) != 0:
                        Label(suggestionbox, bg="white", text="Word 2", font="18").grid(row=3, column=0,
                                                                                        padx=10, sticky="w")
                        word2_frame = Frame(suggestionbox, bg="red")
                        word2_frame.grid_columnconfigure(0, weight=1)
                        word2_frame.grid(row=4, column=0, sticky="we")
                        wrap_btn_place(word2_frame, inter_values.suggested_words, word_output, row_count2, 1)

                    if len(inter_values.suggested_words) == 3:
                        if len(inter_values.suggested_words[2]) != 0:
                            Label(suggestionbox, bg="white", text="Word 3", font="18").grid(row=5, column=0,
                                                                                            padx=10, sticky="w")
                            word3_frame = Frame(suggestionbox, bg="red")
                            word3_frame.grid_columnconfigure(0, weight=1)
                            word3_frame.grid(row=6, column=0, sticky="we")
                            wrap_btn_place(word3_frame, inter_values.suggested_words, word_output, row_count3, 2)


            else:
                print("EMPTY!")


def clear_last(obj):
    last = obj.winfo_children()[-1]
    last.destroy()
    return


def wrap_btn_place(parent, text_list, w_output, d_row, word_n):
    parent.update()
    width = parent.winfo_width()
    current_row = 0
    current_column = 0

    available_width = width
    # print("Start width : ", available_width)

    d_row["row{0}".format(current_row)] = Frame(parent, bg="white", padx=5)
    d_row["row{0}".format(current_row)].grid(row=current_row, column=0, sticky="we")
    for txt in text_list[word_n]:
        text_btn = Button(d_row["row{0}".format(current_row)], text=txt,
                          command=lambda w=txt,
                                         s=w_output.start[word_n],
                                         e=w_output.end[word_n]: selected_word(w, s, e))
        text_btn.grid(row=0, column=current_column, padx=5, pady=5)
        text_btn.update()
        using_width = text_btn.winfo_width()
        if available_width-10 < using_width+10:
            clear_last(d_row["row{0}".format(current_row)])
            available_width = width
            current_row += 1
            d_row["row{0}".format(current_row)] = Frame(parent, bg="white", padx=5)
            d_row["row{0}".format(current_row)].grid(row=current_row, column=0, sticky="we")
            text_btn = Button(d_row["row{0}".format(current_row)], text=txt,
                                   command=lambda w=txt,
                                                  s=w_output.start[word_n],
                                                  e=w_output.end[word_n]: selected_word(w, s, e))
            current_column = 0
            text_btn.grid(row=0, column=current_column, padx=5, pady=5)
            available_width -= using_width+10
            # print("placed button at: ", current_row, current_column)
            # print("Available: ", available_width)
            current_column += 1
        else:
            text_btn.grid(row=0, column=current_column)
            available_width -= using_width+10
            # print("placed button at: ", current_row, current_column)
            # print("Available: ", available_width)
            current_column += 1


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
