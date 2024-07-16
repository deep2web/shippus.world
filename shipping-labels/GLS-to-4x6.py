import pymupdf, sys

origfile = "gls.pdf"

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(21, 101, 277, 250)) # set a cropbox for the page
doc.save("gls-1.pdf")

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(318.7, 55.4, 575.3, 279.29)) # set a cropbox for the page
doc.save("gls-2.pdf")





fname = "gls-1.pdf"  # get filename from command line
doc = pymupdf.open(fname)  # open document
for page in doc:  # iterate through the pages
    pix = page.get_pixmap(dpi=600)
    pix.save("gls-1.png")  # store image as a PNG


fname = "gls-2.pdf"  # get filename from command line
doc = pymupdf.open(fname)  # open document
for page in doc:  # iterate through the pages
    pix = page.get_pixmap(dpi=600)
    pix.save("gls-2.png")  # store image as a PNG




import pymupdf

doc_a = pymupdf.open("gls-1.pdf") # open the 1st document
doc_b = pymupdf.open("gls-2.pdf") # open the 2nd document

doc_a.insert_pdf(doc_b) # merge the docs
doc_a.save("gls-1+2.pdf") # save the merged document with a new filename





doc = pymupdf.open()                 # new empty PDF

page = doc.new_page(-1, # insertion point: end of document
                    width = 287.76978417266184, # page dimension: A4 portrait
                    height = 431.65467625899277)

doc.save("label.pdf") # save the document
"""
import fitz  # PyMuPDF

# Öffnen Sie das Dokument
doc = fitz.open("gls-1+2.pdf")

# Erstellen Sie ein neues leeres Dokument
new_doc = fitz.open()

# Definieren Sie die Positionen der Seiten
positions = [(0, 0), (0, 431.65467625899277)]  # Liste von (x, y) Tupeln

# Durchlaufen Sie das Dokument seitenweise
for i in range(0, len(doc), 2):
    # Erstellen Sie eine neue Seite im neuen Dokument
    page = new_doc.new_page(-1, # insertion point: end of document
                    width = 287.76978417266184, # page dimension: A4 portrait
                    height = 431.65467625899277 * 2)  # Verdoppeln Sie die Höhe, um zwei Seiten untereinander zu platzieren

    # Fügen Sie die aktuelle Seite hinzu
    x, y = positions[0]
    rect = fitz.Rect(x, y, x + 287.76978417266184, y + 431.65467625899277)  # A4-Größe
    page.show_pdf_page(rect, doc, i)

    # Fügen Sie die nächste Seite hinzu, wenn sie existiert
    if i + 1 < len(doc):
        x, y = positions[1]
        rect = fitz.Rect(x, y, x + 287.76978417266184, y + 431.65467625899277)  # A4-Größe und nach unten verschoben
        page.show_pdf_page(rect, doc, i + 1)
"""

import fitz  # PyMuPDF

# Öffnen Sie das Dokument
doc = fitz.open("gls-1+2.pdf")

# Erstellen Sie ein neues leeres Dokument
new_doc = fitz.open()



# Durchlaufen Sie das Dokument seitenweise
for i in range(0, len(doc), 2):
    # Erstellen Sie eine neue Seite im neuen Dokument
    page = new_doc.new_page(-1, width = 287.76978417266184, height = 431.65467625899277)

    # Fügen Sie die aktuelle Seite hinzu
    rect = fitz.Rect(15.88, 10, 271.88, 159)
    page.show_pdf_page(rect, doc, i)

    # Fügen Sie die nächste Seite hinzu
    rect = fitz.Rect(15.58, 177, 272.18, 400.89)
    page.show_pdf_page(rect, doc, i + 1)

# Speichern Sie das neue Dokument
new_doc.save("output.pdf")


"""
src = pymupdf.open("test.pdf")
doc = pymupdf.open()  # empty output PDF

width, height = pymupdf.paper_size("a4")  # A4 portrait output page format
r = pymupdf.Rect(0, 0, width, height)

# define the 4 rectangles per page
r1 = r / 2  # top left rect
r2 = r1 + (r1.width, 0, r1.width, 0)  # top right
r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left
r4 = pymupdf.Rect(r1.br, r.br)  # bottom right

# put them in a list
r_tab = [r1, r2, r3, r4]

# now copy input pages to output
for spage in src:
    if spage.number % 4 == 0:  # create new output page
        page = doc.new_page(-1,
                      width = width,
                      height = height)
    # insert input page into the correct rectangle
    page.show_pdf_page(r_tab[spage.number % 4],  # select output rect
                     src,  # input document
                     spage.number)  # input page number

# by all means, save new file using garbage collection and compression
doc.save("4up.pdf", garbage=3, deflate=True)
"""



doc = pymupdf.open("label.pdf") # open main document
embedded_doc = pymupdf.open("gls-1.pdf") # open document you want to embed

embedded_data = embedded_doc.tobytes() # get the document byte data as a buffer

# embed with the file name and the data
doc.embfile_add("my-embedded_file.pdf", embedded_data)

doc.save("document-with-embed.pdf") # save the document




