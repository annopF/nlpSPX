from PyPDF2 import PdfReader
import re
import textract as tt


#Pypdf
def readtext(filepath):
    reader = PdfReader(filepath)
    pages = []
    for i in range(len(reader.pages)):
        currentpage = reader.pages[i].extract_text()
        currentpage = re.sub(r"\n", " ", currentpage)
        pages.append(currentpage)

    for idx, page in enumerate(pages):
        print("PAGE ", idx+1)
        print(page)

    return pages


# textract method(ERR: returns )
def nopreadtext(filepath):
    text = tt.process(filepath)
    print("Text: ", text)
    texts = text.decode("utf8")
    print("Texts: ", texts)
    pattern = '\n'
    result = re.sub(pattern, " ", texts)
    print("Result", result)
    return result

# https://stackoverflow.com/questions/67724826/analyzing-a-specific-page-of-a-pdf-with-amazon-textract
