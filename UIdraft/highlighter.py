import re
import suggestor


def findtext_inthebox(textbox, target,bg, dox):
    inp = textbox.get(1.0, "end-1c")    # end is end, -1c will delete 1 last char(newline)
    textbox.tag_configure('highlight', background='red', font='lucida 20 bold underline')
    textbox.tag_bind("highlight", "<Button-1>", lambda event:(suggestor.callback(event,bg, dox)))
    textbox.tag_remove("highlight", 1.0, "end-1c")
    # console  
    # print(inp)
    # print(type(inp))

    pattern = re.compile(fr"\b{target}\b")

    #console
    # print(pattern)

    for m in pattern.finditer(inp):

        # console
        # print(m.group(), m.start(), m.end(), type(m.group()), type(m.start()), type(m.end()))

        textbox.tag_add('highlight', f'1.{m.start()}', f'1.{m.end()}')  # line, text index

    return

def buttonPress(func, *args):
    value = func(*args)

def list_highlights(textbox):
    highlights = textbox.tag_ranges("highlight")

    for i in range(0, len(highlights), 2):
        print("TX",highlights[i], highlights[i+1])
    return
