from tkinter import *

root = Tk()


def method2():
    x = "Done it !"
    m.set(x)


m = StringVar()
b1 = Button(root, text="Click", command=method2).pack()
lb1 = Label(root, text="...", textvariable=m).pack()

root.mainloop()