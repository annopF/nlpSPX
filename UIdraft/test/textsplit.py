# Not supported when the word is separated into two lines(but it's nearly impossible to have)

def text_split(input_word, start):
    # print(start)
    words = input_word.split()
    start = start.split(".")
    # print(start)

    line = start[0]
    start_idx = int(start[1])

    words_idx = []

    for word in words:
        idx = [".".join([line, str(start_idx)])]
        start_idx += len(word) - 1
        idx.append(".".join([line, str(start_idx)]))
        words_idx.append(idx)
        start_idx += 2

    return words_idx


string = "rich people"
print(text_split(string, "1.250"))

