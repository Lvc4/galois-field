# GaloisFieldElement für GF(2^m)

Dieses Modul implementiert Elemente des Galois-Feldes \( GF(2^m) \), inklusive grundlegender Feldoperationen und Konvertierungen.

## Funktionen

### Erstellung
- **`__init__(value: int, irreducible_poly: int)`**: Initialisiert ein Element.
- **`from_hex(hex_value: str, irreducible_poly: int)`**: Erstellt aus Hex-Wert.
- **`from_bitvector(bitvector: List[int], irreducible_poly: int)`**: Erstellt aus Bitvektor.

### Operationen
- **Addition/Subtraktion (`+`, `-`)**: XOR der Werte.
- **Multiplikation (`*`)**: Mit Modularreduktion.
- **Vergleich (`==`)**: Prüft Gleichheit.

### Konvertierungen
- **`to_hex()`**: Ausgabe als Hex-Wert.
- **`to_bitvector()`**: Ausgabe als Bitvektor.
- **`to_polynomial()`**: Ausgabe als Polynom.

## Installation

Um das Paket zu installieren, kannst du es direkt von GitHub installieren:

```bash
pip install git+https://github.com/Lvc4/galois-field.git
```

## Beispiel

```python
irreducible_poly = 0b10011  # Irreduzibles Polynom für GF(2^4)

a = GaloisFieldElement(0b1010, irreducible_poly)
b = GaloisFieldElement(0b1100, irreducible_poly)

c = a + b  # Addition
d = a * b  # Multiplikation

print(c.to_polynomial())  # x^3 + x
print(d.to_hex())         # '0x9'
