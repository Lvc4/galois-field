"""
Galois Field Library

This library implements elements of the Galois Field GF(2^m) with basic field operations.
"""

from .galois_field_element import GaloisFieldElement, IRREDUCIBLE_POLYNOMIALS

__version__ = "0.2.0"
__all__ = ["GaloisFieldElement", "IRREDUCIBLE_POLYNOMIALS"]