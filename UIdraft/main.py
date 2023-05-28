import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *

import textreader
import highlighter
import inter_values
from inter_values import replacement
from Pparse import parse
import threading

# GLOBAL VARIABLE(be careful if it goes to other files)
INPUT_TEXT = []
SCAN_OUTPUT = tuple()
CURRENT_PAGE_IDX = 0
PARSER = parse()

# Generate window
root = Tk()
root.title("UniAid - Unique word suggestor")
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
scan_btn = Button(navbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE, command=lambda: threading.Thread(target = scan_texts, args=(text,)).start())
prev_pg_btn = Button(navbar, text="Previous", command=lambda: previous_page(text))
page_label = Label(navbar, text=f"Page 1/1")
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
text.tag_configure('highlight', background='#a2ffee')
text.tag_configure('highlight-clicked', background='#ffa2a2')
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
# suggestion_wordlist.grid_columnconfigure(1, weight=1)
suggestion_function = Frame(sidebar, bg="white")
suggestion_function.grid_columnconfigure(0, weight=1)
suggestion_function.grid_columnconfigure(1, weight=1)
replace_btn = Button(suggestion_function, text="Replace", command=lambda: threading.Thread(target=replace_word,
                                                                                           args=(text,)).start())
ignore_all_btn = Button(suggestion_function, text="Ignore all", command=lambda: ignore_all(inter_values.original_word))


# Functions
def select_file():
    selectedfile = askopenfilename()
    if not selectedfile:
        return

    global INPUT_TEXT

    if selectedfile.endswith(".pdf"):
        clear_inputs()
        INPUT_TEXT = textreader.textract_readtext(selectedfile)
        # for idx, page in enumerate(INPUT_TEXT):
        #     # page = re.sub(r"\r\n", " ", page)
        #     print("PAGE ", idx + 1)
        #     print(page)
        # INPUT_TEXT = textreader.nopreadtext(selectedfile)
        text.insert(INSERT, INPUT_TEXT[0])  # INSERT, END defines direction to insert text
        update_page_label()
        # CONTINUE: .txt file
    elif selectedfile.endswith(".txt"):
        clear_inputs()
        tf = open(selectedfile, 'r')
        INPUT_TEXT.append(tf.read())
        print(INPUT_TEXT)
        text.insert(INSERT, INPUT_TEXT[0].replace('\n', '').replace('\r', ''))
        update_page_label()
    else:
        messagebox.showerror("Open file", "Not supported file format.")
        return


def scan_texts(inputtextbox):
    print("----------------------------------SCAN TEXTS----------------------------------")
    inp = inputtextbox.get(1.0, "end-1c")
    inp = inp.replace("\n", " ")
    inputtextbox.delete('1.0', 'end')
    inputtextbox.insert(INSERT, inp)

    if inp != "":
        inputtextbox.tag_remove("highlight", 1.0, "end-1c")
        inputtextbox.tag_remove("highlight-clicked", 1.0, "end-1c")
        inter_values.destroy_all_buttons(repeatedword)
        global PARSER
        # PARSER = parse()
        PARSER.setUp(inp)

        # print("--->XX<----", PARSER.newline)
        # for i in PARSER.doc.sents:
        # print("----S-->", i)

        pp = PARSER.scantexts()

        print("PP", pp)
        for p in pp:
            if p:
                print("list is not empty")
                break
            else:
                if p == pp[-1]:
                    print("list is empty")
                    messagebox.showinfo("Detector module", "There's no overused word in this page.")
                    return 0
                else:
                    pass
        global SCAN_OUTPUT
        SCAN_OUTPUT = pp
        # create buttons for most repeated word
        for idx, i in enumerate(SCAN_OUTPUT[1]):
            # pack(fill='x', side=TOP)
            print(f"text[{idx}]", i[0])
            Button(repeatedword, text=f"{i[0]}  :  {i[1]} found", relief=FLAT, padx=3, bg="#e7d5fa",
                command=lambda x=i[0]: highlighter.findtext_inthebox(text, suggestion_wordlist, x, PARSER)) \
                .grid(row=idx + 1, column=0, pady=2)
        return 1
    else:
        messagebox.showinfo("Detector module", "There's no text in the page.")
        return 0


