"""
@summary:  An experimental prototype of polynomials (a Work-In-Progress)
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
from IPython.display import display, Math  # For Latex output in Jupyter notebooks


class Term:
    """Represents a term of a polynomial.  Here's an example polynomial with four
    terms, separated by spaces: -2 -4x +7x^2 -3x^4
    """
    
    def __init__(self, coefficient, order, varname='x'):
        if (order < 0) or not isinstance(order, int):
            raise ValueError("Order must be a non-negative integer.")
        else:
            self.__coefficient = coefficient
            self.__order = order
            self.__varname = varname
        
    def __repr__(self):
        if self.__varname == 'x':
            return f"Term({self.__coefficient}, {self.__order})"
        else:
            return f"Term({self.__coefficient}, {self.__order}, {self.__varname})"
    
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

    def __add__(self, other):
        """Add two like terms and return the resulting term."""
        if self.like_term(other):
            return Term(self.__coefficient + other.coefficient, self.__order)
        else:
            raise ValueError(f"Add: {self} not like {other}")

    def __sub__(self, other):
        """Subtract two like terms and return the resulting term."""
        if self.like_term(other):
            return Term(self.__coefficient - other.coefficient, self.__order)
        else:
            raise ValueError(f"Sub: {self} not like {other}")

    def __neg__(self):
        """Return a copy of this term, where the coefficient has been negated."""
        return Term(- self.__coefficient, self.__order, self.__varname)

    def __mul__(self, other):
        """Multiply two terms and return the resulting term."""
        if is_number(other):
            return Term(self.__coefficient * other,
                        self.__order,
                        self.__varname)
        elif isinstance(other, Term) and (self.__varname == other.varname()):
            return Term(self.__coefficient * other.coefficient,
                        self.__order + other.order,
                        self.__varname)
        else:
            raise ValueError(f"Mult: Variables must be the same, {self.__varname} != {other.varname()}")

    __rmul__ = __mul__

    def __pow__(self, n):
        """Return the nth power of this term."""
        result = Term(1, 0, varname=self.__varname)
        for n in range(n, 0, -1):
            result *= self
        return result

    def __eq__(self, other):
        """Return True if the two terms are equal; return False otherwise."""
        return (self.__coefficient == other.coefficient and
                self.__order == other.order and
                self.__varname == other.varname())

    def __call__(self, x):
        """Compute and return the value of the term for x"""
        return self.__coefficient * (x ** self.__order)

    def like_term(self, other):
        """Return True if self & other are like terms (same variable and same order)."""
        if isinstance(other, Term):
            return (self.__varname == other.varname()) and (self.__order == other.order)
        elif is_number(other):
            if self.is_constant():
                return True
            else:
                return False
    
    @property
    def coefficient(self):
        """Return the value of the term's coefficient"""
        return self.__coefficient
    
    @property
    def order(self):
        """Return the order of the term."""
        return self.__order
    
    def varname(self, new_varname=None):
        """Return or change the varname used for the term's variable."""
        if new_varname is not None:
            if isinstance(new_varname, str):
                self.__varname = new_varname
            else:
                raise ValueError("Variable name must be a string.")
        return self.__varname

    def unpack(self):
        """Return all three quantities that make up the Term."""
        return self.__coefficient, self.__order, self.__varname

    def copy(self):
        """Return an exact copy of the Term."""
        return Term(self.__coefficient, self.__order, self.__varname)

    def is_order_n(self, n):
        """Return the coefficient if the Term's order is n.  Return False, otherwise."""
        if self.__order == n:
            return self.__coefficient
        else:
            return False

    def is_constant(self):
        """Return True if the term represents a constant value.  Return False, otherwise."""
        return self.is_order_n(0)
        
    def is_linear(self):
        """Return True if the term is linear in the variable.  Return False, otherwise."""
        return self.is_order_n(1)

    def is_quadratic(self):
        """Return True if the term is quadratic in the variable.  Return False, otherwise."""
        return self.is_order_n(2)

    # TODO: Add optional int arg, n, to differentiate n times
    def derivative(self):
        """Return a Term that represents the derivative of this term."""
        if self.__order == 0:
            return Term(0, 0)
        else:
            return Term(self.coefficient * self.order, self.order - 1, self.__varname)

    def antiderivative(self):
        """Return a Term that represents the antiderivative of this term."""
        order_p_1 = self.__order + 1
        return Term(self.coefficient / order_p_1, order_p_1, self.__varname)


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

        term_list = None

        # The following sequence of if-else statements will set the values of
        # 'term_list' and 'varname'. In the latter case, possibly overriding
        # the input varname.

        # e.g., poly_spec = [-2, -4, 7, 0, -3]
        if isinstance(poly_spec[0], int) or isinstance(poly_spec[0], float):
            term_list = [Term(coeff, order, varname) for order, coeff in enumerate(poly_spec)]

        # e.g., poly_spec = [(-3, 4), (-4, 1), (7, 2), (-2, 0)]
        #                or [[-4, 1], [7, 2], [-2, 0], [-3, 4]]
        elif isinstance(poly_spec[0], tuple) or isinstance(poly_spec[0], list):
            term_list = [Term(tup[0], tup[1], varname) for tup in poly_spec]

        # e.g., poly_spec = [Term(-2,0), Term(-4,1), Term(7,2), Term(-3,4)]
        # NOTE: All terms should use the same variable name.  The default varname,
        # or whatever varname is input to the constructor, is ignored in favor of the
        # varname used in the list of terms.
        elif isinstance(poly_spec[0], Term):
            # Get list of all unique term variable names
            varnames = list({trm.varname() for trm in poly_spec})
            # If all the terms use the same variable name, then use it for the polynomial's
            # variable name, overriding whatever varname was input.
            if len(varnames) == 1:
                varname = varnames[0]
                term_list = poly_spec

        # e.g., poly_spec = "-2 -4x +7x^2 -3x^4"
        elif isinstance(poly_spec, str):
            # Extract unique characters from poly_spec
            var_list = list({char for char in poly_spec if char.isalpha()})
            # There should only be one character in var_list, e.g., ['x']
            num_vars = len(var_list)
            if num_vars == 0:
                pass  # Use the input or default varname
            elif num_vars == 1:
                varname = var_list[0]
            else:
                raise ValueError(f"Too many variables in polynomial specification: {var_list}")
            term_list = parse_polynomial(poly_spec, varname)

        else:
            raise ValueError("Input to Polynomial constructor not valid")

        self.__varname = varname

        self.__terms = [term for term in combine_like_terms(term_list) if term.coefficient != 0]
        if len(self.__terms) == 0:
            self.__terms.append(Term(0, 0))

        self.__order = max([t.order for t in self.__terms])

        self.__lookup_term = {t.order: t for t in self.__terms}

    def __repr__(self):
        # Estimate the size of the two possible representations
        chars_using_tuples = 8 * len(self.__terms)
        chars_using_coeffs = 3 * self.__order
        # Use the representation that is estimated to be the shortest
        if chars_using_tuples < chars_using_coeffs:
            if self.__varname == 'x':
                return f"Poly({self.term_tuples()})"
            else:
                return f"Poly({self.term_tuples()}, '{self.__varname}')"
        else:
            if self.__varname == 'x':
                return f"Poly({self.term_coefficients()})"
            else:
                return f"Poly({self.term_coefficients()}, '{self.__varname}')"

    def __str__(self):
        poly_str = ""
        for term in self.__terms:
            poly_str += " " + str(term)
        return poly_str[1:]
    
    def __call__(self, x):
        return fnc.reduce(lambda a, b: a + b, map(lambda term: term(x), self.__terms))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__add__(Poly([other, 0], self.varname()))
        elif self.__varname == other.varname():
            return Poly(self.__terms + other.terms)
        else:
            raise ValueError(f"Variable names must be equal, {self.__varname} != {other.varname()}")

    __radd__ = __add__  # Handles Number + Poly, whereas the above handles Poly + Number

    def __neg__(self):
        """Return a copy of this polynomial where all of the terms have been negated."""
        return Poly([-t for t in self.terms], self.__varname)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            # return self.__sub__(Poly([other, 0], self.varname()))
            return self.__sub__(Poly([other], self.varname()))
        if self.__varname == other.varname():
            return Poly(self.terms + (- other).terms, self.__varname)
        else:
            raise ValueError(f"Variable names must be equal, {self.__varname} != {other.varname()}")

    def __rsub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other_poly = Poly([other], self.varname())
            return other_poly.__sub__(self)
        else:
            raise ValueError(f"Cannot subtract from, {other}")

    def __mul__(self, other):
        """Return the product of the polynomials, self and other."""
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(Poly([other], self.varname()))
        elif self.__varname == other.varname():
            prod_terms = list()
            for t1 in self.__terms:
                prod_terms += [t1 * t2 for t2 in other.terms]
            return Poly(prod_terms, self.__varname)
        else:
            raise ValueError(f"Variable names must be equal, {self.__varname} != {other.varname()}")

    __rmul__ = __mul__  # Handles Number * Poly, whereas the above handles Poly * Number

    def __pow__(self, n):
        """Return the nth power of this polynomial."""
        result = Poly([1, 0], varname=self.varname())
        for n in range(n, 0, -1):
            result *= self
        return result

    @property
    def order(self):
        return self.__order

    @property
    def terms(self):
        return self.__terms

    def varname(self, new_varname=None):
        """Return or change the string (character) used for the polynomial's variable."""
        if new_varname is not None:
            if isinstance(new_varname, str):
                [t.varname(new_varname) for t in self.__terms]
                self.__varname = new_varname
            else:
                raise ValueError("Variable name must be a string.")
        return self.__varname

    def term(self, order):
        return self.__lookup_term[order]

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

    def copy(self):
        """Return a copy of this polynomial."""
        return Poly([Term(t.coefficient, t.order, t.varname())
                     for t in self.__terms],
                    self.__varname)

    def derivative(self):
        """Return the derivative of this polynomial."""
        return Poly([t.derivative() for t in self.__terms], self.__varname)

    def antiderivative(self, constant_term=0):
        """Return an antiderivative of this polynomial."""
        return Poly([t.antiderivative() for t in self.__terms] + [Term(constant_term, 0)], self.__varname)


def latex(str):
    """Print the string, str, using Latex."""
    display(Math(rf"{str}"))


def show_subst(u, v):
    """A convenience function for displaying term & polynomial substitutions,
    u & v must both be callable."""
    subst = u(v)
    print(f"({u})({u.varname()}={v}) ==> {subst}")
    return subst


def num(st):
    """Figure out if the input string represents an int or a float and return
    the appropriate numeric value."""
    try:
        result = int(st)
    except ValueError:
        try:
            result = float(st)
        except ValueError:
            raise ValueError(f"Could not convert {st} to int or float.")
    return result


def is_number(x):
    return isinstance(x, int) or isinstance(x, float)


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

    return Term(args[0], args[1], varname)


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


def from_roots(roots, varname='x'):
    return fnc.reduce(lambda p, q: p * q, [Poly([r, -1], varname) for r in roots])
