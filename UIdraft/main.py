from tkinter import *
from tkinter.filedialog import *

# import sys
# sys.path.append('./functions')
import textreader
import Pparse

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
    # filecontent = open(selectedfile, encoding="utf8")
    # filetext = filecontent.read()
    # print(filetext)


def scan_texts(inputtextbox):
    inp = inputtextbox.get(1.0, "end-1c")
    if inp != "":
        print(inp)
        pp = Pparse.scantexts(inp)
        # print(pp[1])
        # print(pp[1][0][0])
        # print(type(pp[1]))
        global scanoutput
        scanoutput = pp

        # create buttons for most repeated word
        for i in scanoutput[1]:
            # Button(sbframe1, text=i[0], command=dummy_print).pack(fill='x', side=TOP)
            Button(sbframe1, text=i, command=dummy_print).pack(fill='x', side=TOP)

    return


def print_output(input):
    print(input[1][0])
    return


def dummy_print():
    print("bruh")
    return


# ##Menu(toolbar)## #
myMenu = Menu()
fileItem = Menu()
editItem = Menu()
root.config(menu=myMenu)

myMenu.add_cascade(label="File", menu=fileItem)
fileItem.add_command(label="New")
fileItem.add_command(label="Open", command=select_file)
fileItem.add_command(label="Save", command=lambda: print_output(scanoutput))
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
sbhead1.pack()
sbframe1.pack(expand=1, fill=BOTH, side=TOP)
sbhead2.pack()
sbframe2.pack(expand=1, fill=BOTH, side=BOTTOM)

# Paper(width 500)
textarea.place(x=265, relheight=1)
text.place(relwidth=1, relheight=1)

root.mainloop()
