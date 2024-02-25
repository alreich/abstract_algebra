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
        return Qi(self.real + other.real, self.imag + other.imag)

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

    def __radd__(self):
        return NotImplemented

    def __rmul__(self):
        return NotImplemented

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
