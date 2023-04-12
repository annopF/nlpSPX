from PyPDF2 import PdfReader
import re


def readtext(filepath):
    reader = PdfReader(filepath)
    text = str()
    for i in range(len(reader.pages)):
        currentpage = reader.pages[i].extract_text()
        currentpage = re.sub(r"\n", " ", currentpage) 
        if i == 0:
            text = currentpage + "\n------------------------------\n"
        else:
            text = "".join([text, currentpage])
        # text = f"{text, currentpage}"
    # page = reader.pages[0]
    # text = page.extract_text()
    return text
