"""
@summary:  An experimental prototype of polynomials (still a work-in-progress)
@author:   Alfred J. Reich, Ph.D.
@contact:  al.reich@gmail.com
@copyright: Copyright (C) 2021 Alfred J. Reich, Ph.D.
@license:  MIT
@requires: Python 3.7.7 or higher
@since:    2021.08
@version:  0.1.0
"""

import functools as fnc
import itertools as it


class Term:
    """Represents a term of a polynomial.  Here's an example polynomial with four
    terms, separated by spaces: -2 -4x +7x^2 -3x^4
    """
    
    def __init__(self, coefficient, order, varname='x'):
        self.__coefficient = coefficient
        self.__order = order
        self.__varname = varname
        
    def __repr__(self):
        return f"Term({self.__coefficient},{self.__order})"
    
    def __str__(self):
        if self.__coefficient > 0:
            sign = "+"
        else:
            sign = ""
        if self.__order == 0:
            return f"{sign}{self.__coefficient}"
        elif self.__order == 1:
            return f"{sign}{self.__coefficient}{self.__varname}"
        else:
            return f"{sign}{self.__coefficient}{self.__varname}^{self.__order}"
        
    def __call__(self, x):
        """Compute and return the value of the term for x"""
        return self.__coefficient * power(x, self.__order)
    
    def __add__(self, other):
        """If two terms have the same order, add them and return the resulting term."""
        if self.__order == other.__order:
            return Term(self.__coefficient + other.__coefficient, self.__order)
        else:
            raise ValueError(f"Terms must be of the same order, {self.__order} != {other.__order}")
    
    def __mul__(self, other):
        """Multiply two terms and return the resulting term."""
        return Term(self.__coefficient * other.__coefficient,
                    self.__order + other.__order)
    
    def __eq__(self, other):
        """Return True if the two terms are equal; return False otherwise."""
        return (self.__varname == other.__varname and
                self.__order == other.__order and
                self.__coefficient == other.__coefficient)
    
    @property
    def coefficient(self):
        """Return the value of the term's coefficient"""
        return self.__coefficient
    
    @property
    def order(self):
        """Return the order of the term."""
        return self.__order
    
    def varname(self, new_varname=None):
        """Return or change the string (character) used for the term's variable."""
        if new_varname is not None:
            if isinstance(new_varname, str):
                self.__varname = new_varname
            else:
                raise ValueError("Variable name must be a string.")
        return self.__varname
    
    def is_constant(self):
        """Return True if the term represents a constant value.  Return False, otherwise."""
        if self.__order == 0:
            return self.__coefficient
        else:
            return False
        
    def is_linear(self):
        """Return True if the term is linear in the variable.  Return False, otherwise."""
        if self.__order == 1:
            return self.__coefficient
        else:
            return False


