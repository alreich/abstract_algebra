"""
@summary:  Gaussian Integer class
@author:   Alfred J. Reich, Ph.D.
@contact:  al.reich@gmail.com
@copyright: Copyright (C) 2024 Alfred J. Reich, Ph.D.
@license:  MIT
@requires: Python 3
@since:    2024.02
@version:  0.0.1
"""

from typing import TypeVar

IFC = TypeVar('IFC', int, float, complex)
IF = TypeVar('IF',  int, float)


class Gint:
    """Gaussian Integer Class"""

    def __init__(self, re: IFC = 1, im: IF = 0):  # See TypeVars above

        """The real and imaginary parts of a Gaussian integer must be integers.
        If anything other than two integers is entered, it/they will be rounded
        to the nearest integer(s)."""

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

    def __add__(self, other):  # self + other
        """Add this Gint to (an)other Gint.
        """
        if isinstance(other, int):
            return Gint(self.real + other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):  # other + self
        """Handle addition by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 + Gint(1, 2) ==> Gint(3, 2)
        """
        if isinstance(other, int):
            return Gint(other + self.real, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):  # self - other
        """Subtract (an)other Gint from this Gint.
        """
        # return Gint(self.real - other.real, self.imag - other.imag)
        if isinstance(other, int):
            return Gint(self.real - other, self.imag)
        elif isinstance(other, Gint):
            return Gint(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __rsub__(self, other):  # other - self
        """Handle subtraction by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 - Gint(1, 2) ==> Gint(1, -2)
        """
        if isinstance(other, int):
            return Gint(other - self.real, -self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __mul__(self, other):  # self * other
        """Multiple this Gint by (an)other Gint or integer.
        """
        a = self.real
        b = self.imag
        if isinstance(other, Gint):
            c = other.real
            d = other.imag
        elif isinstance(other, int):
            c = other
            d = 0  # Easy way to handle the int case
        else:
            raise ValueError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:  # might as well take advantage of this here
            return Gint(a * c, b * c)
        else:
            return Gint(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        """Handle multiplication by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 * Gint(1, 2) ==> Gint(2, 4)
        """
        if isinstance(other, int):
            return Gint(other * self.real, other * self.imag)
        else:
            raise ValueError(f"Multiplication by '{other}' not supported")

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int) and n >= 0:
            if n == 0:
                result = Gint()  # Return "1"
            else:
                for _ in range(n - 1):
                    result = result * self
        else:
            raise ValueError(f"The power, {n}, is not a positive integer.")
        return result

    def __complex__(self) -> complex:
        return complex(self.real, self.imag)

    def __neg__(self):
        return Gint(-self.real, -self.imag)

    def __eq__(self, other) -> bool:
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other) -> bool:
        return (self.real != other.real) or (self.imag != other.imag)

    def __truediv__(self, other):  # self / other
        """Implements the / operator, and returns the exact, complex result
        of dividing this Gint by (an)other Gint or int or float or complex.
        """
        return complex(self) / complex(other)

    def __rtruediv__(self, other):  # other / self
        """Implements the / operator, and returns the exact, complex result
        of dividing other by this Gint.
        """
        if isinstance(other, complex):
            return other / complex(self)
        elif isinstance(other, float) or isinstance(other, int):
            return complex(other) / complex(self)
        else:
            raise TypeError(f"{other} cannot be divided by a Gint")

    def __floordiv__(self, other):  # self // other
        """Implements the // operator, and returns the closest integer approximation
        to the quotient, self/other, as a Gint, by ROUNDING the real and imag parts
        after division, NOT flooring. 'other' can be an int, float, complex, or Gint.
        """
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return Gint(complex(self) / other)
        # elif isinstance(other, complex):
        #     other_conj = other.conjugate()
        #     other_norm = other * other_conj
        #     q = Gint((complex(self) * other_conj) / other_norm)
        elif isinstance(other, Gint):
            return Gint(complex(self * other.conj) / other.norm)
        else:
            raise TypeError(f"{other} is not a supported type.")

    def __rfloordiv__(self, other):  # other // self
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return Gint(other / complex(self))
        else:
            raise TypeError(f"{other} is not a supported type.")

    # See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
    def divmod(self, other):  # A modified division theorem
        """Let a = self & b = other, then this method computes q & r,
        such that a = b * q + r, where (1/2) * r.norm < b.norm.
        It returns q & r (i.e., the quotient and remainder).
        This is the Modified Division Theorem described in
        'The Gaussian Integers' by Keith Conrad
        """
        q = Gint(complex(self * other.conj) / other.norm)  # Gint rounds the complex result here
        r = self - other * q
        return q, r

    def __mod__(self, other):
        """Implements the % operator, and returns only the remainder
        portion of the result from self.divmod(other)
        """
        _, r = self.divmod(other)
        return r

    @classmethod
    def eye(cls):
        """Returns i = Gint(0, 1)"""
        return Gint(0, 1)

    @classmethod
    def units(cls):
        """Returns the list of units, [1, -1, i, -i]"""
        return [Gint(), -Gint(), cls.eye(), -cls.eye()]

    @property
    def conj(self):
        """Returns the conjugate of this Gaussian integer"""
        return Gint(self.real, - self.imag)

    @property
    def norm(self) -> int:
        """Returns the norm of this Gaussian integer.
        NOTE: The norm here is the square of the usual absolute value."""
        n = self * self.conj
        return n.real

    def associates(self):
        """Return the list of this Gint's associates"""
        us = Gint.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Gint is an associate of this Gint,
        otherwise return False.
        """
        q = self // other
        if q:
            if q in Gint.units():
                return True
            else:
                return False
        else:
            return False

