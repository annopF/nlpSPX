from tkinter import *
from tkinter.filedialog import *

import textreader
import highlighter
from Pparse import parse

# GLOBAL VARIABLE(be careful if it goes to other files)
scanoutput = []

# Generate window
root = Tk()
root.title("Draft GUI")
root.geometry("1280x720")
root.resizable(width=False, height=False)

# Initialize and config labels before functions
# # Menubar
menubar = Menu()
menubar_file = Menu()
menubar_edit = Menu()
root.config(menu=menubar)

# # Main frame(The most outside)
mainframe = Frame(root, bg="green")

# # Navbar
navbar = Frame(mainframe, height=60, padx=10, pady=10, bg="white")
scan_btn = Button(navbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE, command=lambda: scan_texts(text))
navbar_border = Canvas(mainframe, height=0, highlightbackground="#d8d8d8",
                       highlightthickness="0.5")  # fake bottom border

# # Workspace
workspace = Frame(mainframe, bg="red")
workspace.grid_columnconfigure(0, weight=7)
workspace.grid_columnconfigure(1, weight=2)
workspace.grid_rowconfigure(0, weight=1)  # full height since no others rowconfigure
# # # Paper
textarea = Frame(workspace, bg="#ebeff8")
text = Text(textarea, font=("Ink Free", 16), padx=10, pady=10, relief=FLAT)
# # # Sidebar
sidebar = Frame(workspace, bg="green")
sidebar.grid_columnconfigure(0, weight=1)
sidebar.grid_rowconfigure(0, weight=1)
sidebar.grid_rowconfigure(1, weight=1)

repeatedword = Frame(sidebar, bg="white", highlightbackground="#d8d8d8", highlightthickness="1")
repeatedword.grid_columnconfigure(0, weight=1)
repeatedword_header = Label(repeatedword, bg="white", text="Most repeated word", padx=20, pady=15, font="24")

suggestion = Frame(sidebar, bg="white", highlightbackground="#d8d8d8", highlightthickness="1")
suggestion.grid_columnconfigure(0, weight=1)
suggestion_header = Label(suggestion, bg="white", text="Suggestions", padx=20, pady=15, font="24")


# Functions
def select_file():
    selectedfile = askopenfilename()
    if not selectedfile:
        return
    inputtext = textreader.readtext(selectedfile)
    text.insert(INSERT, inputtext)


def scan_texts(inputtextbox):
    inp = inputtextbox.get(1.0, "end-1c")
    if inp != "":
        parser = parse()
        parser.setUp(inp)
        pp = parser.scantexts()

        print("PP",pp)
        global scanoutput
        scanoutput = pp
        # create buttons for most repeated word
        global topwords
        for idx, i in enumerate(scanoutput[1]):
            # pack(fill='x', side=TOP)
            print("texti[0]",i[0])
            Button(repeatedword, text=i[0], command=lambda x=i[0]: highlighter.findtext_inthebox(text, x, parser))\
                .grid(row=idx+1, column=0)
    return ()


# Place default labels
# # Menubar
menubar.add_cascade(label="File", menu=menubar_file)
menubar_file.add_command(label="New")
menubar_file.add_command(label="Open", command=select_file)
menubar_file.add_command(label="Save")
menubar_file.add_command(label="Save as")
menubar_file.add_command(label="Settings")

# # Main frame(The most outside)
mainframe.pack(expand=True, fill=BOTH)

# # Navbar
navbar.pack(fill='x')
scan_btn.grid(row=0, column=0)
navbar_border.pack(fill='x')

# # Workspace
workspace.pack(expand=True, fill=BOTH)
# # # Paper
textarea.grid(row=0, column=0, sticky="nsew")
text.place(relwidth= 0.5, relx=0.5, rely=0.5, anchor=CENTER)
# # # Sidebar
sidebar.grid(row=0, column=1, sticky="nsew")
sidebar.grid_propagate(False)

repeatedword.grid(row=0, column=0, sticky="nsew")
repeatedword.grid_propagate(False)
repeatedword_header.grid(row=0, column=0, sticky="w")  # Note: grid also has padx,y function with tuples(padx=(10, 10))

suggestion.grid(row=1, column=0, sticky="nsew")
suggestion.grid_propagate(False)
suggestion_header.grid(row=0, column=0, sticky="w")

# Launch GUI(last)
root.mainloop()

print("final: ", )