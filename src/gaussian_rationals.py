"""A Gaussian Rational class

blah, blah, blah, blah...
"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "0.1.0"

from math import sqrt
from numbers import Complex
from fractions import Fraction


class Qi(Complex):
    """Gaussian Rational Number Class"""

    def __init__(self, re=Fraction(0, 1), im=Fraction(0, 1)):
        if isinstance(re, Fraction) and isinstance(im, Fraction):
            self.__real = re
            self.__imag = im
        elif isinstance(re, str) and isinstance(im, str):
            self.__real = Fraction(re)
            self.__imag = Fraction(im)
        elif isinstance(re, int) and isinstance(im, int):
            self.__real = Fraction(re, 1)
            self.__imag = Fraction(im, 1)
        else:
            raise TypeError("{re} & {im} are not a supported type")

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    def __repr__(self):
        return f"Qi({repr(str(self.real))}, {repr(str(self.imag))})"

    def __str__(self):
        if self.imag < 0:
            return f"({self.real}{self.imag}j)"
        else:
            return f"({self.real}+{self.imag}j)"

    def __add__(self, other):
        if isinstance(other, Qi):
            return Qi(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, int):
            return Qi(self.real + other, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):
        if isinstance(other, int):
            return Qi(other + self.real, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):
        return Qi(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        return Qi(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int) and n >= 0:
            if n == 0:
                result = Qi(Fraction(1, 1), Fraction(0, 1))  # Return "1"
            else:
                for _ in range(n - 1):
                    result = result * self
        else:
            raise TypeError(f"The power, {n}, is not a positive integer.")
        return result

    def __truediv__(self, other):
        """Returns self/other as a Gaussian rational, Qi"""
        return self * other.inverse

    def __neg__(self):
        return Qi(-self.real, -self.imag)

    def __complex__(self) -> complex:
        # re = self.real.numerator / self.real.denominator
        # im = self.imag.numerator / self.imag.denominator
        return complex(float(self.real), float(self.imag))

    def __eq__(self, other) -> bool:
        """Return True if this Qi equals other."""
        if isinstance(other, Qi):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        """Return True if this Qi does NOT equal other."""
        if isinstance(other, Qi):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    def __hash__(self):
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        return sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rsub__(self, other):
        if isinstance(other, int):
            return Qi(other - self.real, -self.imag)
        else:
            raise TypeError(f"Subtraction by '{other}' not supported")

    def __rmul__(self, other):
        if isinstance(other, int):
            return Qi(other * self.real, other * self.imag)
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")

    def __rpow__(self):
        return NotImplemented

    def __rtruediv__(self):
        return NotImplemented

    @property
    def conjugate(self):
        return Qi(self.real, -self.imag)

    @property
    def norm(self) -> Fraction:
        tmp = self * self.conjugate
        return tmp.real

    @property
    def inverse(self):
        norm = self.norm
        conj = self.conjugate
        return Qi(conj.real / norm, conj.imag / norm)


def parse_printed_form(x):
    """Parse the printed form (string) of a Gaussian rational
    and return the corresponding Gaussian rational (Qi).

    Example:
    parse_printed_form('(2/3-1/7j)') -> Qi('2/3', '-1/7')
    """
    w = x[1:-2]  # Remove leading '(' and trailing 'j)'

    if w[0] == '-' or w[0] == '+':
        sign = w[0]  # Leading sign
        y = w[1:]
    else:
        sign = ''  # No leading sign
        y = w

    if '+' in y:
        re, im = y.split('+')
        return Qi(sign + re, im)
    elif '-' in y:
        re, im = y.split('-')
        return Qi(sign + re, '-' + im)
    else:
        raise ValueError(f"Can't parse {s}")

# s1 = "(1/2+3/5j)"
# s2 = "(1/2-3/5j)"
# s3 = "(-1/2+3/5j)"
# s4 = "(-1/2-3/5j)"
# s5 = "(+1/2+3/5j)"
# s6 = "(+1/2-3/5j)"
#
# test_strings = [s1, s2, s3, s4, s5, s6]
#
# for ts in test_strings:
#     print(f"{ts} -> {parse_printed_form(ts)}")
