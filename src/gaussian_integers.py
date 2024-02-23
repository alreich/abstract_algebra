"""A Gaussian Integer class, together with associated functions.

A Gaussian integer is a complex number whose real and imaginary parts are both integers.
In this module, a Gaussian integer is represented in the form, Gint(re, im), where re is
the real integer and im is the imaginary integer. The Gint class supports the arithmetic
of Gaussian integers using numeric-style operators: +, -, *, /, //, %, **, +=, -=, *=,
and /=, along with a modified version of divmod, called mod_divmod, and two functions
related to the Greatest Common Divisor: gcd and xgcd.

Example:
  > from gaussian_integers import Gint, mod_divmod, gcd, xgcd
  >
  > alpha = Gint(11, 3)
  > beta = Gint(1, 8)
  > a, x, y = xgcd(alpha, beta)
  > print(f"{alpha * x + beta * y} = {alpha} * {x} + {beta} * {y}")
  >
  > (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j

"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "0.1.0"


from math import sqrt


class Gint:
    """Gaussian Integer Class with arithmetic and related functionality.

    A Gaussian integer, Gint, has two integer input values, re & im.
    Floats and complex numbers can be entered, but they will be rounded to the
    nearest integers. If a complex number is provided for re, then the value of
    im will be ignored, and the complex number's components, real & imag, will be
    rounded to nearest integers and used as inputs for re & im, respectively.
    """

    def __init__(self, re: (int, float, complex) = 0, im: (int, float) = 0):
        """Instantiate a Gaussian integer, Gint(re=0, im=0)."""

        if isinstance(re, int):
            self.real = re
        elif isinstance(re, float):
            self.real = round(re)
        elif isinstance(re, complex):
            self.real = round(re.real)
        else:
            raise TypeError(f"{re} cannot be used for the real part of a Gint instance")

        if isinstance(re, complex):
            self.imag = round(re.imag)
        elif isinstance(im, int):
            self.imag = im
        elif isinstance(im, float):
            self.imag = round(im)
        else:
            raise TypeError(f"{im} cannot be used for the imaginary part of a Gint instance")

    def __repr__(self) -> str:
        return f"Gint({self.real}, {self.imag})"

    def __str__(self) -> str:
        return str(complex(self))

    def __add__(self, other):
        """Implements the + operator: self + other

        Add this Gint to another Gint or integer.
        """
        if isinstance(other, int):
            return Gint(self.real + other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self

        Handle addition by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 + Gint(1, 2) ==> Gint(3, 2)
        """
        if isinstance(other, int):
            return Gint(other + self.real, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        if isinstance(other, int):
            return Gint(self.real + other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):
        """Implements the subtraction operator: self - other

        Subtract another Gint or integer from this Gint.
        """
        if isinstance(other, int):
            return Gint(self.real - other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self

        Handle subtraction by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 - Gint(1, 2) ==> Gint(1, -2)
        """
        if isinstance(other, int):
            return Gint(other - self.real, -self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        if isinstance(other, int):
            return Gint(self.real - other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other"""
        a = self.real
        b = self.imag
        if isinstance(other, Gint):
            c = other.real
            d = other.imag
        elif isinstance(other, int):
            c = other
            d = 0  # Easy way to handle the int case
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:  # might as well take advantage of this here
            return Gint(a * c, b * c)
        else:
            return Gint(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        """The reflected (swapped) operand for multiplication: other * self

        Handle multiplication by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 * Gint(1, 2) ==> Gint(2, 4)
        """
        if isinstance(other, int):
            return Gint(other * self.real, other * self.imag)
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
        a = self.real
        b = self.imag
        if isinstance(other, Gint):
            c = other.real
            d = other.imag
        elif isinstance(other, int):
            c = other
            d = 0  # Easy way to handle the int case
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:
            return Gint(a * c, b * c)
        else:
            return Gint(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int) and n >= 0:
            if n == 0:
                result = Gint()  # Return "1"
            else:
                for _ in range(n - 1):
                    result = result * self
        else:
            raise TypeError(f"The power, {n}, is not a positive integer.")
        return result

    def __complex__(self) -> complex:
        """Return the complex number that corresponds to this Gint."""
        return complex(self.real, self.imag)

    def __neg__(self):
        """Negate this Gint."""
        return Gint(-self.real, -self.imag)

    def __eq__(self, other) -> bool:
        """Return True if this Gint equals other."""
        if isinstance(other, Gint):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        """Return True if this Gint does NOT equal other."""
        if isinstance(other, Gint):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    def __truediv__(self, other):  # self / other
        """Divide self by other, exactly, and return the resulting complex number.

        Implements the / operator, and returns the exact, complex result
        of dividing this Gint by another Gint, int, float, or complex number.
        """
        if isinstance(other, (int, float, complex, Gint)):
            return complex(self) / complex(other)
        else:
            raise TypeError(f"{other} cannot divide a Gint")

    def __rtruediv__(self, other):  # other / self
        """Divide other by self, exactly, and return the resulting complex number.

        Implements the 'swapped' version of the / operator, and returns the exact,
        complex result of dividing other by this Gint.
        """
        if isinstance(other, (int, float, complex)):  # the Gint case is handled by __truediv__
            return complex(other) / complex(self)
        else:
            raise TypeError(f"{other} cannot be divided by a Gint")

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Gint, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Gint.
        """
        if isinstance(other, (int, float, complex, Gint)):
            return Gint(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Gint(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __mod__(self, other):
        """Implements the % operator.

        Returns the remainder of the result from mod_divmod
        """
        _, r = mod_divmod(self, other)
        return r

    def __hash__(self):
        """Allow this Gint to be hashed."""
        return hash((self.real, self.imag))

    # # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    # def divmod(self, other):  # A modified division theorem
    #     """A modified division theorem.
    #
    #     Let a = self & b = other, then this method computes q & r,
    #     such that a = b * q + r, where (1/2) * r.norm < b.norm.
    #     It returns q & r (i.e., the quotient and remainder).
    #     This is the Modified Division Theorem described in
    #     'The Gaussian Integers' by Keith Conrad
    #     """
    #     q = Gint(complex(self * other.conj) / other.norm)  # Gint rounds the complex result here
    #     r = self - other * q
    #     return q, r
    #
    # def gcd(self, other, verbose=False):
    #     """Return the greatest common divisor of self and other.
    #
    #     This function implements the Euclidean algorithm for Gaussian integers.
    #     """
    #     zero = Gint()
    #     if self * other == zero:
    #         raise ValueError(f"Both inputs must be non-zero: {self} and {other}")
    #     else:
    #         r1, r2 = self, other
    #         while r2 != zero:
    #             r0, r1 = r1, r2
    #             q, r2 = r0.divmod(r1)  # q is not used in the computation
    #             if verbose:
    #                 print(f"   {r0} = {r1} * {q} + {r2}")
    #     return r1

    @classmethod
    def eye(cls):
        """Return i = Gint(0, 1)"""
        return Gint(0, 1)

    @classmethod
    def units(cls):
        """Returns the list of four units, [1, -1, i, -i], as Gints."""
        return [Gint(1), -Gint(1), cls.eye(), -cls.eye()]

    @property
    def conj(self):
        """Return the conjugate of this Gaussian integer"""
        return Gint(self.real, - self.imag)

    @property
    def norm(self) -> int:
        """Return the norm of this Gaussian integer.

        NOTE: The norm here is the square of the usual absolute value.
        """
        n = self * self.conj
        return n.real

    def associates(self):
        """Return a list of this Gint's three associates"""
        us = Gint.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Gint is an associate of this Gint

        Otherwise, return False.
        """
        q = self // other
        if q:
            if q in Gint.units():
                return True
            else:
                return False
        else:
            return False

    # def unpack(self):
    #     """Return the two components of the Gint."""
    #     return self.real, self.imag


def isprime(n: int) -> bool:
    """Returns True if n is a positive, prime integer; otherwise, False is returned.
    The same function exists in SymPy."""
    if isinstance(n, int):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        root_n = int(sqrt(n)) + 1
        for val in range(3, root_n, 2):
            if n % val == 0:
                return False
        return True
    else:
        raise False


# See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
def mod_divmod(a, b):
    """A modified divmod algorithm for Gaussian integers.

    Returns q & r, such that a = b * q + r, where
    (1/2) * r.norm < b.norm. This is the Modified Division
    Theorem described in 'The Gaussian Integers' by Keith Conrad
    """
    q = Gint(complex(a * b.conj) / b.norm)  # Gint rounds the complex result here
    r = a - b * q
    return q, r


def gcd(a, b, verbose=False):
    """Return the greatest common divisor of self and other.

    This function implements the Euclidean algorithm for Gaussian integers.
    """
    zero = Gint()
    if a * b == zero:
        raise ValueError(f"Both inputs must be non-zero: {a} and {b}")
    else:
        r1, r2 = a, b
        while r2 != zero:
            r0, r1 = r1, r2
            q, r2 = mod_divmod(r0, r1)  # q is not used in the computation
            if verbose:
                print(f"   {r0} = {r1} * {q} + {r2}")
    return r1


def xgcd(alpha, beta):
    """The Extended Euclidean Algorithm for Gaussian Integers.

    Three values are returned: a, x, & y, such that
    the Greatest Common Divisor (gcd) of a & b can be
    written as gcd = a * x + b * y. x & y are called
    Bézout's coefficients.
    """
    if isinstance(alpha, Gint) and isinstance(beta, Gint):
        zero = Gint()
    else:
        raise ValueError(f"Inputs must be two Gints.")

    # NOTE: Many of the lines below perform two assigment operations
    a, b = alpha, beta
    x, next_x = 1, 0
    y, next_y = 0, 1
    while b != zero:
        q = a // b
        next_x, x = x - q * next_x, next_x
        next_y, y = y - q * next_y, next_y
        a, b = b, a % b
    return a, x, y
