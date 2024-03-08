"""A Gaussian Integer class, Zi, together with associated functionality.

A Gaussian integer is a complex number whose real and imaginary parts are both integers.
In mathematics, the integers are denoted by Z and Gaussian integers are denoted by Z[i].
In this module, a Gaussian integer is represented in the form, Zi(re, im), where re is
the real integer and im is the imaginary integer. The Zi class supports the arithmetic
of Gaussian integers using numeric-style operators: +, -, *, /, //, %, **, +=, -=, *=,
and /=, along with a modified version of divmod, modified_divmod, and two functions
related to the Greatest Common Divisor: gcd and xgcd.

A companion module, gaussian_rationals, is also required by this module to provide,
among other things for example, a way to exactly divide any two Gaussian integers.

Example:
  > from gaussian_integers import Zi, mod_divmod, gcd, xgcd
  >
  > alpha = Zi(11, 3)
  > beta = Zi(1, 8)
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
from fractions import Fraction
from numbers import Complex
from gaussian_rationals import Qi


class Zi(Complex):
    """Gaussian Integer Class with arithmetic and related functionality.

    A Gaussian integer, Zi, has two integer input values, re & im.
    Floats and complex numbers can be entered, but they will be rounded to the
    nearest integers. If a complex number is provided for re, then the value of
    im will be ignored, and the complex number's components, real & imag, will be
    rounded to nearest integers and used as inputs for re & im, respectively.
    """

    def __init__(self, re: (int, float, complex) = 0, im: (int, float) = 0):
        """Instantiate a Gaussian integer, Zi(re=0, im=0)."""

        if isinstance(re, int):
            self.__real = re
        elif isinstance(re, float):
            self.__real = round(re)
        elif isinstance(re, complex):
            self.__real = round(re.real)
        else:
            raise TypeError(f"{re} cannot be used for the real part of a Zi instance")

        if isinstance(re, complex):
            self.__imag = round(re.imag)
        elif isinstance(im, int):
            self.__imag = im
        elif isinstance(im, float):
            self.__imag = round(im)
        else:
            raise TypeError(f"{im} cannot be used for the imaginary part of a Zi instance")

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    def __repr__(self) -> str:
        return f"Zi({self.real}, {self.imag})"

    def __str__(self) -> str:
        return str(complex(self))

    def __add__(self, other):
        """Implements the + operator: self + other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return self + Zi(other)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return Zi(other) + self
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __iadd__(self, other):
        """Implements the += operation: self += other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return self + Zi(other)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):
        """Implements the subtraction operator: self - other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return self - Zi(other)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Subtraction by '{other}' not supported")

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return Zi(other) - self
        else:
            raise TypeError(f"Subtraction by '{other}' not supported")

    def __isub__(self, other):
        """Implements the -= operation: self -= other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            return self - Zi(other)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        a = self.real
        b = self.imag
        if isinstance(other, Zi):
            c = other.real
            d = other.imag
        elif isinstance(other, complex):
            c = round(other.real)
            d = round(other.imag)
        elif isinstance(other, float):
            c = round(other)
            d = 0
        elif isinstance(other, int):
            c = other
            d = 0
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a * c - b * d) + (a * d + b * c)
        if d == 0:
            return Zi(a * c, b * c)
        else:
            return Zi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        """The reflected (swapped) operand for multiplication: other * self

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        if isinstance(other, int):
            return Zi(other * self.real, other * self.imag)
        elif isinstance(other, float):
            oth = round(other)
            return Zi(oth * self.real, oth * self.imag)
        elif isinstance(other, complex):
            return Zi(other) * self
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")

    def __imul__(self, other):
        """Implements the *= operation: self *= other

        other can be a Zi, int, float, or complex. Floats & complex will be rounded.
        """
        a = self.real
        b = self.imag
        if isinstance(other, Zi):
            c = other.real
            d = other.imag
        elif isinstance(other, complex):
            c = round(other.real)
            d = round(other.imag)
        elif isinstance(other, float):
            c = round(other)
            d = 0
        elif isinstance(other, int):
            c = other
            d = 0
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:
            return Zi(a * c, b * c)
        else:
            return Zi(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):
        """Implements the ** operator: self ** n.

        If n == 0, then Zi(1, 0) is returned. If n < 0, then the Gaussian
        rational, Qi, for 1 / self**n is returned. Otherwise, self ** n is returned.
        """
        result = self
        if isinstance(n, int):
            if n == 0:
                result = Zi(1)  # Return "1"
            elif n > 0:
                for _ in range(n - 1):
                    result = result * self
            else:  # n < 0
                return 1 / (self ** abs(n))
        else:
            raise TypeError(f"The power, {n}, must be an integer.")
        return result

    def __complex__(self) -> complex:
        """Return the complex number that corresponds to this Zi."""
        return complex(self.real, self.imag)

    def __neg__(self):
        """Negate this Zi."""
        return Zi(-self.real, -self.imag)

    def __eq__(self, other) -> bool:
        """Return True if this Zi equals other."""
        if isinstance(other, Zi):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        """Return True if this Zi does NOT equal other."""
        if isinstance(other, Zi):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    # def __truediv__(self, other) -> Qi:  # self / other
    #     """Divide self by other, exactly, and return the resulting Gaussian rational, Qi.
    #
    #     Implements the / operator, and returns the exact, Gaussian rational result
    #     of dividing this Gaussian integer by another Gaussian integer or regular integer.
    #     """
    #     if isinstance(other, Zi):
    #         denom = other.norm
    #         numer = self * other.conjugate
    #     elif isinstance(other, int):
    #         denom = other
    #         numer = self
    #     else:
    #         raise TypeError(f"{other} cannot divide a Gaussian integer")
    #     return Qi(Fraction(numer.real, denom), Fraction(numer.imag, denom))

    def __truediv__(self, other) -> Qi:  # self / other
        """Divide self by other, exactly, and return the resulting Gaussian rational, Qi.

        Implements the / operator, and returns the exact, Gaussian rational result
        of dividing this Gaussian integer by another Gaussian integer, or an int,
        float, or complex. Floats & complexes will be rounded.
        """
        if isinstance(other, (int, float, complex)):
            oth = Zi(other)
        elif isinstance(other, Zi):
            oth = other
        else:
            raise TypeError(f"Cannot divide a Gaussian integer by {other}")
        numer = self * oth.conjugate
        denom = oth.norm
        return Qi(Fraction(numer.real, denom), Fraction(numer.imag, denom))

    def __rtruediv__(self, other):  # other / self
        """Divide other by self, exactly, and return the resulting Gaussian rational, Qi.

        Implements the 'swapped' version of the / operator, and returns the exact,
        Gaussian rational result of dividing other by this Gaussian integer. Other
        must be a Gaussian integer or an int, float, or complex. Floats & complexes
        will be rounded.
        """
        if isinstance(other, (int, float, complex)):  # the Zi case is handled by __truediv__
            oth = Zi(other)
            numer = oth * self.conjugate
            denom = self.norm
            return Qi(Fraction(numer.real, denom), Fraction(numer.imag, denom))
        else:
            raise TypeError(f"{other} cannot be divided by a Gaussian integer")

    def __floordiv__(self, other):  # self // other
        """Implements the // operator using 'round', instead of 'floor'.

        Returns the closest integer approximation to the quotient, self / other,
        as a Zi, by rounding the real and imag parts after division, not flooring.
        'other' can be an int, float, complex, or Zi.
        """
        if isinstance(other, (int, float, complex, Zi)):
            return Zi(complex(self) / complex(other))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, (int, float, complex)):
            return Zi(complex(other) / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __mod__(self, other):
        """Implements the % operator.

        Returns the remainder of the result from modified_divmod
        """
        _, r = Zi.modified_divmod(self, other)
        return r

    def __hash__(self):
        """Allow this Zi to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self, base):
        return NotImplemented

    @staticmethod
    def eye():
        """Return i = Zi(0, 1)"""
        return Zi(0, 1)

    @staticmethod
    def units():
        """Returns the list of four units, [1, -1, i, -i], as Zis."""
        return [Zi(1), -Zi(1), Zi.eye(), -Zi.eye()]

    @property
    def conjugate(self):
        """Return the conjugate of this Gaussian integer"""
        return Zi(self.real, - self.imag)

    @property
    def norm(self) -> int:
        """Return the norm of this Gaussian integer.

        NOTE: The norm here is the square of the usual absolute value.
        """
        n = self * self.conjugate
        return n.real

    def associates(self):
        """Return a list of this Zi's three associates"""
        us = Zi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Zi is an associate of this Zi

        Otherwise, return False.
        """
        q = self // other
        if q:
            if q in Zi.units():
                return True
            else:
                return False
        else:
            return False

    def to_gaussian_rational(self):
        """Convert this Gaussian integer to an equivalent Gaussian rational."""
        return Qi(self.real, self.imag)

    # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    @staticmethod
    def modified_divmod(a, b):
        """The divmod algorithm, modified for Gaussian integers.

        Returns q & r, such that a = b * q + r, where
        (1/2) * r.norm < b.norm. This is the Modified Division
        Theorem described in 'The Gaussian Integers' by Keith Conrad
        """
        q = Zi(complex(a * b.conjugate) / b.norm)  # Zi rounds the complex result here
        r = a - b * q
        return q, r

    @staticmethod
    def gcd(a, b, verbose=False):
        """A gcd algorithm for Gaussian integers.
        Returns the greatest common divisor of a & b.

        This function implements the Euclidean algorithm for Gaussian integers.
        """
        zero = Zi()
        if a * b == zero:
            raise ValueError(f"Both inputs must be non-zero: {a} and {b}")
        else:
            r1, r2 = a, b
            while r2 != zero:
                r0, r1 = r1, r2
                q, r2 = Zi.modified_divmod(r0, r1)  # q only used in call to print, below
                if verbose:
                    print(f"   {r0} = {r1} * {q} + {r2}")
        return r1

    @staticmethod
    def xgcd(alpha, beta):
        """The Extended Euclidean Algorithm for Gaussian Integers.

        Three values are returned: a, x, & y, such that
        the Greatest Common Divisor (gcd) of a & b can be
        written as gcd = a * x + b * y. x & y are called
        Bézout's coefficients.
        """
        if isinstance(alpha, Zi) and isinstance(beta, Zi):
            zero = Zi()
        else:
            raise ValueError(f"Inputs must be two Zis.")

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

    @staticmethod
    def is_gaussian_prime(x) -> bool:
        """Return True if x is a Gaussian prime.  Otherwise, return False.
        x can be an integer or a Gaussian integer.

        See https://mathworld.wolfram.com/GaussianPrime.html
        """
        re = im = norm = None  # So PyCharm won't complain about using variables before assigning them

        if isinstance(x, Zi):
            re = abs(x.real)
            im = abs(x.imag)
            norm = x.norm
        elif isinstance(x, int):
            re = abs(x)
            im = 0
            norm = re * re

        if (re * im != 0) and isprime(norm):
            return True

        elif re == 0:
            if isprime(im) and (im % 4 == 3):
                return True
            else:
                return False

        elif im == 0:
            if isprime(re) and (re % 4 == 3):
                return True
            else:
                return False

        else:
            return False


def isprime(n: int) -> bool:
    """Returns True if n is a positive, prime integer; otherwise, False is returned.
    FYI, the same function exists in SymPy."""
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

