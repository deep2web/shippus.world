import pymupdf, sys
import os
import glob

# Liste aller PDF-Dateien im Unterordner /batch
pdf_files = glob.glob("./batch/*.pdf")

for origfile in pdf_files:
    doc = pymupdf.open(origfile) # open document
    page = doc[0] # get the 1st page of the document
    page.set_cropbox(pymupdf.Rect(21, 101, 277, 250)) # set a cropbox for the page
    doc.save(origfile.replace(".pdf", "-1.pdf"))

    doc = pymupdf.open(origfile) # open document
    page = doc[0] # get the 1st page of the document
    page.set_cropbox(pymupdf.Rect(318.7, 55.4, 575.3, 279.29)) # set a cropbox for the page
    doc.save(origfile.replace(".pdf", "-2.pdf"))

    doc_a = pymupdf.open(origfile.replace(".pdf", "-1.pdf")) # open the 1st document
    doc_b = pymupdf.open(origfile.replace(".pdf", "-2.pdf")) # open the 2nd document

    doc_a.insert_pdf(doc_b) # merge the docs
    doc_a.save(origfile.replace(".pdf", "-1+2.pdf")) # save the merged document with a new filename

    # Öffnen Sie das Dokument
    doc = pymupdf.open(origfile.replace(".pdf", "-1+2.pdf"))

    # Erstellen Sie ein neues leeres Dokument
    new_doc = pymupdf.open()

    # Durchlaufen Sie das Dokument seitenweise
    for i in range(0, len(doc), 2):
        # Erstellen Sie eine neue Seite im neuen Dokument
        page = new_doc.new_page(-1, width = 287.76978417266184, height = 431.65467625899277)

        # Fügen Sie die aktuelle Seite hinzu
        rect = pymupdf.Rect(15.88, 10, 271.88, 159)
        page.show_pdf_page(rect, doc, i)

        # Fügen Sie die nächste Seite hinzu
        rect = pymupdf.Rect(15.58, 159, 272.18, 382.89)
        page.show_pdf_page(rect, doc, i + 1)

    # Speichern Sie das neue Dokument
    new_doc.save(origfile.replace(".pdf", "-4x6.pdf"))
    os.remove(origfile)

    os.remove(origfile.replace(".pdf", "-1.pdf")) #cleanup
    os.remove(origfile.replace(".pdf", "-2.pdf")) #cleanup
    os.remove(origfile.replace(".pdf", "-1+2.pdf")) #cleanup