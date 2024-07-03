import barcode #for barcode generation
import cups #for printing
from barcode.writer import SVGWriter #for barcode generation
from fpdf import FPDF #for PDF generation
import tempfile #for temporary saving the barcode


def print_file(file_path, printer_name):

    conn = cups. Connection()

    printers = conn.getPrinters()
    
    if printer_name in printers:
        try:
            conn.printFile(printer_name, file_path, "Print Job", {})
            print("File sent to printer successfully.")
        except cups.IPPError as e:
            print(f"Error printing file: {e}")
    else:
        print(f"Printer '{printer_name}' not found.")



# General Values:
carton_id = "1003092703"
order_number = "1046"
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
pdf = FPDF("L", "mm", (57, 170))
pdf.set_margins(0, 0, 0)


pdf.add_page()

pdf.interleaved2of5(carton_id, x=5, y=25, w=2, h=30) # add barcode

pdf.set_font("Arial", size = 50) # set font and size for carriage class code
pdf.text(60, 20, carriage_class_code) # add carriage class code


pdf.set_font("Arial", size = 9) # set font and size for order_number and carton_id
pdf.text(5, 16, "Carton ID:") # add order number
pdf.text(5, 6, "Order No.:") # add order number

pdf.set_font("Arial", size = 17) # set font and size for order_number and carton_id
pdf.text(5, 21, carton_id) # add order number
pdf.text(5, 11, order_number) # add order number






pdf.interleaved2of5(carton_id, x=100, y=25, w=2, h=30) # add barcode

pdf.set_font("Arial", size = 50) # set font and size for carriage class code
pdf.text(155, 20, carriage_class_code) # add carriage class code


pdf.set_font("Arial", size = 9) # set font and size for order_number and carton_id
pdf.text(100, 16, "Carton ID:") # add order number
pdf.text(100, 6, "Order No.:") # add order number

pdf.set_font("Arial", size = 17) # set font and size for order_number and carton_id
pdf.text(100, 21, carton_id) # add order number
pdf.text(100, 11, order_number) # add order number

pdf.output('sample.pdf', 'F')


file_to_print = "sample.pdf"
printer_name = "alere_prima"
print_file(file_to_print, printer_name)