class Poly:
    """A callable class for polynomials.  The constructor takes the polynomial as a 
    single string, as long as the terms of the polynomial are separated by spaces.
    """
    
    def __init__(self, poly_spec, varname='x'):
        """Given a list of coefficients, coeff, return a Polynomial.

        poly_spec is the specification required to build the polynomial.
        It can take one of five different forms as shown below.

        1. An ordered list of term coefficients, where the position in
        the list represents the order of the term:
        [-2, -4, 7, 0, -3]

        2. A list (no required order) of two-element tuples, where the
        first element is a term's coefficient and the second is its order:
        [(-3, 4), (-4,1), (7, 2), (-2,0)]

        3. Same as 2, except the coefficient/order pairs can be lists:
        [[-4,1], [7, 2], [-2,0], [-3, 4]]

        4. A list of Term instances (no required order):
        [Term(-2,0), Term(-4,1), Term(7,2), Term(-3,4)]

        5. A string representation of a polynomial: "-2 -4x +7x^2 -3x^4", where
        there must be a space between each term, and, except for the first term,
        every term must begin with a + or - sign, and then a number, unless the
        number is a 1.
        """

        if isinstance(poly_spec[0], int) or isinstance(poly_spec[0], float):
            terms = [Term(coeff, order, varname) for order, coeff in enumerate(poly_spec)]

        elif isinstance(poly_spec[0], tuple) or isinstance(poly_spec[0], list):
            terms = [Term(tup[0], tup[1], varname) for tup in poly_spec]

        elif isinstance(poly_spec[0], Term):
            if all([trm.varname() == varname for trm in poly_spec]):
                terms = poly_spec
            else:
                raise ValueError(f"All variable names must be the same as '{varname}'")

        elif isinstance(poly_spec[0], str):
            terms = parse_polynomial(poly_spec, 'x')

        else:
            raise ValueError("Input to Polynomial constructor not valid")

        self.__varname = varname

        self.__terms = [term for term in combine_like_terms(terms) if term.coefficient != 0]
        if len(self.__terms) == 0:
            self.__terms.append(Term(0, 0))

        self.__order = max([t.order for t in self.__terms])

    def __repr__(self):
        chars_using_tuples = 8 * len(self.__terms)
        chars_using_coeffs = 3 * self.__order
        if chars_using_tuples < chars_using_coeffs:
            return f"Poly({self.term_tuples()})"
        else:
            return f"Poly({self.term_coefficients()})"

    def __str__(self):
        poly_str = ""
        for term in self.__terms:
            poly_str += " " + str(term)
        return poly_str[1:]
    
    def __call__(self, x):
        return fnc.reduce(lambda a, b: a + b, map(lambda term: term(x), self.__terms))

    def __add__(self, other):
        if self.__varname == other.varname():
            return Poly(self.__terms + other.terms())
        else:
            raise ValueError(f"Variable names must be equal, {self.__varname} != {other.varname()}")

    def __mul__(self, other):
        if self.__varname == other.varname():
            prod_terms = list()
            for t1 in self.__terms:
                prod_terms += [t1 * t2 for t2 in other.terms()]
            return Poly(prod_terms)
        else:
            raise ValueError(f"Variable names must be equal, {self.__varname} != {other.varname()}")

    @property
    def order(self):
        return self.__order

    def terms(self):
        return self.__terms

    def varname(self):
        return self.__varname

    def term_tuples(self):
        """Returns a list of the polynomial's (coeff, order) tuples.  Suitable as input
        to recreate the polynomial"""
        ts = self.__terms
        return [(t.coefficient, t.order) for t in ts]

    def term_coefficients(self):
        """Returns a 1D array of the polynomial's coefficients, where the array index
        is the coefficient's order.  Suitable as input to recreate the polynomial"""
        coeffs = [0] * (self.__order + 1)
        for t in self.__terms:
            coeffs[t.order] = t.coefficient
        return coeffs


def power(x, n):
    result = 1
    for _ in range(n):
        result = result * x
    return result


def num(st):
    try:
        result = int(st)
    except ValueError:
        try:
            result = float(st)
        except ValueError:
            raise ValueError(f"Could not convert {st} to int or float.")
    return result


def parse_term(term_str, varname):
    """A very hacky term string parser.  Returns a Term from the input string."""

    if varname in term_str:
        varpower = varname + "^"
        if varpower in term_str:
            foo = term_str.split(varpower)  # e.g., '-3x^4' ==> ('-3', '4')
            if foo[0] == '' or foo[0] == '+':
                args = [1, num(foo[1])]  # e.g., '+x^2' ==> ('1', '2')
            elif foo[0] == '-':
                args = [-1, num(foo[1])]  # e.g., '-x^2' ==> ('-1', '2')
            else:
                # args = list(map(lambda x: num(x), foo))
                args = [num(foo[0]), num(foo[1])]  # e.g., '-3x^4' ==> ('-3', '4')
        else:
            foo = term_str.split(varname)[0]
            if foo == '+' or foo == '-' or foo == '':
                coeff_str = foo + '1'
                args = [num(coeff_str), 1]
            else:
                args = [num(foo), 1]
    else:
        args = [num(term_str), 0]

    return Term(args[0], args[1])


def parse_polynomial(poly_str, varname):
    """Given the string representation of a polynomial and the name of the polynomial's
    variable, return the list Terms that represent it. This is an extreme hack.
    The terms in the polynomial string must be separated by a space.
    EXAMPLE: parse_polynomial('-2 -4x +7x^2 -3x^4', 'x')
    """
    return [parse_term(term, varname) for term in poly_str.split()]


# TODO: Make this function also consider 'varname'
def combine_like_terms(terms):
    """Given a list of Terms, this function returns a possibly smaller list of Terms,
    where terms with the same order ("like terms") have been combined."""
    result = list()
    # NOTE: 'groupby' **requires** the input list be sorted on the key used for grouping
    terms_sorted = sorted(terms, key=lambda x: x.order)
    for _, like_terms in it.groupby(terms_sorted, lambda x: x.order):
        combined_term = fnc.reduce(lambda t, s: t + s, like_terms)
        result.append(combined_term)
    return result
