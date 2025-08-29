from typing import List

# Häufig verwendete irreduzible Polynome für verschiedene Grade
IRREDUCIBLE_POLYNOMIALS = {
    2: 0b111,       # x^2 + x + 1
    3: 0b1011,      # x^3 + x + 1  
    4: 0b10011,     # x^4 + x + 1
    5: 0b100101,    # x^5 + x^2 + 1
    6: 0b1000011,   # x^6 + x + 1
    7: 0b10000011,  # x^7 + x + 1
    8: 0b100011011, # x^8 + x^4 + x^3 + x + 1
}

class GaloisFieldElement:
    def __init__(self, value: int, irreducible_poly: int) -> None:
        """
        Galois-Feld-Element initialisieren (nur für GF(2^m)).
        :param value: Ganzzahldarstellung des Polynoms (z. B. 0b101 für x^2 + 1).
        :param irreducible_poly: Irreduzibles Polynom des Grades m für GF(2^m).
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("Value muss eine nicht-negative ganze Zahl sein.")
        if not isinstance(irreducible_poly, int) or irreducible_poly <= 1:
            raise ValueError("Irreduzibles Polynom muss eine ganze Zahl > 1 sein.")
        
        self.irreducible_poly: int = irreducible_poly
        self.m = self.irreducible_poly.bit_length() - 1
        self.value: int = self._poly_reduction(value)

    @classmethod
    def from_hex(cls, hex_value: str, irreducible_poly: int) -> 'GaloisFieldElement':
        """
        Erstelle ein Galois-Feld-Element aus einem Hex-Wert.
        :param hex_value: Hex-Wert des Polynoms (z. B. '0x6').
        :param irreducible_poly: Irreduzibles Polynom des Grades m des Grades m für Erweiterungskörper `GF(2^m)`.
        """
        value: int = int(hex_value, 16)
        return cls(value, irreducible_poly)

    @classmethod
    def from_bitvector(cls, bitvector: List[int], irreducible_poly: int) -> 'GaloisFieldElement':
        """
        Erstelle ein Galois-Feld-Element aus einem Bitvektor.
        :param bitvector: Liste von 0 und 1 (z. B. [1, 1, 0] für x^2 + x).
        :param irreducible_poly: Irreduzibles Polynom des Grades m für Erweiterungskörper `GF(2^m)`.
        """
        value: int = 0
        for i, bit in enumerate(reversed(bitvector)):
            if bit:
                value |= 1 << i
        return cls(value, irreducible_poly)

    @classmethod
    def from_standard_field(cls, value: int, m: int) -> 'GaloisFieldElement':
        """
        Erstellt ein Element aus einem Standardfeld GF(2^m) mit vordefiniertem irreduziblem Polynom.
        :param value: Wert des Elements.
        :param m: Grad des Feldes (2, 3, 4, 5, 6, 7, oder 8).
        """
        if m not in IRREDUCIBLE_POLYNOMIALS:
            raise ValueError(f"Kein Standardpolynom für GF(2^{m}) definiert. Verfügbar: {list(IRREDUCIBLE_POLYNOMIALS.keys())}")
        
        return cls(value, IRREDUCIBLE_POLYNOMIALS[m])

    def _poly_reduction(self, value: int) -> int:
        """
        Führt eine Polynom-Division durch und gibt den Rest zurück.
        :param value: Das Polynom, das reduziert werden soll.
        :return: Der Rest der Polynom-Division von `value` durch `irreducible_poly`.
        """
        while value.bit_length() >= self.irreducible_poly.bit_length():
            shift = value.bit_length() - self.irreducible_poly.bit_length()
            value ^= self.irreducible_poly << shift  # Subtrahiere (XOR) das irreduzible Polynom, verschoben
        return value

    def _check_same_field(self, other: 'GaloisFieldElement') -> None:
        if self.irreducible_poly != other.irreducible_poly:
            raise ValueError("Elemente müssen aus demselben Galois-Feld stammen.")

    def __add__(self, other: 'GaloisFieldElement') -> 'GaloisFieldElement':
        self._check_same_field(other)
        result: int = self.value ^ other.value
        return GaloisFieldElement(result, self.irreducible_poly)

    def __sub__(self, other: 'GaloisFieldElement') -> 'GaloisFieldElement':
        return self.__add__(other)

    def __mul__(self, other: 'GaloisFieldElement') -> 'GaloisFieldElement':
        self._check_same_field(other)
        result: int = 0
        a: int = self.value
        b: int = other.value

        while b > 0:
            if b & 0b1:
                result ^= a
            b >>= 1
            a <<= 1
            a = self._poly_reduction(a)

        return GaloisFieldElement(result, self.irreducible_poly)

    def __pow__(self, exponent: int) -> 'GaloisFieldElement':
        """
        Potenzierung in GF(2^m) mit wiederholter Quadrierung.
        :param exponent: Exponent (muss >= 0 sein).
        :return: self^exponent
        """
        if exponent < 0:
            # Für negative Exponenten berechnen wir erst das multiplikative Inverse
            return self.inverse() ** (-exponent)
        if exponent == 0:
            return self.one_element()
        
        result = self.one_element()
        base = GaloisFieldElement(self.value, self.irreducible_poly)
        
        while exponent > 0:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        
        return result

    def __truediv__(self, other: 'GaloisFieldElement') -> 'GaloisFieldElement':
        """
        Division in GF(2^m): a / b = a * b^(-1)
        """
        return self * other.inverse()

    def inverse(self) -> 'GaloisFieldElement':
        """
        Berechnet das multiplikative Inverse mit dem erweiterten euklidischen Algorithmus.
        :return: Das multiplikative Inverse dieses Elements.
        :raises: ValueError wenn das Element 0 ist (kein Inverses existiert).
        """
        if self.value == 0:
            raise ValueError("Das Nullelement hat kein multiplikatives Inverses.")
        
        # Erweiterter euklidischer Algorithmus für Polynome
        old_r, r = self.irreducible_poly, self.value
        old_s, s = 0, 1
        
        while r != 0:
            quotient = self._poly_divide(old_r, r)
            old_r, r = r, old_r ^ self._poly_multiply(quotient, r)
            old_s, s = s, old_s ^ self._poly_multiply(quotient, s)
        
        # Das Ergebnis muss reduziert werden
        return GaloisFieldElement(old_s, self.irreducible_poly)

    def _poly_divide(self, dividend: int, divisor: int) -> int:
        """
        Polynom-Division: gibt den Quotienten zurück.
        """
        if divisor == 0:
            raise ValueError("Division durch Null-Polynom.")
        
        quotient = 0
        while dividend.bit_length() >= divisor.bit_length():
            shift = dividend.bit_length() - divisor.bit_length()
            quotient |= 1 << shift
            dividend ^= divisor << shift
        
        return quotient

    def _poly_multiply(self, a: int, b: int) -> int:
        """
        Polynom-Multiplikation ohne Reduktion.
        """
        result = 0
        while b > 0:
            if b & 1:
                result ^= a
            a <<= 1
            b >>= 1
        return result

    def __hash__(self) -> int:
        """
        Hash-Funktion für Verwendung in Sets und Dictionaries.
        """
        return hash((self.value, self.irreducible_poly))

    @classmethod
    def zero(cls, irreducible_poly: int) -> 'GaloisFieldElement':
        """
        Erstellt das Nullelement des Feldes.
        """
        return cls(0, irreducible_poly)

    @classmethod
    def one(cls, irreducible_poly: int) -> 'GaloisFieldElement':
        """
        Erstellt das Einselement des Feldes.
        """
        return cls(1, irreducible_poly)

    def zero_element(self) -> 'GaloisFieldElement':
        """
        Gibt das Nullelement dieses Feldes zurück.
        """
        return GaloisFieldElement.zero(self.irreducible_poly)

    def one_element(self) -> 'GaloisFieldElement':
        """
        Gibt das Einselement dieses Feldes zurück.
        """
        return GaloisFieldElement.one(self.irreducible_poly)

    def __repr__(self) -> str:
        return f"GFElement({bin(self.value)}, GF(2^{self.m}))"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GaloisFieldElement):
            return False
        return self.value == other.value and self.irreducible_poly == other.irreducible_poly

    def to_hex(self) -> str:
        """
        Gibt den Wert des Galois-Feld-Elements in Hexadezimalform zurück.
        """
        return hex(self.value)

    def to_bitvector(self) -> List[int]:
        """
        Gibt den Wert des Galois-Feld-Elements als Bitvektor (Liste von 0 und 1) zurück.
        """
        bit_length: int = self.m
        return [int(x) for x in bin(self.value)[2:].zfill(bit_length)]

    def to_polynomial(self) -> str:
        """
        Gibt den Wert des Galois-Feld-Elements als Polynom zurück (z. B. x^2 + 1).
        """
        terms: List[str] = []
        for i in range(self.value.bit_length()):
            if (self.value >> i) & 1:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(reversed(terms)) if terms else "0"

    def field_size(self) -> int:
        """
        Gibt die Größe des Feldes zurück (2^m).
        """
        return 2 ** self.m

    def order(self) -> int:
        """
        Berechnet die multiplikative Ordnung dieses Elements.
        Die Ordnung ist die kleinste positive Zahl k, sodass a^k = 1.
        """
        if self.value == 0:
            raise ValueError("Das Nullelement hat keine multiplikative Ordnung.")
        
        current = GaloisFieldElement(self.value, self.irreducible_poly)
        one_elem = self.one_element()
        order = 1
        
        while current != one_elem:
            current = current * self
            order += 1
            if order > self.field_size():
                raise ValueError("Ordnung zu groß - möglicherweise Implementierungsfehler.")
        
        return order

    def is_primitive(self) -> bool:
        """
        Prüft, ob dieses Element ein primitives Element ist.
        Ein Element ist primitiv, wenn seine Ordnung gleich (2^m - 1) ist.
        """
        if self.value == 0:
            return False
        try:
            return self.order() == self.field_size() - 1
        except ValueError:
            return False

    def frobenius(self, power: int = 1) -> 'GaloisFieldElement':
        """
        Wendet den Frobenius-Automorphismus an: x -> x^(2^power).
        :param power: Potenz des Frobenius (Standard: 1 für x -> x^2).
        """
        exp = 2 ** power
        return self ** exp

    @classmethod
    def all_elements(cls, irreducible_poly: int) -> List['GaloisFieldElement']:
        """
        Generiert alle Elemente des Feldes GF(2^m).
        """
        m = irreducible_poly.bit_length() - 1
        field_size = 2 ** m
        return [cls(i, irreducible_poly) for i in range(field_size)]

    @classmethod
    def random_element(cls, irreducible_poly: int) -> 'GaloisFieldElement':
        """
        Generiert ein zufälliges Element des Feldes.
        """
        import random
        m = irreducible_poly.bit_length() - 1
        field_size = 2 ** m
        random_value = random.randint(0, field_size - 1)
        return cls(random_value, irreducible_poly)
