from PyPDF2 import PdfReader
import re
import textract as tt


def readtext(filepath):
    # reader = PdfReader(filepath)
    # text = str()
    # for i in range(len(reader.pages)):
    #     currentpage = reader.pages[i].extract_text()
    #     currentpage = re.sub(r"\n", " ", currentpage)
    #     if i == 0:
    #         text = currentpage + "\n------------------------------\n"
    #     else:
    #         text = "".join([text, currentpage]) + "\n------------------------------\n"
    #     # text = f"{text, currentpage}"
    # # page = reader.pages[0]
    # # text = page.extract_text()
    # return text

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
