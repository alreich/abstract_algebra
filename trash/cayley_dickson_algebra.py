

from numbers import Real, Complex


class Xi(Complex):
    """A class for creating Cayley-Dickson algebras"""

    def __init__(self, re: Complex = 0, im: Complex = 0):

        if isinstance(re, Complex):
            self.__real = re
        else:
            raise TypeError(f"{re} cannot be used for the real part")

        if isinstance(im, Complex):
            self.__imag = im
        else:
            raise TypeError(f"{im} cannot be used for the imaginary part")

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    def __repr__(self) -> str:
        return f"Xi({self.real}, {self.imag})"

    def __complex__(self) -> str:
        if isinstance(self, (int, float, complex)):
            return complex(self)
        elif isinstance(self, Complex):
            return f"({complex(self.real)} + {complex(self.imag)}i)"
        else:
            raise TypeError(f"complex() does not support {self}")

    def __bool__(self):
        return self != 0

    def __add__(self, other: Complex) -> Complex:
        return Xi(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        raise NotImplementedError

    def __neg__(self) -> Complex:
        return Xi(-self.real, -self.imag)

    def __pos__(self) -> Complex:
        return Xi(+self.real, +self.__imag)

    def __sub__(self, other: Complex) -> Complex:
        return Xi(self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other):
        return NotImplemented

    def __mul__(self, other: Complex) -> Complex:
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        # (a, b) * (c, d) = (a * c - b * d, a * d + b * c)
        return Xi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            numer = self
            denom = other
        elif isinstance(other, Complex):
            numer = self * other.conjugate()
            denom = other.norm()
        else:
            raise TypeError(f"Division by {other.__class__.__name__} not supported")
        return Xi(numer.real / denom, numer.imag / denom)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, complex)):
            print(other, self)
            return other / self
        else:
            raise TypeError(f"{other} cannot be divided by Xi")

    def __pow__(self, exponent):
        raise NotImplementedError

    def __rpow__(self, base):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        return (self.real == other.real) and (self.imag == other.imag)

    def conjugate(self) -> Complex:
        if isinstance(self, Real):
            return self
        elif isinstance(self, Complex):
            return Xi(self.real, -self.imag)
        else:
            raise TypeError(f"Cannot conjugate {self.__class__.__name__}")

    def norm(self):
        if isinstance(self, Real):
            return self * self
        elif isinstance(self, Complex):
            tmp = self * self.conjugate()
            tmp.real
        else:
            raise TypeError(f"Cannot compute norm of {self.__class__.__name__}")

    def inverse(self: Complex) -> Complex:
        norm = self.norm()
        conj = self.conjugate()
        return Xi(conj.real / norm, conj.imag / norm)
