import barcode
from barcode.writer import ImageWriter

# ITF-14 Barcode Klasse laden
ITF = barcode.get_barcode_class('itf')

# Daten für den Barcode (muss eine 14-stellige Zahl sein)
data = '1'

# Barcode Objekt erstellen mit Anpassungen
itf_barcode = ITF(data, writer=ImageWriter(), narrow=2, wide=5)

# Barcode als PNG Datei speichern
filename = itf_barcode.save('custom_itf14_barcode')

print(f"Angepasster Barcode gespeichert als {filename}")

from fpdf import FPDF

carton_id = "1003092703"
carriage_class = "priority"

pdf = FPDF("P", "mm", (40, 80))
pdf.add_page()
pdf.set_margins(0, 0, 0)
pdf.add_page()
pdf.output('sample.pdf', 'F')