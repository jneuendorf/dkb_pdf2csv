from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


for page_layout in extract_pages("sample.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(element.get_text(), element)
        else:
            print(element)
