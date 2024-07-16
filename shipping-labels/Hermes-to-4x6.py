import pymupdf, sys

origfile = "hermes.pdf"

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(40, 72, 469, 362)) # set a cropbox for the page
doc.save("hermes-4x6.pdf")


