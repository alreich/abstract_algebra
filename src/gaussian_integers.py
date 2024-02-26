"""A Gaussian Integer class, Zi, together with associated functionality.

In mathematics, the integers are denoted by Z and Gaussian integers are denoted by Z[i].
A Gaussian integer is a complex number whose real and imaginary parts are both integers.
In this module, a Gaussian integer is represented in the form, Zi(re, im), where re is
the real integer and im is the imaginary integer. The Zi class supports the arithmetic
of Gaussian integers using numeric-style operators: +, -, *, /, //, %, **, +=, -=, *=,
and /=, along with a modified version of divmod, called mod_divmod, and two functions
related to the Greatest Common Divisor: gcd and xgcd.

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

        Add this Zi to another Zi or integer.
        """
        if isinstance(other, int):
            return Zi(self.real + other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __radd__(self, other):
        """The reflected (swapped) operand for addition: other + self

        Handle addition by an integer, where this Zi is on the right side,
        and an integer, other, is on the left. e.g., 2 + Zi(1, 2) ==> Zi(3, 2)
        """
        if isinstance(other, int):
            return Zi(other + self.real, self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __iadd__(self, other):
        """Implements the += operation: self += other"""
        if isinstance(other, int):
            return Zi(self.real + other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __sub__(self, other):
        """Implements the subtraction operator: self - other

        Subtract another Zi or integer from this Zi.
        """
        if isinstance(other, int):
            return Zi(self.real - other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __rsub__(self, other):
        """The reflected (swapped) operand for subtraction: other - self

        Handle subtraction by an integer, where this Zi is on the right side,
        and an integer, other, is on the left. e.g., 2 - Zi(1, 2) ==> Zi(1, -2)
        """
        if isinstance(other, int):
            return Zi(other - self.real, -self.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __isub__(self, other):
        """Implements the -= operation: self -= other"""
        if isinstance(other, int):
            return Zi(self.real - other, self.imag)
        elif isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError(f"Addition by '{other}' not supported")

    def __mul__(self, other):  # self * other
        """Implements the multiplication operator: self * other"""
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
        """The reflected (swapped) operand for multiplication: other * self

        Handle multiplication by an integer, where this Zi is on the right side,
        and an integer, other, is on the left. e.g., 2 * Zi(1, 2) ==> Zi(2, 4)
        """
        if isinstance(other, int):
            return Zi(other * self.real, other * self.imag)
        else:
            raise TypeError(f"Multiplication by '{other}' not supported")

    def __imul__(self, other):
        """Implements the *= operation: self *= other"""
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

    def __truediv__(self, other) -> Qi:  # self / other
        """Divide self by other, exactly, and return the resulting Gaussian rational, Qi.

        Implements the / operator, and returns the exact, Gaussian rational result
        of dividing this Gaussian integer by another Gaussian integer or regular integer.
        """
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
        """Divide other by self, exactly, and return the resulting complex number.

        Implements the 'swapped' version of the / operator, and returns the exact,
        complex result of dividing other by this Gaussian integer. Other must be
        a Gaussian integer or a regular integer.
        """
        if isinstance(other, (int, float, complex)):  # the Zi case is handled by __truediv__
            return complex(other) / complex(self)
        else:
            raise TypeError(f"{other} cannot be divided by a Zi")

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

        Returns the remainder of the result from mod_divmod
        """
        _, r = mod_divmod(self, other)
        return r

    def __hash__(self):
        """Allow this Zi to be hashed."""
        return hash((self.real, self.imag))

    def __abs__(self) -> float:
        """Returns the square root of the norm."""
        return sqrt(self.norm)

    def __pos__(self):
        return +self

    def __rpow__(self):
        return NotImplemented

    @classmethod
    def eye(cls):
        """Return i = Zi(0, 1)"""
        return Zi(0, 1)

    @classmethod
    def units(cls):
        """Returns the list of four units, [1, -1, i, -i], as Zis."""
        return [Zi(1), -Zi(1), cls.eye(), -cls.eye()]

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
        """Convert this to a Gaussian rational."""
        return Qi(self.real, self.imag)

    def unpack(self):
        """Return the two components of the Zi."""
        return self.real, self.imag


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
def mod_divmod(a: Zi, b: Zi):
    """A modified divmod algorithm for Gaussian integers.

    Returns q & r, such that a = b * q + r, where
    (1/2) * r.norm < b.norm. This is the Modified Division
    Theorem described in 'The Gaussian Integers' by Keith Conrad
    """
    q = Zi(complex(a * b.conjugate) / b.norm)  # Zi rounds the complex result here
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
