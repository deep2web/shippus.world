import pymupdf, sys
import os
import glob

# Liste aller PDF-Dateien im Unterordner /batch
pdf_files = glob.glob("./batch/*.pdf")

for origfile in pdf_files:
    doc = pymupdf.open(origfile) # open document
    page = doc[0] # get the 1st page of the document
    page.set_cropbox(pymupdf.Rect(5, 0, 289, 420.154)) # set a cropbox for the page
    doc.save(origfile.replace(".pdf", "-4x6.pdf")) # save the document with a new filename

    # Löschen Sie die ursprüngliche Datei nach der Verarbeitung
    os.remove(origfile)