# Not supported when the word is separated into two lines(but it's nearly impossible to have)

def text_split(input_word, start):
    words = input_word.split()
    start = start.split(".")
    return words



string = "people"
print(text_split(string, "1.250"))

