import barcode #for barcode generation
from barcode.writer import SVGWriter #for barcode generation
from fpdf import FPDF #for PDF generation
import tempfile #for temporary saving the barcode



# General Values:
carton_id = "1003092703"
carriage_class_code = "P"

# Erstellen Sie einen Code 128 Barcode
code128 = barcode.get('code128', carton_id, writer=SVGWriter())


# Optionen für den Barcode definieren
options = {
    'module_width': 0.4,  # Breite eines Moduls in mm
    'module_height': 25,  # Höhe des Barcodes in mm
    'quiet_zone': 2.5,    # Ruhezone um den Barcode in mm
    'font_size': 0,      # Schriftgröße in Punkten
    'text_distance': 0,   # Abstand zwischen Barcode und Text in mm
    'background': 'white',  # Hintergrundfarbe
    'foreground': 'black',     # Vordergrundfarbe (Balkenfarbe)
    'write_text': False,   # Text unter dem Barcode anzeigen
    #'text': 'Custom Text' # Benutzerdefinierter Text (optional)
}

# Barcode mit benutzerdefinierten Optionen speichern
filename = code128.save('custom_barcode', options=options)


# Speichern Sie den Barcode als PNG-Datei
filename = code128.save('code128_barcode')

with tempfile.NamedTemporaryFile(delete=False, suffix=".svg") as temp:
    code128.write(temp, options=options)
    temp_barcode = temp.name



# generate PDF



pdf = FPDF("L", "mm", (57, 80))
pdf.set_margins(0, 0, 0)
pdf.set_font("Arial", size = 50) # set font and size

pdf.add_page()
pdf.interleaved2of5("1337", x=10, y=35, w=4, h=20) # add barcode
pdf.text(60, 20, "P")# add carriage class code

pdf.output('sample.pdf', 'F')