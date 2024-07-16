import pymupdf, sys

origfile = "dhl.pdf"

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(15, 70.2, 581, 355)) # set a cropbox for the page
page.set_rotation(90) # rotate the page
doc.save("dhl-4x8.pdf")


