from tkinter import *
from tkinter.filedialog import *

import textreader
import highlighter
from Pparse import parse

# GLOBAL VARIABLE(be careful if it goes to other files)
input_text = []
scan_output = []
current_page_idx = 0

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
navbar.grid_columnconfigure(1, weight=3)
navbar.grid_columnconfigure(2, weight=3)
navbar.grid_columnconfigure(3, weight=4)
scan_btn = Button(navbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE, command=lambda: scan_texts(text))
prev_pg_btn = Button(navbar, text="Previous", command=lambda: previous_page(text))
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

    global input_text
    input_text = textreader.readtext(selectedfile)
    # input_text = textreader.nopreadtext(selectedfile)
    # CONTINUE: show EACH page in textbox
    text.insert(INSERT, input_text[0])      # INSERT, END defines direction to insert text


def scan_texts(inputtextbox):
    inp = inputtextbox.get(1.0, "end-1c")
    if inp != "":
        parser = parse()
        parser.setUp(inp)
        pp = parser.scantexts()

        print("PP", pp)
        global scan_output
        scan_output = pp
        # create buttons for most repeated word
        for idx, i in enumerate(scan_output[1]):
            # pack(fill='x', side=TOP)
            print(f"text[{idx}]", i[0])
            Button(repeatedword, text=i[0], command=lambda x=i[0]: highlighter.findtext_inthebox(text, x, parser))\
                .grid(row=idx+1, column=0)
    return ()


# Need more? condition check
def previous_page(textbox):
    global input_text
    global current_page_idx

    page_length = len(input_text)

    if current_page_idx in range(1, page_length):       # prev page is available when cur_pg is at idx 1 to last
        input_text[current_page_idx] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, input_text[current_page_idx - 1])
        current_page_idx -= 1
        print("Showed page ", current_page_idx+1, ' / ', page_length)

    return


def next_page(textbox):
    global input_text
    global current_page_idx

    page_length = len(input_text)

    if current_page_idx in range(0, page_length-1):       # next page is available when cur_pg is at idx 0 to last-1
        input_text[current_page_idx] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, input_text[current_page_idx + 1])
        current_page_idx += 1
        print("Showed page ", current_page_idx+1, ' / ', page_length)

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
prev_pg_btn.grid(row=0, column=1, sticky="e", padx=(0, 5))
next_pg_btn.grid(row=0, column=2, sticky="w", padx=(5, 0))
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
repeatedword_header.grid(row=0, column=0, sticky="w")
suggestion.grid(row=1, column=0, sticky="nsew")
suggestion.grid_propagate(False)
suggestion_header.grid(row=0, column=0, sticky="w")

# Launch GUI(last)
root.mainloop()

print("final: ", )