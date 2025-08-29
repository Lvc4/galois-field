import unittest
from galois_field.galois_field_element import GaloisFieldElement, IRREDUCIBLE_POLYNOMIALS

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

    # New tests for added features

    def test_division_and_inverse(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        b = GaloisFieldElement.from_hex("0x60", self.irreducible_poly)
        
        # Test inverse
        a_inv = a.inverse()
        self.assertEqual(a * a_inv, GaloisFieldElement.one(self.irreducible_poly))
        
        # Test division
        c = a / b
        self.assertEqual(c, a * b.inverse())
        self.assertEqual(c * b, a)

    def test_inverse_zero_element(self):
        zero = GaloisFieldElement.zero(self.irreducible_poly)
        with self.assertRaises(ValueError):
            zero.inverse()

    def test_power_operations(self):
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        
        # Test basic powers
        self.assertEqual(a ** 0, GaloisFieldElement.one(self.irreducible_poly))
        self.assertEqual(a ** 1, a)
        self.assertEqual(a ** 2, a * a)
        self.assertEqual(a ** 3, a * a * a)
        
        # Test negative powers
        a_inv = a.inverse()
        self.assertEqual(a ** (-1), a_inv)
        self.assertEqual(a ** (-2), a_inv * a_inv)

    def test_hash_function(self):
        a = GaloisFieldElement(0b1010, self.irreducible_poly)
        b = GaloisFieldElement(0b1010, self.irreducible_poly)
        c = GaloisFieldElement(0b1100, self.irreducible_poly)
        
        # Equal elements should have equal hashes
        self.assertEqual(hash(a), hash(b))
        
        # Test that elements can be used in sets
        element_set = {a, b, c}
        self.assertEqual(len(element_set), 2)  # a and b are equal

    def test_zero_and_one_elements(self):
        zero = GaloisFieldElement.zero(self.irreducible_poly)
        one = GaloisFieldElement.one(self.irreducible_poly)
        
        self.assertEqual(zero.value, 0)
        self.assertEqual(one.value, 1)
        
        # Test additive identity
        a = GaloisFieldElement.from_hex("0x02", self.irreducible_poly)
        self.assertEqual(a + zero, a)
        
        # Test multiplicative identity
        self.assertEqual(a * one, a)
        
        # Test instance methods
        self.assertEqual(a.zero_element(), zero)
        self.assertEqual(a.one_element(), one)

    def test_field_size(self):
        a = GaloisFieldElement(5, self.irreducible_poly)
        expected_size = 2 ** (self.irreducible_poly.bit_length() - 1)
        self.assertEqual(a.field_size(), expected_size)

    def test_order_and_primitive(self):
        # For GF(2^4) with irreducible polynomial x^4 + x + 1
        irreducible_poly_4 = 0b10011
        
        # Element with value 2 (x) should be primitive in GF(2^4)
        x = GaloisFieldElement(2, irreducible_poly_4)
        
        # Test order calculation
        order = x.order()
        self.assertEqual(order, 15)  # 2^4 - 1 = 15
        
        # Test if it's primitive
        self.assertTrue(x.is_primitive())
        
        # Zero element has no order
        zero = GaloisFieldElement.zero(irreducible_poly_4)
        with self.assertRaises(ValueError):
            zero.order()
        
        self.assertFalse(zero.is_primitive())

    def test_frobenius_mapping(self):
        a = GaloisFieldElement(5, self.irreducible_poly)
        
        # Frobenius mapping: x -> x^2
        frobenius_a = a.frobenius()
        expected = a ** 2
        self.assertEqual(frobenius_a, expected)
        
        # Double frobenius: x -> x^4
        double_frobenius = a.frobenius(2)
        expected = a ** 4
        self.assertEqual(double_frobenius, expected)

    def test_standard_fields(self):
        # Test creation from standard fields
        elem = GaloisFieldElement.from_standard_field(5, 4)
        self.assertEqual(elem.irreducible_poly, IRREDUCIBLE_POLYNOMIALS[4])
        self.assertEqual(elem.value, 5)
        
        # Test invalid field degree
        with self.assertRaises(ValueError):
            GaloisFieldElement.from_standard_field(5, 10)

    def test_all_elements(self):
        # Test for small field GF(2^2)
        irreducible_poly_2 = IRREDUCIBLE_POLYNOMIALS[2]
        all_elems = GaloisFieldElement.all_elements(irreducible_poly_2)
        
        self.assertEqual(len(all_elems), 4)  # 2^2 = 4
        values = [elem.value for elem in all_elems]
        self.assertEqual(sorted(values), [0, 1, 2, 3])

    def test_random_element(self):
        random_elem = GaloisFieldElement.random_element(self.irreducible_poly)
        self.assertIsInstance(random_elem, GaloisFieldElement)
        self.assertEqual(random_elem.irreducible_poly, self.irreducible_poly)
        self.assertTrue(0 <= random_elem.value < random_elem.field_size())

    def test_input_validation(self):
        # Test invalid value
        with self.assertRaises(ValueError):
            GaloisFieldElement(-1, self.irreducible_poly)
        
        with self.assertRaises(ValueError):
            GaloisFieldElement("invalid", self.irreducible_poly)
        
        # Test invalid irreducible polynomial
        with self.assertRaises(ValueError):
            GaloisFieldElement(5, -1)
        
        with self.assertRaises(ValueError):
            GaloisFieldElement(5, 1)

    def test_irreducible_polynomials_constants(self):
        # Test that all predefined polynomials work
        for m, poly in IRREDUCIBLE_POLYNOMIALS.items():
            elem = GaloisFieldElement(1, poly)
            self.assertEqual(elem.m, m)
            self.assertEqual(elem.field_size(), 2 ** m)

if __name__ == "__main__":
    unittest.main()
