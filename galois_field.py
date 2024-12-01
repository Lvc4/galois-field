from typing import List

class GaloisFieldElement:
    def __init__(self, value: int, irreducible_poly: int) -> None:
        """
        Galois-Feld-Element initialisieren (nur für GF(2^m)).
        :param value: Ganzzahldarstellung des Polynoms (z. B. 0b101 für x^2 + 1).
        :param irreducible_poly: Irreduzibles Polynom des Grades m für GF(2^m).
        """
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

    def _poly_reduction(self, value: int) -> int:
        """
        Führt eine Polynom-Division durch und gibt den Rest zurück.
        :param value: Das Polynom, das reduziert werden soll.
        :return: Der Rest der Polynom-Division von `value` durch `irreducible_poly`.
        """
        while value.bit_length() >= self.m:
            shift = value.bit_length() - self.irreducible_poly.bit_length()
            value ^= (self.irreducible_poly << shift)
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