def page_init():
    global INPUT_TEXT
    print("PAGE INIT")
    if len(INPUT_TEXT) == 0:
        INPUT_TEXT.insert(0, [])
    update_page_label()


def update_page_label():
    global page_label
    global INPUT_TEXT
    page_length = len(INPUT_TEXT)
    page_label = Label(navbar, text=f"Page {CURRENT_PAGE_IDX + 1}/{page_length}")
    page_label.grid(row=0, column=2, sticky="nsew")


def previous_page(textbox):
    global INPUT_TEXT
    global CURRENT_PAGE_IDX

    page_length = len(INPUT_TEXT)

    if CURRENT_PAGE_IDX in range(1, page_length):  # prev page is available when cur_pg is at idx 1 to last
        inter_values.suggested_words.clear()
        inter_values.destroy_all_buttons(repeatedword)
        inter_values.suggestion_clear(suggestion_wordlist)
        INPUT_TEXT[CURRENT_PAGE_IDX] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, INPUT_TEXT[CURRENT_PAGE_IDX - 1])
        CURRENT_PAGE_IDX -= 1
        # print("Showed page ", CURRENT_PAGE_IDX + 1, ' / ', page_length)
        update_page_label()

    return


def next_page(textbox):
    global INPUT_TEXT
    global CURRENT_PAGE_IDX

    page_length = len(INPUT_TEXT)

    if CURRENT_PAGE_IDX in range(0, page_length - 1):  # next page is available when cur_pg is at idx 0 to last-1
        inter_values.suggested_words.clear()
        inter_values.destroy_all_buttons(repeatedword)
        inter_values.suggestion_clear(suggestion_wordlist)

        INPUT_TEXT[CURRENT_PAGE_IDX] = textbox.get('1.0', 'end-1c')
        textbox.delete('1.0', 'end')
        textbox.insert(INSERT, INPUT_TEXT[CURRENT_PAGE_IDX + 1])
        CURRENT_PAGE_IDX += 1
        # print("Showed page ", CURRENT_PAGE_IDX + 1, ' / ', page_length)
        update_page_label()

    return


def insert_page_after():
    global CURRENT_PAGE_IDX
    global INPUT_TEXT

    INPUT_TEXT.insert(CURRENT_PAGE_IDX+1, [])
    update_page_label()
    next_page(text)


def insert_page_before():
    global CURRENT_PAGE_IDX
    global INPUT_TEXT

    inter_values.suggested_words.clear()
    inter_values.destroy_all_buttons(repeatedword)
    inter_values.suggestion_clear(suggestion_wordlist)

    INPUT_TEXT[CURRENT_PAGE_IDX] = text.get('1.0', 'end-1c')
    INPUT_TEXT.insert(CURRENT_PAGE_IDX, [])
    text.delete('1.0', 'end')
    INPUT_TEXT[CURRENT_PAGE_IDX].clear()
    update_page_label()


def delete_page():
    global CURRENT_PAGE_IDX
    global INPUT_TEXT

    inter_values.suggested_words.clear()
    inter_values.destroy_all_buttons(repeatedword)
    inter_values.suggestion_clear(suggestion_wordlist)

    if CURRENT_PAGE_IDX > 0:
        previous_page(text)
        # print(CURRENT_PAGE_IDX+1)
        del INPUT_TEXT[CURRENT_PAGE_IDX+1]
        update_page_label()
    else:
        # print(CURRENT_PAGE_IDX)
        if len(INPUT_TEXT) > 1:
            next_page(text)
            del INPUT_TEXT[CURRENT_PAGE_IDX-1]
            CURRENT_PAGE_IDX -= 1
            update_page_label()
            # print(INPUT_TEXT)
        else:
            del INPUT_TEXT[CURRENT_PAGE_IDX]
            text.delete('1.0', 'end')
            # print(INPUT_TEXT)



