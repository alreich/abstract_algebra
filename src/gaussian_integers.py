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

# from my_math import divides
import my_math as my


class Gint():
    """Gaussian Integer Class"""

    def __init__(self, re=1, im=0):

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

    def __repr__(self):
        return f"Gint({self.real}, {self.imag})"

    def __str__(self):
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

    def __truediv__(self, other):
        """If other divides self, then self / other is returned,
        otherwise False is returned.
        """
        if isinstance(other, int):
            oth = Gint(other, 0)
        else:
            oth = other
        numer = self * oth.conj
        denom = oth.norm
        if my.divides(denom, numer.real) and my.divides(denom, numer.imag):
            return Gint(numer.real // denom, numer.imag // denom)
        else:
            return False

    def __pow__(self, n, modulo=None):
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

    def __complex__(self):
        return complex(self.real, self.imag)

    def __neg__(self):
        return Gint(-self.real, -self.imag)

    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other):
        return (self.real != other.real) or (self.imag != other.imag)

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
    def norm(self):
        """Returns the norm of this Gaussian integer.
        NOTE: The norm here is the square of the usual absolute value."""
        n = self * self.conj
        return n.real

    def divides(self, other):
        """Return True if this Gint divides the other Gint,
        otherwise return False.
        """
        a = self.norm
        b = other.norm
        if b % a == 0:
            return True
        else:
            return False

    def divided_by(self, other):
        """Return True if the other Gint or int divides this Gint,
        otherwise return False.
        """
        if isinstance(other, Gint):
            return other.divides(self)
        elif isinstance(other, int):
            if (self.real % other == 0) and (self.imag % other == 0):
                # return Gint(self.real // other, self.imag // other)
                return True
            else:
                return False
        else:
            raise ValueError(f"{other} is not a valid input")

    def division(self, b):
        """Compute q & r, such that self = bq + r
        """
        q = Gint(complex(self * b.conj) / b.norm)  # Gint rounds the complex parts here
        r = self - b * q
        return q, r

    def associates(self):
        """Return the list of this Gint's associates"""
        us = Gint.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        """Return True if the other Gint is an associate of this Gint,
        otherwise return False.
        """
        q = self / other
        if q:
            if q in Gint.units():
                return True
            else:
                return False
        else:
            return False