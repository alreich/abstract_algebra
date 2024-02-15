

def divides(m, n):
    """Returns True if m divides n."""
    if (abs(m) <= abs(n)) and (n % m == 0):
        return True
    else:
        return False


class Gint():
    """Gaussian Integer Class"""

    def __init__(self, re=1, im=0):

        if not (isinstance(re, int) and isinstance(im, int)):
            raise ValueError(f"Both {re} and {im} must be Integers.")
        else:
            self.real = re
            self.imag = im

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
            d = 0
        else:
            raise ValueError(f"Multiplication by {other} not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        return Gint(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        a = self.real
        b = self.imag
        if isinstance(other, int):
            c = other
            d = 0
        else:
            raise ValueError(f"Multiplication by {other} not supported")
        # (a, b) * (c, d) = (a*c - b*d) + (a*d + b*c)
        return Gint(a * c - b * d, a * d + b * c)

    def __truediv__(self, other):
        """If other divides self, then self / other is returned,
        otherwise False is returned.
        """
        numer = self * other.conj
        denom = other.norm
        if divides(denom, numer.real) and divides(denom, numer.imag):
            return Gint(numer.real // denom, numer.imag // denom)
        else:
            return False

    def __complex__(self):
        return complex(self.real, self.imag)

    def __neg__(self):
        return Gint(-self.real, -self.imag)

    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)

    def __ne__(self, other):
        return (self.real != other.real) or (self.imag != other.imag)

    @property
    def conj(self):
        return Gint(self.real, - self.imag)

    @property
    def norm(self):
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

    def is_divided_by(self, other):
        """Return True if the other Gint divides this Gint,
        otherwise return False.
        """
        if isinstance(other, Gint):
            return other.divides(self)
        elif isinstance(other, int):
            if (self.real % other == 0) and (self.imag % other == 0):
                return Gint(self.real // other, self.imag // other)
            else:
                return False
        else:
            raise ValueError(f"{other} is not a valid input")

