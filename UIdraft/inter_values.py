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


global suggested_words
suggested_words = []

global replacement      # word to replace, start point, end point(where to delete)
# replacement = ["dum", 1.0, 1.2]
replacement = Replace()


def destroy_all_buttons(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, tkinter.Button):
            widget.destroy()
    return


def suggestion_clear(suggestionbox):
    suggested_words.clear()
    replacement.__init__()
    destroy_all_buttons(suggestionbox)
