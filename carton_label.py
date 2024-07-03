import barcode
from barcode.writer import ImageWriter

# ITF-14 Barcode Klasse laden
ITF = barcode.get_barcode_class('itf')

# Daten für den Barcode (muss eine 14-stellige Zahl sein)
data = '1'


def is_valid_itf(data):
    if not data.isdigit():
        return False  # enthält nicht-numerische Zeichen
    if len(data) % 2 != 0:
        return False  # ungerade Anzahl
    # Prüfziffer berechnen
    odd_sum = sum(int(data[i]) for i in range(len(data)-1, -1, -2))
    even_sum = sum(int(data[i]) for i in range(len(data)-2, -1, -2))
    check_digit = (10 - ((3 * odd_sum + even_sum) % 10)) % 10
    if int(data[-1]) != check_digit:
        return False  # falsche Prüfziffer
    return True




from pyitf.code import  validate_code


def calculate_check_digit(code: int) -> int:
    """Calculates and returns the check digit for the given code."""
    digits = internal.digits(code)

    sum_digits = 0
    for i, n in enumerate(digits):
        sum_digits += n if (i+1) % 2 == 0 else n*3

    mod10 = sum_digits % 10

    return 0 if mod10 < 1 else 10-mod10


def append_check_digit(code: int) -> int:
    """Returns the given code including a calculated check digit."""
    return code*10 + calculate_check_digit(code)




# Beispiele
print(is_valid_itf("1234567890"))  # True
print(is_valid_itf("12345678901"))  # False (ungerade Anzahl)
print(is_valid_itf("1234567891"))  # False (falsche Prüfziffer)
print(is_valid_itf("12345a7890"))  # False (enthält nicht-numerische Zeichen)
print(is_valid_itf(data))
print(is_valid_itf("1003092703"))  # True
print(is_valid_itf("12345678901"))  # False (ungerade Anzahl)
print(is_valid_itf("1234567891"))  # False (falsche Prüfziffer)
print(is_valid_itf("12345a7890"))  # False (enthält nicht-numerische Zeichen)


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