def replace_word(textbox):
    print("----------------------------------REPLACE----------------------------------")
    if replacement.is_not_empty():
        textbox.delete(f"{replacement.start}", f"{replacement.end}")
        textbox.insert(f"{replacement.start}", replacement.word)
        print("Replacement completed")

        # inp = textbox.get(1.0, "end-1c")
        # PARSER.setUp(inp)
        scan = scan_texts(text)
        if scan:
            for i in SCAN_OUTPUT[1]:
                if inter_values.original_word == i[0]:
                    highlighter.findtext_inthebox(text, suggestion_wordlist, inter_values.original_word, PARSER)
                    break

        # Clear Suggestion list
        inter_values.suggestion_clear(suggestion_wordlist)
    else:
        messagebox.showwarning("Replacing word", "You haven't select any words yet")
        return


def clear_inputs():
    global INPUT_TEXT
    global SCAN_OUTPUT
    global CURRENT_PAGE_IDX
    global PARSER
    global page_label

    text.delete('1.0', 'end')
    inter_values.destroy_all_buttons(repeatedword)
    inter_values.suggestion_clear(suggestion_wordlist)
    replacement.__init__()
    INPUT_TEXT.clear()
    SCAN_OUTPUT = tuple()
    CURRENT_PAGE_IDX = 0
    PARSER = parse()
    page_label = Label(navbar, text="Page 1/1")
    page_label.grid(row=0, column=2, sticky="nsew")


def ignore_all(word):   # Insert a word here
    if word == "":
        messagebox.showwarning("Exception list", "You haven't select any words yet")
        return
    else:
        info_text = "'" + word + "'"
        answer = messagebox.askyesno("Confirm", f"Add the word {info_text} to the exception list?")
        if answer:
            if word in inter_values.exception_list:
                messagebox.showwarning("Exception list", "The word is already in the exception list.")
                pass
            else:
                splitted_word = word.split()
                inter_values.exception_list.append(splitted_word)
                print(inter_values.exception_list)
                messagebox.showinfo("Exception list", f"Added the word {info_text} to the exception list")
                inter_values.destroy_all_buttons(repeatedword)
                inter_values.suggestion_clear(suggestion_wordlist)
                replacement.__init__()
                threading.Thread(target = scan_texts, args=(text,)).start()
                inter_values.original_word = str()
    return
    # Create a Label
    # Label(root, text=answer, font=('Georgia 20 bold')).pack()


# Place default labels
# # Menubar
menubar.add_cascade(label="File", menu=menubar_file)
menubar_file.add_command(label="New", command=clear_inputs)
menubar_file.add_command(label="Open", command=select_file)
# menubar_file.add_command(label="Save")
# menubar_file.add_command(label="Save as")
# menubar_file.add_command(label="Settings")

menubar.add_cascade(label="Edit", menu=menubar_edit)
menubar_edit.add_command(label="Insert page before", command=lambda: insert_page_before())
menubar_edit.add_command(label="Insert page after", command=lambda: insert_page_after())
menubar_edit.add_command(label="Delete page", command=lambda: delete_page())

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
text.place(relwidth=0.5, relx=0.5, rely=0.5, anchor=CENTER)
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
suggestion_function.grid(row=2, column=0, sticky="sew")
replace_btn.grid(row=0, column=0, sticky="we", padx=10, pady=10)
ignore_all_btn.grid(row=0, column=1, sticky="we", padx=10, pady=10)  # PUT command=function_name HERE

# Configure scrollbar
text_scroll.config(command=text.yview)

page_init()

# Launch GUI(last)
root.mainloop()

# BABUU
print("final: ", )
