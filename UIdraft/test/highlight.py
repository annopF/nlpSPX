import tkinter as tk
import re


def findtext_inthebox(textbox, target):
    inp = textbox.get(1.0, "end-1c")    # end is end, -1c will delete 1 last char(newline)
    # linecount = int(textbox.index('end-1c').split('.')[0])
    # endindex = int(textbox.index('\n'))
    # print(endindex)
    # inp = []
    # print(type(inp))
    # for i in range(linecount):
    #     startindex = f'{i+1}.0'
    #     inp.append(textbox.get(startindex, 'end-1c'))   # end-nc
    print(inp)
    print(type(inp))

    pattern = re.compile(f"{target}")
    print(pattern)
    for m in pattern.finditer(inp):
        print(m.group(), m.start(), m.end(), type(m.group()), type(m.start()), type(m.end()))
        textbox.tag_add(f'color{m}', f'1.{m.start()}', f'1.{m.end()}')  # line, text index
        textbox.tag_configure(f'color{m}', background='red', font='lucida 20 bold underline')

    return


root = tk.Tk()
root.geometry("500x200")
root.configure(bg='sky blue')
root.resizable(width=False, height=False)

root.grid_columnconfigure(0, weight=1)

root.grid_rowconfigure(0, weight=20)    # row 0 is x times bigger(scale) than row 1
root.grid_rowconfigure(1, weight=1)

text = tk.Text(root, width=1, height=1)
text.grid(row=0, column=0, padx=5, pady=5, sticky="WENS")


string = "My name is Yoshikage Kira. I’m 33 years old. "
string2 = "My house is in the northeast section of Morioh. Where all the villas are. And I am not married."
text.insert("1.0", string)
text.insert("2.0", string2)

btn = tk.Button(root, text="find me", command=lambda: findtext_inthebox(text, "My"))
btn.grid(row=1, column=0)


root.mainloop()
