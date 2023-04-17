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
    texts = text.decode("utf8")
    pattern = '\n'
    result = re.sub(pattern, " ", texts)
    print(result)
    return result
