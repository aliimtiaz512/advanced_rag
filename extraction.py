import PyPDF2
def extract_from_pdf():
    raw_text=""
    with open("great_gatsby.pdf", "rb") as f:
        reader=PyPDF2.PdfReader(f)
        for page in reader.pages:
            raw_text+=page.extract_text()
    return raw_text
