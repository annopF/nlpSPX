import tkinter
from tkinter import *
from tkinter.filedialog import *

import textreader
import highlighter
import inter_values
from Pparse import parse


# GLOBAL VARIABLE(be careful if it goes to other files)
INPUT_TEXT = []
SCAN_OUTPUT = []
CURRENT_PAGE_IDX = 0

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
navbar.grid_columnconfigure(0, weight=1)
navbar.grid_columnconfigure(1, weight=5)
navbar.grid_columnconfigure(2, weight=1)
navbar.grid_columnconfigure(3, weight=6)
navbar.grid_columnconfigure(4, weight=7)
scan_btn = Button(navbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE, command=lambda: scan_texts(text))
prev_pg_btn = Button(navbar, text="Previous", command=lambda: previous_page(text))
page_label = Label(navbar, text="Page x / y")
next_pg_btn = Button(navbar, text="Next", command=lambda: next_page(text))
navbar_border = Canvas(mainframe, height=0, highlightbackground="#d8d8d8",
                       highlightthickness="0.5")  # fake bottom border

# # Workspace
workspace = Frame(mainframe, bg="red")
workspace.grid_columnconfigure(0, weight=7)
workspace.grid_columnconfigure(1, weight=2)
workspace.grid_rowconfigure(0, weight=1)  # full height since no others rowconfigure
# # # Paper
textarea = Frame(workspace, bg="#ebeff8")
text_scroll = Scrollbar(textarea)
text = Text(textarea, font=("Ink Free", 16), padx=10, pady=10, relief=FLAT
            , yscrollcommand=text_scroll.set, wrap=WORD)
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
suggestion_wordlist = Frame(suggestion, bg="white")
suggestion_wordlist.grid_columnconfigure(0, weight=1)
suggestion_wordlist.grid_columnconfigure(1, weight=1)
ignore_all_btn = Button(suggestion, text="Ignore all", command=lambda: dummy_print())


# Functions
def select_file():
    selectedfile = askopenfilename()
    if not selectedfile:
        return

    global INPUT_TEXT
    INPUT_TEXT = textreader.readtext(selectedfile)
    # INPUT_TEXT = textreader.nopreadtext(selectedfile)
    text.insert(INSERT, INPUT_TEXT[0])      # INSERT, END defines direction to insert text


def scan_texts(inputtextbox):
    inp = inputtextbox.get(1.0, "end-1c")
    if inp != "":
        inputtextbox.tag_remove("highlight", 1.0, "end-1c")
        destroy_all_buttons(repeatedword)
        parser = parse()
        parser.setUp(inp)
        pp = parser.scantexts()
        for i in parser.ug:
            print(i.gram1,i.count)
        for i in parser.bg:
            print(i.gram1, i.gram2, i.count)
        
        print("PP", pp)
        global SCAN_OUTPUT
        SCAN_OUTPUT = pp
        # create buttons for most repeated word
        for idx, i in enumerate(SCAN_OUTPUT[1]):
            # pack(fill='x', side=TOP)
            print(f"text[{idx}]", i[0])
            Button(repeatedword, text=i[0], command=lambda x=i[0]: highlighter.findtext_inthebox(text, suggestion_wordlist, x, parser))\
                .grid(row=idx+1, column=0)
    return ()


# Need more? condition check
def previous_page(textbox):
    global INPUT_TEXT
    global CURRENT_PAGE_IDX

    page_length = len(INPUT_TEXT)

    if CURRENT_PAGE_IDX in range(1, page_length):       # prev page is available when cur_pg is at idx 1 to last
        destroy_all_buttons(repeatedword)
        INPUT_TEXT[CURRENT_PAGE_IDX] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, INPUT_TEXT[CURRENT_PAGE_IDX - 1])
        CURRENT_PAGE_IDX -= 1
        print("Showed page ", CURRENT_PAGE_IDX+1, ' / ', page_length)

    return


def dummy_print():
    print(type(inter_values.suggested_words))
    print("Current: ", inter_values.suggested_words)
    highlighter.list_highlights(text)
    # Return text, and then what about MULTIPLE WORDS
    return


def next_page(textbox):
    global INPUT_TEXT
    global CURRENT_PAGE_IDX

    page_length = len(INPUT_TEXT)

    if CURRENT_PAGE_IDX in range(0, page_length-1):       # next page is available when cur_pg is at idx 0 to last-1
        destroy_all_buttons(repeatedword)
        INPUT_TEXT[CURRENT_PAGE_IDX] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, INPUT_TEXT[CURRENT_PAGE_IDX + 1])
        CURRENT_PAGE_IDX += 1
        print("Showed page ", CURRENT_PAGE_IDX+1, ' / ', page_length)

    return


def destroy_all_buttons(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tkinter.Button):
            widget.destroy()
    return

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
scan_btn.grid(row=0, column=0, sticky="w")
# CONTINUE: Add page number
prev_pg_btn.grid(row=0, column=1, sticky="e", padx=(0, 5))
page_label.grid(row=0, column=2, sticky="nsew")
next_pg_btn.grid(row=0, column=3, sticky="w", padx=(5, 0))
navbar_border.pack(fill='x')

# # Workspace
workspace.pack(expand=True, fill=BOTH)
# # # Paper
textarea.grid(row=0, column=0, sticky="nsew")
text_scroll.pack(side=RIGHT, fill='y')
text.place(relwidth= 0.5, relx=0.5, rely=0.5, anchor=CENTER)
# # # Sidebar
sidebar.grid(row=0, column=1, sticky="nsew")
sidebar.grid_propagate(False)

repeatedword.grid(row=0, column=0, sticky="nsew")
repeatedword.grid_propagate(False)
repeatedword_header.grid(row=0, column=0, sticky="w")
suggestion.grid(row=1, column=0, sticky="nsew")
suggestion.grid_propagate(False)
suggestion_header.grid(row=0, column=0, sticky="w")
suggestion_wordlist.grid(row=1, column=0, sticky="nsew")
ignore_all_btn.grid(row=2, column=0, sticky="s")    # PUT command=function_name HERE

# Configure scrollbar
text_scroll.config(command=text.yview)

# Launch GUI(last)
root.mainloop()

# BABUU
print("final: ", )