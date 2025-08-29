# GaloisFieldElement für GF(2^m)

Dieses Modul implementiert Elemente des Galois-Feldes \( GF(2^m) \), inklusive grundlegender Feldoperationen, erweiterten algebraischen Funktionen und praktischen Hilfsmitteln.

## Funktionen

### Erstellung
- **`__init__(value: int, irreducible_poly: int)`**: Initialisiert ein Element mit Eingabevalidierung.
- **`from_hex(hex_value: str, irreducible_poly: int)`**: Erstellt aus Hex-Wert.
- **`from_bitvector(bitvector: List[int], irreducible_poly: int)`**: Erstellt aus Bitvektor.
- **`from_standard_field(value: int, m: int)`**: Erstellt Element aus Standardfeld mit vordefiniertem irreduziblem Polynom.

### Grundlegende Operationen
- **Addition/Subtraktion (`+`, `-`)**: XOR der Werte.
- **Multiplikation (`*`)**: Mit Modularreduktion.
- **Division (`/`)**: a / b = a * b^(-1).
- **Potenzierung (`**`)**: Effiziente Exponentiation mit negativer Exponenten-Unterstützung.
- **Vergleich (`==`)**: Prüft Gleichheit.
- **Hash (`hash()`)**: Ermöglicht Verwendung in Sets und Dictionaries.

### Erweiterte Feldoperationen
- **`inverse()`**: Berechnet multiplikatives Inverses mit erweiterten euklidischen Algorithmus.
- **`order()`**: Berechnet multiplikative Ordnung des Elements.
- **`is_primitive()`**: Prüft, ob Element primitiv ist (Ordnung = 2^m - 1).
- **`frobenius(power=1)`**: Wendet Frobenius-Automorphismus an (x -> x^(2^power)).

### Konvertierungen
- **`to_hex()`**: Ausgabe als Hex-Wert.
- **`to_bitvector()`**: Ausgabe als Bitvektor.
- **`to_polynomial()`**: Ausgabe als Polynom-String.

### Feldkonstanten und Hilfsmittel
- **`zero(irreducible_poly)`**: Erstellt Nullelement (Klassenmethode).
- **`one(irreducible_poly)`**: Erstellt Einselement (Klassenmethode).
- **`zero_element()` / `one_element()`**: Gibt Null-/Einselement des aktuellen Feldes zurück.
- **`field_size()`**: Gibt Feldgröße (2^m) zurück.
- **`all_elements(irreducible_poly)`**: Generiert alle Feldelemente (Klassenmethode).
- **`random_element(irreducible_poly)`**: Generiert zufälliges Feldelement (Klassenmethode).

### Vordefinierte irreduzible Polynome
Die Konstante `IRREDUCIBLE_POLYNOMIALS` enthält Standard-Polynome für Grade 2-8:
- **GF(2^2)**: x^2 + x + 1
- **GF(2^3)**: x^3 + x + 1  
- **GF(2^4)**: x^4 + x + 1
- **GF(2^5)**: x^5 + x^2 + 1
- **GF(2^6)**: x^6 + x + 1
- **GF(2^7)**: x^7 + x + 1
- **GF(2^8)**: x^8 + x^4 + x^3 + x + 1

## Installation

Um das Paket zu installieren, kannst du es direkt von GitHub installieren:

```bash
pip install git+https://github.com/Lvc4/galois-field.git
```

## Beispiele

### Grundlegende Operationen
```python
from galois_field import GaloisFieldElement, IRREDUCIBLE_POLYNOMIALS

# Verwende vordefiniertes Polynom für GF(2^4)
irreducible_poly = IRREDUCIBLE_POLYNOMIALS[4]  # x^4 + x + 1

a = GaloisFieldElement(0b1010, irreducible_poly)  # x^3 + x
b = GaloisFieldElement(0b1100, irreducible_poly)  # x^3 + x^2

c = a + b  # Addition (XOR)
d = a * b  # Multiplikation
e = a / b  # Division
f = a ** 3  # Potenzierung

print(f"Addition: {c.to_polynomial()}")     # x^2 + x
print(f"Multiplikation: {d.to_polynomial()}")  # x^2
print(f"Division: {e.to_polynomial()}")     # x^3 + x^2 + x + 1
print(f"Potenz: {f.to_polynomial()}")       # x^3 + x^2 + 1
```

### Erweiterte Funktionen
```python
# Standardfeld-Erstellung
elem = GaloisFieldElement.from_standard_field(5, 4)  # GF(2^4)
print(f"Element: {elem.to_polynomial()}")  # x^2 + 1

# Feldeigenschaften
print(f"Feldgröße: {elem.field_size()}")      # 16
print(f"Ordnung: {elem.order()}")             # 15 
print(f"Primitiv? {elem.is_primitive()}")     # True

# Inverses und Division
inv = elem.inverse()
print(f"Inverses: {inv.to_polynomial()}")     # x^3 + x + 1
print(f"Verifikation: {(elem * inv).value}")  # 1

# Frobenius-Automorphismus  
frob = elem.frobenius()
print(f"x -> x^2: {frob.to_polynomial()}")    # x

# Alle Feldelemente generieren
all_elems = GaloisFieldElement.all_elements(IRREDUCIBLE_POLYNOMIALS[3])
print(f"GF(2^3) hat {len(all_elems)} Elemente:")
for e in all_elems:
    print(f"  {e.value}: {e.to_polynomial()}")
```

### Sets und Dictionaries
```python
# Elemente können in Sets/Dicts verwendet werden
field_set = {
    GaloisFieldElement(1, IRREDUCIBLE_POLYNOMIALS[4]),
    GaloisFieldElement(2, IRREDUCIBLE_POLYNOMIALS[4]),
    GaloisFieldElement(1, IRREDUCIBLE_POLYNOMIALS[4])  # Duplikat
}
print(f"Set-Größe: {len(field_set)}")  # 2 (keine Duplikate)

# Als Dictionary-Keys
field_properties = {
    GaloisFieldElement(2, IRREDUCIBLE_POLYNOMIALS[4]): "primitives Element",
    GaloisFieldElement(1, IRREDUCIBLE_POLYNOMIALS[4]): "Einselement"
}
```

## Neue Features in Version 0.2.0

- **Division und multiplicatives Inverses**: Vollständige Division mit `/`-Operator
- **Potenzierung**: Effiziente Exponentiation inklusive negative Exponenten  
- **Hash-Unterstützung**: Verwendung in Sets und als Dictionary-Keys
- **Feldtheorie-Funktionen**: Ordnung, primitive Elemente, Frobenius-Mapping
- **Verbesserte Eingabevalidierung**: Robuste Fehlerbehandlung
- **Vordefinierte Polynome**: Standard-Polynome für häufige Feldgrößen
- **Hilfsfunktionen**: Zufällige Elemente, alle Elemente, Feldkonstanten
- **Erweiterte Tests**: Umfassende Testsuite für alle neuen Features

## Lizenz

MIT