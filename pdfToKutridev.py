# import fitz  # PyMuPDF

# pdf_path = "HindiElective.pdf"
# txt_path = "output.txt"

# doc = fitz.open(pdf_path)

# with open(txt_path, "w", encoding="utf-8") as f:
#     for page in doc:
#         text = page.get_text()
#         f.write(text + "\n")

# print("✅ Text extracted successfully!")

import pdfplumber

with pdfplumber.open("mypdf.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

with open("raw.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Raw text extracted")