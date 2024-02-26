

from numbers import Complex


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

    def __repr__(self):
        return f"Xi({self.real}, {self.imag})"

    def __complex__(self):
            return NotImplemented

    def __bool__(self):
        return self != 0

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    def __add__(self, other):
        return Xi(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        raise NotImplementedError

    def __neg__(self):
        return Xi(-self.real, -self.imag)

    def __pos__(self):
        return Xi(+self.real, +self.__imag)

    def __sub__(self, other):
        return Xi(self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other):
        return NotImplemented

    def __mul__(self, other):
        a = self.real
        b = self.imag
        c = other.real
        d = other.imag
        # (a, b) * (c, d) = (a * c - b * d, a * d + b * c)
        return Xi(a * c - b * d, a * d + b * c)

    def __rmul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __rtruediv__(self, other):
        raise NotImplementedError

    def __pow__(self, exponent):
        raise NotImplementedError

    def __rpow__(self, base):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError

    def conjugate(self):
        return Xi(self.real, -self.imag)

    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)
