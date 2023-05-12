import tkinter


class Replace():
    def __init__(self):
        self.word = None
        self.start = None
        self.end = None

    def add_replace(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end
        return

    def is_not_empty(self):
        if self.word is None or self.start is None or self.end is None:
            return False
        else:
            return True


global original_word
original_word = str()

global suggested_words
suggested_words = []

global replacement      # word to replace, start point, end point(where to delete)
# replacement = ["dum", 1.0, 1.2]
replacement = Replace()

global exception_list
exception_list = []


def destroy_all_buttons(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tkinter.Button):
            widget.destroy()
    return


def suggestion_clear(suggestionbox):
    suggested_words.clear()
    replacement.__init__()
    for widget in suggestionbox.winfo_children():
        widget.destroy()
    return
