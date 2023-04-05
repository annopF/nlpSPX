import tkinter as tk


# https://stackoverflow.com/questions/40940397/tkinter-text-widget-use-clicked-text-in-event-function
def callback(event):
    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('tag'))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            # return string between tag start and end
            print(start, end, event.widget.get(start, end))

root = tk.Tk()

text = tk.Text(root)
text.pack()

text.tag_config("tag", foreground="blue")
text.tag_bind("tag", "<Button-1>", callback)

text.insert('end', "first link", "tag")

text.insert('end', " other text ")

text.insert('end', "second link", "tag")

root.mainloop()