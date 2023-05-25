from PyPDF2 import PdfReader
import re
import textract as tt


#Pypdf
def pypdf_readtext(filepath):
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
def textract_readtext(filepath):
    text = tt.process(filepath)
    print("Text: ", text)
    texts = text.decode("utf8")
    print("Texts: ", texts)
    pages = texts.split("\r\n\r\n")
    pages[-1] = pages[-1].replace("", "")
    print(type(pages))
    for idx, page in enumerate(pages):
        pages[idx] = re.sub(r"\r\n", " ", pages[idx])
        print("PAGE ", idx + 1)
        print(pages[idx])
    # pattern = '\n'
    # result = re.sub(pattern, " ", texts)
    # print("Result", result)
    # return result
    return pages
