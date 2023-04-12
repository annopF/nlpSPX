from PyPDF2 import PdfReader
import re
import textract as tt

def readtexts(filepath):
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
    print(text)
    return text

def readtext(input):
    text = tt.process(input)
    texts = text.decode("utf8")
    texts = re.sub(r"\n"," ", texts)
    return(texts)