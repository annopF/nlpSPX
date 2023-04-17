import tkinter as tk
import datetime

def set_label():
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label['text'] = currentTime
    root.after(1000, set_label)

root = tk.Tk()
label = tk.Label(root, text="placeholder")
label.pack()

set_label()
root.mainloop()
