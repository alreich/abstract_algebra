"""
@author: Alfred J. Reich

"""

from finite_algebras import Field


class AbstractComplexNumber:

    def __init__(self, a, b, algebra):
        self.__real = a
        self.__imag = b
        self.__alg = algebra

    def __repr__(self):
        return f"({repr(self.__real)}, {repr(self.__imag)})"

    @property
    def real(self):
        return self.__real

    @property
    def imag(self):
        return self.__imag

    @property
    def algebra(self):
        return self.__alg

    def unpack(self):
        return self.real, self.imag

    def arithmetic_inputs_ok(self, other):
        if isinstance(other, AbstractComplexNumber):
            if self.algebra == other.algebra:
                return True
            else:
                raise ValueError(f"{self.algebra.name} != {other.algebra.name}")
        else:
            raise ValueError(f"{other} is not an AbstractComplexNumber")

    def __add__(self, other):
        if self.arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.add(a, c)
            v = alg.add(b, d)
            return AbstractComplexNumber(u, v, alg)

    def __sub__(self, other):
        if self.arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.sub(a, c)
            v = alg.sub(b, d)
            return AbstractComplexNumber(u, v, alg)

    def __neg__(self):
        alg = self.algebra
        a, b = self.unpack()
        return AbstractComplexNumber(alg.inv(a), alg.inv(b), alg)

    def __mul__(self, other):
        if self.arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.sub(alg.mult(a, c), alg.mult(b, d))
            v = alg.add(alg.mult(a, d), alg.mult(b, c))
            return AbstractComplexNumber(u, v, alg)

    @property
    def __key(self):
        return tuple([self.real, self.imag])

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        if isinstance(other, AbstractComplexNumber):
            return self.__key == other.__key and self.__alg == other.__alg
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def scalar_mult(self, scalar, left=True):
        alg = self.algebra
        a, b = self.unpack()
        if left:
            u = alg.mult(scalar, a)
            v = alg.mult(scalar, b)
        else:
            u = alg.mult(a, scalar)
            v = alg.mult(b, scalar)
        return AbstractComplexNumber(u, v, alg)

    def conj(self):
        """Return the conjugate of this element."""
        alg = self.algebra
        a, b = self.unpack()
        return AbstractComplexNumber(a, alg.inv(b), alg)

    def sqr_abs_val(self):
        """Return the squared absolute value of this element."""
        w = self * self.conj()
        # The imaginary part should be equal to the field's additive identity
        if w.imag == self.algebra.zero:
            return w.real
        else:
            raise ValueError(f"{w.imag} != {self.algebra.add_identity}")

    def inv(self):
        """Return the inverse of this element."""
        if isinstance(self.algebra, Field):
            absqr = self.sqr_abs_val()
            conj = self.conj()
            return conj.scalar_mult(self.algebra.mult_inv(absqr))
        else:
            return ValueError(f"{self} must be a Field.")

    def __truediv__(self, other):
        if isinstance(self.algebra, Field):
            return self * other.inv()
        else:
            return ValueError(f"{self} must be a Field.")