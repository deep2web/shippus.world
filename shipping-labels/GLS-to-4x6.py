import pymupdf

origfile = "gls.pdf"

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(21, 101, 277, 250)) # set a cropbox for the page
doc.save("gls-1.pdf")

doc = pymupdf.open(origfile) # open document
page = doc[0] # get the 1st page of the document
page.set_cropbox(pymupdf.Rect(318.7, 55.4, 575.3, 279.29)) # set a cropbox for the page
doc.save("gls-2.pdf")
















doc = pymupdf.open()                 # new empty PDF

page = doc.new_page(-1, # insertion point: end of document
                    width = 287.76978417266184, # page dimension: A4 portrait
                    height = 431.65467625899277)

doc.save("label.pdf") # save the document



doc = pymupdf.open("label.pdf") # open main document
embedded_doc = pymupdf.open("gls-1.pdf") # open document you want to embed

embedded_data = embedded_doc.tobytes() # get the document byte data as a buffer

# embed with the file name and the data
doc.embfile_add("my-embedded_file.pdf", embedded_data)

doc.save("document-with-embed.pdf") # save the document




