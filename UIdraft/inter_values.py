import tkinter

global suggested_words
suggested_words = []

global replacement      # word to replace, start point, end point(where to delete)
# replacement = ["dum", 1.0, 1.2]
replacement = []


def destroy_all_buttons(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tkinter.Button):
            widget.destroy()
    return


def suggestion_clear(suggestionbox):
    suggested_words.clear()
    replacement.clear()
    destroy_all_buttons(suggestionbox)
