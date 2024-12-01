import unittest
from galois_field.galois_field_element import GaloisFieldElement

class TestGaloisFieldElement(unittest.TestCase):
    def setUp(self):
        self.irreducible_poly = 0b100011011

    def test_from_hex(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        b = GaloisFieldElement(0b00000010, self.irreducible_poly)
        self.assertEqual(a, b)

    def test_to_polynomial(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        self.assertEqual(a.to_polynomial(), "x")
        b = GaloisFieldElement.from_hex("0x60", self.irreducible_poly)
        self.assertEqual(b.to_polynomial(), "x^6 + x^5")

    def test_addition(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        b = GaloisFieldElement.from_hex("0x60", self.irreducible_poly)
        c = a + b
        self.assertEqual(c, GaloisFieldElement.from_hex("0x62", self.irreducible_poly))

    def test_subtraction(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        b = GaloisFieldElement.from_hex("0x60", self.irreducible_poly)
        c = a - b
        self.assertEqual(c, GaloisFieldElement.from_hex("0x62", self.irreducible_poly))

    def test_multiplication(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        b = GaloisFieldElement.from_hex("0x60", self.irreducible_poly)
        c = a * b
        self.assertEqual(c, GaloisFieldElement.from_hex("0xC0", self.irreducible_poly))

    def test_equality(self):
        a = GaloisFieldElement(0b1010, self.irreducible_poly)
        b = GaloisFieldElement(0b1010, self.irreducible_poly)
        c = GaloisFieldElement(0b1100, self.irreducible_poly)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_invalid_addition(self):
        a = GaloisFieldElement(0b1010, self.irreducible_poly)
        b = GaloisFieldElement(0b1100, 0b1011)
        with self.assertRaises(ValueError):
            _ = a + b

if __name__ == "__main__":
    unittest.main()
