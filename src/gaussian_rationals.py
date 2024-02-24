"""A Gaussian Rational class

blah, blah, blah, blah...
"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "0.1.0"


from gaussian_integers import Gint
from fractions import Fraction


class Grat:
    """Gaussian Rational Number Class"""

    def __init__(self, re=Fraction(0, 1), im=Fraction(0, 1)):
        # re & im must be Fractions
        if isinstance(re, Fraction) and isinstance(im, Fraction):
            self.real = re
            self.imag = im
        elif isinstance(re, str) and isinstance(im, str):
            self.real = Fraction(re)
            self.imag = Fraction(im)
        elif isinstance(re, int) and isinstance(im, int):
            self.real = Fraction(re, 1)
            self.imag = Fraction(im, 1)
        elif isinstance(re, Gint) and isinstance(im, Gint):
            # re & im are interpreted as the numerator & denominator, resp.
            nrm = im.norm
            prd = re * im.conj
            self.real = Fraction(prd.real, nrm)
            self.imag = Fraction(prd.imag, nrm)
        else:
            raise TypeError("{re} & {im} are not a supported type")

    def __repr__(self):
        return f"Grat({repr(self.real)}, {repr(self.imag)})"

    def __str__(self):
        return f"({self.real}, {self.imag}j)"

    def __add__(self, other):
        return Grat(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Grat(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        return Grat(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int) and n >= 0:
            if n == 0:
                result = Gint(1)  # Return "1"
            else:
                for _ in range(n - 1):
                    result = result * self
        else:
            raise TypeError(f"The power, {n}, is not a positive integer.")
        return result

    def __truediv__(self, other):
        return self * other.inv

    def __neg__(self):
        return Grat(-self.real, -self.imag)

    def __complex__(self) -> complex:
        re = self.real.numerator / self.real.denominator
        im = self.imag.numerator / self.imag.denominator
        return complex(re, im)

    def __eq__(self, other) -> bool:
        """Return True if this Grat equals other."""
        if isinstance(other, Grat):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        """Return True if this Grat does NOT equal other."""
        if isinstance(other, Grat):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    def __hash__(self):
        return hash((self.real, self.imag))

    @property
    def conj(self):
        return Grat(self.real, -self.imag)

    @property
    def norm(self) -> Fraction:
        tmp = self * self.conj
        return tmp.real

    @property
    def inv(self):
        norm = self.norm
        conj = self.conj
        return Grat(conj.real / norm, conj.imag / norm)

