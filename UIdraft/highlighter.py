import re
import suggestor
import inter_values
import threading

def findtext_inthebox(textbox, suggestionbox, target, parser):
    print("----------------------------------REPEATED WORDS CLICK----------------------------------")
    # destroy all buttons if any
    inter_values.suggestion_clear(suggestionbox)

    line_count = int(textbox.index('end').split('.')[0]) - 1  # returns line count(not index)

    # List of inp according to textbox 'lines'
    inp = []

    textbox.tag_bind("highlight", "<Button-1>", lambda event: threading.Thread(target = suggestor.on_highlight_click, args=(textbox, suggestionbox, event, parser)).start())
    textbox.tag_remove("highlight", 1.0, "end-1c")

    textbox.tag_remove("highlight-clicked", 1.0, "end-1c")

    # get all the lines in the text
    # inp is updated every time you click the button
    for i in range(line_count):
        inp.append(textbox.get(f"{i + 1}.0", f"{i + 1}.0 lineend"))

    # console  
    # print(inp)
    # print(type(inp))

    pattern = re.compile(fr"\b{target.lower()}\b")

    # console
    # print(pattern)
   
    

    # for all lines(list)
    for idx, line in enumerate(inp):
        for m in pattern.finditer(line.lower()):
            # console
            print("m.start()",m.start())
            if parser.highlightAble(m.start()):

                print(m.group(), f'{idx + 1}.{m.start()}', f'{idx + 1}.{m.end()}', type(m.group()), type(m.start()),
                      type(m.end()))
                textbox.tag_add('highlight', f'{idx + 1}.{m.start()}', f'{idx + 1}.{m.end()}')

    return


# def buttonPress(func, *args):
#     value = func(*args)

def list_highlights(textbox):
    highlights = textbox.tag_ranges("highlight")
    for i in range(0, len(highlights), 2):
        print("TX", highlights[i], highlights[i + 1])
    return
