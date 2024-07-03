import barcode
from barcode.writer import ImageWriter

# ITF-14 Barcode Klasse laden
ITF = barcode.get_barcode_class('itf')

# Daten für den Barcode (muss eine 14-stellige Zahl sein)
data = '1'

def is_valid_itf(string):
    # Überprüfen, ob der String nur aus Ziffern besteht und eine gerade Anzahl hat
    if not string.isdigit() or len(string) % 2 != 0:
        return False
    
    # Prüfziffer berechnen
    total = 0
    for i, digit in enumerate(string[:-1]):
        if i % 2 == 0:
            total += int(digit) * 3
        else:
            total += int(digit)
    
    check_digit = (10 - (total % 10)) % 10
    
    # Vergleichen der berechneten Prüfziffer mit der letzten Ziffer des Strings
    return check_digit == int(string[-1])

# Beispiele
print(is_valid_itf("1234567890"))  # True
print(is_valid_itf("12345678901"))  # False (ungerade Anzahl)
print(is_valid_itf("1234567891"))  # False (falsche Prüfziffer)
print(is_valid_itf("12345a7890"))  # False (enthält nicht-numerische Zeichen)
print(is_valid_itf(data))

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