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
            raise ValueError(f"{re} cannot be used for the real part of a Gint instance")

        if isinstance(re, complex):
            self.imag = round(re.imag)
        elif isinstance(im, int):
            self.imag = im
        elif isinstance(im, float):
            self.imag = round(im)
        else:
            raise ValueError(f"{im} cannot be used for the imaginary part of a Gint instance")

    def __repr__(self) -> str:
        return f"Gint({self.real}, {self.imag})"

    def __str__(self) -> str:
        return str(complex(self))

    def __add__(self, other):
        return Gint(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Gint(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
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

    def __rmul__(self, other):
        """Handle multiplication by an integer, where this Gint is on the right side,
        and an integer, other, is on the left. e.g., 2 * Gint(1, 2) ==> Gint(2, 4)
        """
        a = self.real
        b = self.imag
        if isinstance(other, int):
            return Gint(other * a, other * b)
        else:
            raise ValueError(f"Multiplication by '{other}' not supported")

    def __pow__(self, n: int, modulo=None):
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

    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other):
        return (self.real != other.real) or (self.imag != other.imag)

    def __truediv__(self, other):  # self / other
        """Return the exact, complex result of dividing this Gint by other"""
        return complex(self) / complex(other)

    def __floordiv__(self, other):  # self // other
        """Return the quotient, self / other, using the division theorem
        """
        if isinstance(other, int) or isinstance(other, float):
            q = Gint(complex(self) / other)
        else:
            q = Gint(complex(self * other.conj) / other.norm)
        return q

    def division_theorem(self, other):
        """Let a = self & b = other, then compute q & r, such that a = b * q + r,
        and return q & r (i.e., the quotient and remainder of a/b)
        """
        q = Gint(complex(self * other.conj) / other.norm)  # Gint rounds the complex result here
        r = self - other * q
        return q, r

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

    # def __truediv__(self, other):
    #     """If other divides self, then self / other is returned,
    #     otherwise False is returned.
    #     """
    #     if isinstance(other, int):
    #         oth = Gint(other, 0)
    #     else:
    #         oth = other
    #     numer = self * oth.conj
    #     denom = oth.norm
    #     if my.divides(denom, numer.real) and my.divides(denom, numer.imag):
    #         return Gint(numer.real // denom, numer.imag // denom)
    #     else:
    #         return False

    # def divides(self, other):
    #     """Return True if this Gint divides the other Gint,
    #     otherwise return False.
    #     """
    #     a = self.norm
    #     b = other.norm
    #     if b % a == 0:
    #         return True
    #     else:
    #         return False

    # def divided_by(self, other):
    #     """Return True if the other Gint or int divides this Gint,
    #     otherwise return False.
    #     """
    #     if isinstance(other, Gint):
    #         return other.divides(self)
    #     elif isinstance(other, int):
    #         if (self.real % other == 0) and (self.imag % other == 0):
    #             # return Gint(self.real // other, self.imag // other)
    #             return True
    #         else:
    #             return False
    #     else:
    #         raise ValueError(f"{other} is not a valid input")
