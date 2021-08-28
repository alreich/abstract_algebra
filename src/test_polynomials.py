"""
@author: Alfred J. Reich

"""

from unittest import TestCase
from polynomials import *


class TestPolynomials(TestCase):

    # def setUp(self) -> None:
    #     pass

    # def test_power_1(self):
    #     self.assertEqual(power(2, 3), 8)

    def test_parse_term_1(self):
        self.assertEqual(parse_term('-3x^4', 'x'), Term(-3, 4))

    def test_parse_term_2(self):
        self.assertEqual(parse_term('x^4', 'x'), Term(1, 4))

    def test_parse_term_3a(self):
        self.assertEqual(parse_term('x', 'x'), Term(1, 1))

    def test_parse_term_3b(self):
        self.assertEqual(parse_term('+x', 'x'), Term(1, 1))

    def test_parse_term_3c(self):
        self.assertEqual(parse_term('-x', 'x'), Term(-1, 1))

    def test_parse_term_4a(self):
        self.assertEqual(parse_term('3x', 'x'), Term(3, 1))

    def test_parse_term_4b(self):
        self.assertEqual(parse_term('-3x', 'x'), Term(-3, 1))

    def test_parse_term_4c(self):
        self.assertEqual(parse_term('+3x', 'x'), Term(3, 1))

    def test_parse_polynomial_1(self):
        poly_str = '-2 -4x +7x^2 -3x^4'
        result = [Term(-2, 0), Term(-4, 1), Term(7, 2), Term(-3, 4)]
        self.assertEqual(parse_polynomial(poly_str, 'x'), result)

    def test_combine_like_terms_1(self):
        test_terms_1 = [Term(7, 2), Term(-2, 0), Term(-4, 1), Term(-3, 1), Term(5, 0)]
        result = [Term(3, 0), Term(-7, 1), Term(7, 2)]
        self.assertEqual(combine_like_terms(test_terms_1), result)

    def test_term_1(self):
        self.assertEqual(Term(-3, 4), Term(-3, 4))

    def test_polynomial_1(self):
        coeffs = [-2, -4, 7, 0, -3]
        p = Poly(coeffs)
        result = [Term(-2,0), Term(-4,1), Term(7,2), Term(-3,4)]
        self.assertEqual(p.terms, result)
