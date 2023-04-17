import re
import suggestor


def findtext_inthebox(textbox, target,parser):
    line_count = int(textbox.index('end').split('.')[0]) - 1  # returns line count(not index)
    print(line_count)

    # List of inp according to textbox 'lines'
    inp = []

    # inp is updated every time you click the button
    # inp = textbox.get(1.0, "end-1c")    # end is end, -1c will delete 1 last char(newline)
    # inp = textbox.get("1.0", "1.0 lineend")
    textbox.tag_configure('highlight', background='red', font='lucida 20 bold underline')
    textbox.tag_bind("highlight", "<Button-1>", lambda event: (suggestor.callback(event, parser)))
    textbox.tag_remove("highlight", 1.0, "end-1c")

    # get all the lines in the text
    for i in range(line_count):
        inp.append(textbox.get(f"{i+1}.0", f"{i+1}.0 lineend"))

    # console  
    # print(inp)
    # print(type(inp))

    pattern = re.compile(fr"\b{target.lower()}\b")

    #console
    # print(pattern)

    # for all lines(list)
    for idx, line in enumerate(inp):
        for m in pattern.finditer(line.lower()):
            # console
            print(m.group(), f'{idx + 1}.{m.start()}', f'{idx + 1}.{m.end()}', type(m.group()), type(m.start()),
                  type(m.end()))

            # textbox.tag_add('highlight', f'1.{m.start()}', f'1.{m.end()}')  # line, text index

            textbox.tag_add('highlight', f'1.{m.start()}', f'1.{m.end()}')

    return

def buttonPress(func, *args):
    value = func(*args)

def list_highlights(textbox):
    highlights = textbox.tag_ranges("highlight")

    for i in range(0, len(highlights), 2):
        print("TX",highlights[i], highlights[i+1])
    return
