from tkinter import *
from tkinter.filedialog import *

import textreader

root = Tk()
root.title("Draft GUI")
root.geometry("1280x720")
root.resizable(width=False, height=False)


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


# ##Menu(toolbar)## #
myMenu = Menu()
fileItem = Menu()
editItem = Menu()
root.config(menu=myMenu)

myMenu.add_cascade(label="File", menu=fileItem)
fileItem.add_command(label="New")
fileItem.add_command(label="Open", command=select_file)
fileItem.add_command(label="Save")
fileItem.add_command(label="Save as")
fileItem.add_command(label="Settings")

myMenu.add_cascade(label="Edit")
editItem.add_command(label="Undo")
editItem.add_command(label="Redo")

# ##Toolbar## #
toolbar = Frame(root, height=60, padx=10, pady=10, bg="white", highlightbackground="#d8d8d8", highlightthickness="2")
toolbar.pack(fill="x")
btn1 = Button(toolbar, text="Scan", bg="#b5ffc1", padx=15, relief=RIDGE)
btn1.pack(anchor="w")

# ##Workspace## #
mainframe = Frame(root, bg="#ebeff8")
mainframe.pack(expand=1, fill=BOTH)

# Sidebar
sidebar = Frame(mainframe, width=250, bg="white", highlightbackground="#d8d8d8", highlightthickness="2")
sidebar.pack(fill="y", expand=True, anchor="e")
sidebarHeader = Label(sidebar, bg="white", text="Most repeated word", padx=50, pady=10, font="24")
sidebarHeader.pack()

# Paper(width 500)
textarea = Frame(mainframe, width=500, bg="red")
textarea.place(x=265, relheight=1)
text = Text(textarea, font=("Ink Free", 16), padx=10, pady=10, relief=FLAT)
text.place(relwidth=1, relheight=1)

root.mainloop()
