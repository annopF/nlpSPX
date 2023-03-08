from PyPDF2 import PdfReader


def readtext(filepath):
    reader = PdfReader(filepath)
    text = str()
    for i in range(len(reader.pages)):
        currentpage = reader.pages[i].extract_text()
        if i == 0:
            text = currentpage
        else:
            text = "\n------------------------------\n".join([text, currentpage])
        # text = f"{text, currentpage}"
    # page = reader.pages[0]
    # text = page.extract_text()
    return text
