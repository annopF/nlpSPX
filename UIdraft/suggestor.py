from Pparse import parse

def callback(event,bg, dox):
    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "adj" tags
    tag_indices = list(event.widget.tag_ranges('highlight'))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        # check if the tag matches the mouse click index
        if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
            # return string between tag start and end
            word = event.widget.get(start,end).split(" ")
            gram1 = word[0]
            gram2 = word[1]
            print("PACK GRAM ",gram1, gram2)

            ###### CALL SUGGESTION FUNCTION ######
            def tclToInt(tcl):
                return int(str(tcl)[slice(2,len(str(tcl)))])
            
        
            print("type of start: ", type(start))

            for item in bg:
                a = item.getParentSentence(tclToInt(start),gram1, gram2)
                if a:
                    print(list(dox.sents)[a.getSentId()])
