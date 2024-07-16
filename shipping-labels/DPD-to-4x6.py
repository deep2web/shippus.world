import pymupdf, sys

origfile = "dpd.pdf"

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(5, 0, 289, 420.154)) # set a cropbox for the page
doc.save("dpd-4x6.pdf")


