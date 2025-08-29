#!/usr/bin/env python3
"""
Galois Field Demo - Showcasing all the new features in version 0.2.0

This script demonstrates the comprehensive functionality of the improved galois-field library.
"""

from galois_field import GaloisFieldElement, IRREDUCIBLE_POLYNOMIALS

def demo_basic_operations():
    print("=== Basic Operations Demo ===")
    # Use GF(2^4) with predefined polynomial
    poly = IRREDUCIBLE_POLYNOMIALS[4]
    print(f"Using GF(2^4) with polynomial: {bin(poly)} = x^4 + x + 1")
    
    a = GaloisFieldElement(0b1010, poly)  # x^3 + x  
    b = GaloisFieldElement(0b1100, poly)  # x^3 + x^2
    
    print(f"a = {a.to_polynomial()} (value: {a.value})")
    print(f"b = {b.to_polynomial()} (value: {b.value})")
    print(f"a + b = {(a + b).to_polynomial()}")
    print(f"a * b = {(a * b).to_polynomial()}")
    print(f"a / b = {(a / b).to_polynomial()}")
    print(f"a^3 = {(a ** 3).to_polynomial()}")
    print()

def demo_field_theory():
    print("=== Field Theory Functions Demo ===")
    elem = GaloisFieldElement.from_standard_field(2, 4)  # x in GF(2^4)
    print(f"Element: {elem.to_polynomial()}")
    print(f"Field size: {elem.field_size()}")
    print(f"Element order: {elem.order()}")
    print(f"Is primitive: {elem.is_primitive()}")
    print(f"Multiplicative inverse: {elem.inverse().to_polynomial()}")
    print(f"Frobenius (x -> x^2): {elem.frobenius().to_polynomial()}")
    print()

def demo_collections():
    print("=== Collections Support Demo ===")
    poly = IRREDUCIBLE_POLYNOMIALS[3]
    
    # Using elements in sets
    elements = {
        GaloisFieldElement(1, poly),
        GaloisFieldElement(2, poly),
        GaloisFieldElement(1, poly),  # Duplicate
    }
    print(f"Set of elements (duplicates removed): {len(elements)} unique elements")
    
    # Using elements as dictionary keys
    element_info = {}
    for i in range(4):  # All elements of GF(2^2) 
        elem = GaloisFieldElement(i, IRREDUCIBLE_POLYNOMIALS[2])
        if elem.value == 0:
            element_info[elem] = "Zero element"
        elif elem.value == 1:
            element_info[elem] = "One element"
        else:
            element_info[elem] = f"Order: {elem.order()}"
    
    print("Element properties in GF(2^2):")
    for elem, info in element_info.items():
        print(f"  {elem.to_polynomial(): <6} -> {info}")
    print()

def demo_field_generation():
    print("=== Field Generation Demo ===")
    # Generate all elements of GF(2^3)
    all_elements = GaloisFieldElement.all_elements(IRREDUCIBLE_POLYNOMIALS[3])
    print(f"All elements of GF(2^3) ({len(all_elements)} total):")
    for elem in all_elements:
        if elem.value == 0:
            print(f"  {elem.value}: {elem.to_polynomial(): <8} (zero)")
        elif elem.value == 1:
            print(f"  {elem.value}: {elem.to_polynomial(): <8} (one)")
        else:
            order = elem.order() 
            primitive = " (primitive)" if elem.is_primitive() else ""
            print(f"  {elem.value}: {elem.to_polynomial(): <8} order={order}{primitive}")
    
    # Random element
    random_elem = GaloisFieldElement.random_element(IRREDUCIBLE_POLYNOMIALS[4])
    print(f"\nRandom element from GF(2^4): {random_elem.to_polynomial()}")
    print()

def demo_advanced_operations():
    print("=== Advanced Operations Demo ===")
    # Work with larger field GF(2^8) 
    poly = IRREDUCIBLE_POLYNOMIALS[8]
    a = GaloisFieldElement(0x53, poly)  # Some element
    
    print(f"Element in GF(2^8): {a.to_polynomial()}")
    print(f"As hex: {a.to_hex()}")
    print(f"As bitvector: {a.to_bitvector()}")
    
    # Power operations
    print(f"a^2 = {(a**2).to_hex()}")
    print(f"a^(-1) = {(a**(-1)).to_hex()}")  
    print(f"a^255 = {(a**255).to_hex()}")  # Should be 1 since order divides 255
    
    # Double Frobenius
    print(f"Frobenius^2 (x -> x^4): {a.frobenius(2).to_hex()}")
    print()

def demo_error_handling():
    print("=== Error Handling Demo ===")
    try:
        # Invalid value
        GaloisFieldElement(-1, IRREDUCIBLE_POLYNOMIALS[4])
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        # Division by zero equivalent (inverse of zero)
        zero = GaloisFieldElement.zero(IRREDUCIBLE_POLYNOMIALS[4])
        zero.inverse()
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        # Invalid field degree
        GaloisFieldElement.from_standard_field(5, 15)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print()

def main():
    print("🔢 Galois Field Library v0.2.0 - Comprehensive Demo")
    print("=" * 60)
    
    demo_basic_operations()
    demo_field_theory()
    demo_collections()
    demo_field_generation()
    demo_advanced_operations()
    demo_error_handling()
    
    print("✅ All demos completed successfully!")
    print("The galois-field library now provides comprehensive GF(2^m) functionality!")

if __name__ == "__main__":
    main()