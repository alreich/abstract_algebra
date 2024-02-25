"""Classes for Gaussian Integers and Gaussian Rationals

blah, blah, blah, blah...
"""

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "0.1.0"

from my_math import isprime
from numbers import Complex
from fractions import Fraction


class Qi(Complex):
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
        return self * other.inv

    def __neg__(self):
        return Qi(-self.real, -self.imag)

    def __complex__(self) -> complex:
        re = self.real.numerator / self.real.denominator
        im = self.imag.numerator / self.imag.denominator
        return complex(re, im)

    def __eq__(self, other) -> bool:
        if isinstance(other, Qi):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Qi):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    def __hash__(self):
        return hash((self.real, self.imag))

    def conjugate(self):
        return Qi(self.real, -self.imag)

    def norm(self) -> Fraction:
        tmp = self * self.conjugate()
        return tmp.real

    def inv(self):
        norm = self.norm
        conj = self.conjugate()
        return Qi(conj.real / norm, conj.imag / norm)

    def __abs__(self):
        return NotImplemented

    def __pos__(self):
        return NotImplemented

    def __radd__(self):
        return NotImplemented

    def __rmul__(self):
        return NotImplemented

    def __rpow__(self):
        return NotImplemented

    def __rtruediv__(self):
        return NotImplemented


class Zi(Complex):

    def __init__(self, re: (int, float, complex) = 0, im: (int, float) = 0):

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
        if isinstance(other, int):
            return Zi(self.real + other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):
        if isinstance(other, int):
            return Zi(other + self.real, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __iadd__(self, other):
        if isinstance(other, int):
            return Zi(self.real + other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):
        if isinstance(other, int):
            return Zi(self.real - other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __rsub__(self, other):
        if isinstance(other, int):
            return Zi(other - self.real, -self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __isub__(self, other):
        if isinstance(other, int):
            return Zi(self.real - other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __mul__(self, other):  # self * other
        a = self.real
        b = self.imag
        if isinstance(other, Zi):
            c = other.real
            d = other.imag
        elif isinstance(other, int):
            c = other
            d = 0  # Easy way to handle the int case
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:  # might as well take advantage of this here
            return Zi(a * c, b * c)
        else:
            return Zi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):  # other * self
        if isinstance(other, int):
            return Zi(other * self.real, other * self.imag)
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")

    def __imul__(self, other):
        a = self.real
        b = self.imag
        if isinstance(other, Zi):
            c = other.real
            d = other.imag
        elif isinstance(other, int):
            c = other
            d = 0  # Easy way to handle the int case
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        if d == 0:
            return Zi(a * c, b * c)
        else:
            return Zi(a * c - b * d, a * d + b * c)

    def __pow__(self, n: int, modulo=None):  # self ** n
        result = self
        if isinstance(n, int) and n >= 0:
            if n == 0:
                result = Zi(1)  # Return "1"
            else:
                for _ in range(n - 1):
                    result = result * self
        else:
            raise TypeError(f"The power, {n}, is not a positive integer.")
        return result

    def __complex__(self) -> complex:
        return complex(self.real, self.imag)

    def __neg__(self):
        return Zi(-self.real, -self.imag)

    def __eq__(self, other) -> bool:
        if isinstance(other, Zi):
            return (self.real == other.real) and (self.imag == other.imag)
        else:
            return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Zi):
            return (self.real != other.real) or (self.imag != other.imag)
        else:
            return True

    def __truediv__(self, other) -> Qi:  # self / other
        if isinstance(other, Zi):
            denom = other.norm
            numer = self * other.conjugate
        elif isinstance(other, int):
            denom = other
            numer = self
        else:
            raise TypeError(f"{other} cannot divide a Gaussian integer")
        return Qi(Fraction(numer.real, denom), Fraction(numer.imag, denom))

    # TODO: Finish implementing this
    def __rtruediv__(self, other):  # other / self
        if isinstance(other, (int, float, complex)):  # the Zi case is handled by __truediv__
            return complex(other) / complex(self)
        else:
            raise TypeError(f"{other} cannot be divided by a Zi")

    def __floordiv__(self, other):  # self // other
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
        _, r = mod_divmod(self, other)
        return r

    def __hash__(self):
        return hash((self.real, self.imag))

    def __abs__(self):
        return NotImplemented

    def __pos__(self):
        return NotImplemented

    def __rpow__(self):
        return NotImplemented

    @classmethod
    def eye(cls):
        return Zi(0, 1)

    @classmethod
    def units(cls):
        return [Zi(1), -Zi(1), cls.eye(), -cls.eye()]

    @property
    def conjugate(self):
        return Zi(self.real, - self.imag)

    @property
    def norm(self) -> int:
        n = self * self.conjugate
        return n.real

    def associates(self):
        us = Zi.units()
        return list(map(lambda u: u * self, us[1:]))  # skip multiplying by 1

    def is_associate(self, other):
        q = self // other
        if q:
            if q in Zi.units():
                return True
            else:
                return False
        else:
            return False


# See https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf
def mod_divmod(a: Zi, b: Zi):
    """A modified divmod algorithm for Gaussian integers.

    Returns q & r, such that a = b * q + r, where
    (1/2) * r.norm < b.norm. This is the Modified Division
    Theorem described in 'The Gaussian Integers' by Keith Conrad
    """
    q = Zi(complex(a * b.conjugate()) / b.norm)  # Zi rounds the complex result here
    r = a - b * q
    return q, r


def gcd(a: Zi, b: Zi, verbose=False) -> Zi:
    """Return the greatest common divisor of self and other.

    This function implements the Euclidean algorithm for Gaussian integers.
    """
    zero = Zi()
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


def xgcd(alpha: Zi, beta: Zi):
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


def is_gaussian_prime(x: (int, Zi)) -> bool:
    """Return True if x is a Gaussian prime.  Otherwise, return False.

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
