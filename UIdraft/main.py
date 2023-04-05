from tkinter import *
from tkinter.filedialog import *

# import sys
# sys.path.append('./functions')
import textreader
import highlighter
import Pparse
import re

# GLOBAL VARIABLE(be careful if it goes to other files)
scanoutput = []

root = Tk()
root.title("Draft GUI")
root.geometry("1280x720")
root.resizable(width=False, height=False)


# ##Initialize labels(not placed yet)## #
mainframe = Frame(root, bg="#ebeff8")
sidebar = Frame(mainframe, width=250, bg="green", highlightbackground="#d8d8d8", highlightthickness="2")
sbframe1 = Frame(sidebar, bg="red")
sbhead1 = Label(sidebar, bg="yellow", text="Most repeated word", padx=50, pady=10, font="24")
sbframe2 = Label(sidebar, bg="blue")
sbhead2 = Label(sidebar, bg="yellow", text="Suggestions", padx=50, pady=10, font="24")

textarea = Frame(mainframe, width=500, bg="red")
text = Text(textarea, font=("Ink Free", 16), padx=10, pady=10, relief=FLAT)

toolbar = Frame(root, height=60, padx=10, pady=10, bg="white", highlightbackground="#d8d8d8", highlightthickness="2")
scanbtn = Button(toolbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE,
                 command=lambda: scan_texts(text))  # scan text


# ##Function## #
def select_file():
    selectedfile = askopenfilename()
    if not selectedfile:
        return
    inputtext = textreader.readtext(selectedfile)
    text.insert(INSERT, inputtext)


def scan_texts(inputtextbox):
    inp = inputtextbox.get(1.0, "end-1c")
    if inp != "":
        pp = Pparse.scantexts(inp)
        global scanoutput
        scanoutput = pp

        # create buttons for most repeated word
        global topwords
        for idx, i in enumerate(scanoutput[1]):
            # pack(fill='x', side=TOP)
            Button(sbframe1, text=i[0], command=lambda x=i[0]: highlighter.findtext_inthebox(text, x)).pack(side=TOP)
    return


# ##Menu(toolbar)## #
myMenu = Menu()
fileItem = Menu()
editItem = Menu()
root.config(menu=myMenu)

myMenu.add_cascade(label="File", menu=fileItem)
fileItem.add_command(label="New")
fileItem.add_command(label="Open", command=select_file)
fileItem.add_command(label="Check", command=lambda: highlighter.list_highlights(text))
fileItem.add_command(label="Save")
fileItem.add_command(label="Save as")
fileItem.add_command(label="Settings")

myMenu.add_cascade(label="Edit")
editItem.add_command(label="Undo")
editItem.add_command(label="Redo")

# ##Toolbar## #
toolbar.pack(fill="x")
scanbtn.pack(anchor="w")

# ##Workspace## #
mainframe.pack(expand=1, fill=BOTH)

# Sidebar
sidebar.pack(fill="y", expand=True, anchor="e")
sbhead1.pack(fill='x')
sbframe1.pack(expand=1, fill=BOTH, side=TOP)
sbhead2.pack(fill='x')
sbframe2.pack(expand=1, fill=BOTH, side=BOTTOM)

# Paper(width 500)
textarea.place(x=265, relheight=1)
text.place(relwidth=1, relheight=1)

root.mainloop()
