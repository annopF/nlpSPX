from tkinter import *
import tkinter

root = Tk()
root.title("Draft GUI")
root.geometry("200x400")
root.resizable(width=False, height=False)
frame = Frame(root)
# frame.bindtags((str(frame), str(root), "all"))

frame.pack(expand=True, fill='both', side="left")
frame.pack_propagate(False)
# print(get_screensize)

frame.update()

button_row = {}
# for x in range(1, 10):
#     button_row["row{0}".format(x)] = "Hello"
print(button_row)
print(type(button_row))


# btn.pack()
# btn.update()
# print(btn.winfo_width())

texts = ["one", "two", "three","four", "five", "six","seven", "eight", "nine","ten", "eleven", "twelve", "capybara"]

def print_text(text):
    print(text)


def clear_last(obj):
    last = obj.winfo_children()[-1]
    last.destroy()


# For inter_values
def destroy_subrow_btn(fr):
    for row in fr:
        for widget in row.winfo_children():
            if isinstance(widget, tkinter.Button):
                widget.destroy()
    return


def wrap_btn_place(parent, text_list):
    width = parent.winfo_width()
    current_row = 0
    current_column = 0

    available_width = width

    button_row["row{0}".format(current_row)] = Frame(parent, bg="green")
    button_row["row{0}".format(current_row)].grid(sticky="we")
    for text in text_list:
        text_btn = Button(button_row["row{0}".format(current_row)], text=f"{text}", command=lambda x=text: print_text(x))
        text_btn.grid(row=0, column=current_column)
        text_btn.update()
        using_width = text_btn.winfo_width()
        if available_width < using_width:
            clear_last(button_row["row{0}".format(current_row)])
            available_width = width
            current_row += 1
            button_row["row{0}".format(current_row)] = Frame(parent, bg="blue")
            text_btn = Button(button_row["row{0}".format(current_row)], text=f"{text}",
                              command=lambda x=text: print_text(x))
            button_row["row{0}".format(current_row)].grid(sticky="we")
            current_column = 0
            text_btn.grid(row=0, column=current_column)
            available_width -= using_width
            print("placed button at: ", current_row, current_column)
            print("Available: ", available_width)
            current_column += 1
        else:
            text_btn.grid(row=0, column=current_column)
            available_width -= using_width
            print("placed button at: ", current_row, current_column)
            print("Available: ", available_width)
            current_column += 1

        # print(available_width)

# for n in range(0, 5):
#     Button(frame, text="Capybara").pack()


wrap_btn_place(frame, texts)

root.mainloop()
