"""
@author: Alfred J. Reich

"""

# from finite_algebras import Field


class AbstractComplexElement:

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
        if isinstance(other, AbstractComplexElement):
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
            return AbstractComplexElement(u, v, alg)

    def __sub__(self, other):
        if self.arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.sub(a, c)
            v = alg.sub(b, d)
            return AbstractComplexElement(u, v, alg)

    def __neg__(self):
        alg = self.algebra
        a, b = self.unpack()
        return AbstractComplexElement(alg.inv(a), alg.inv(b), alg)

    def __mul__(self, other):
        if self.arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.sub(alg.mult(a, c), alg.mult(b, d))
            v = alg.add(alg.mult(a, d), alg.mult(b, c))
            return AbstractComplexElement(u, v, alg)

    @property
    def __key(self):
        return tuple([self.real, self.imag])

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        if isinstance(other, AbstractComplexElement):
            return self.__key == other.__key and self.__alg == other.__alg
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def scalar_mult(self, scalar, left=True):
        """Multiply each element of this object by a scalar, e.g., s*(u,v) = (su, sv).
        To multiply on the right instead, set 'left' to False, e.g., (u,v)*s = (us, vs).
        """
        alg = self.algebra
        a, b = self.unpack()
        if left:
            u = alg.mult(scalar, a)
            v = alg.mult(scalar, b)
        else:
            u = alg.mult(a, scalar)
            v = alg.mult(b, scalar)
        return AbstractComplexElement(u, v, alg)

    def conj(self):
        """Return the conjugate of this element."""
        alg = self.algebra
        a, b = self.unpack()
        return AbstractComplexElement(a, alg.inv(b), alg)

    def sqr_abs_val(self):
        """Return the squared absolute value of this element."""
        w = self * self.conj()
        # The imaginary part should be equal to the field's additive identity
        if w.imag == self.algebra.zero:
            return w.real
        else:
            raise ValueError(f"{w.imag} != {self.algebra.add_identity}")

    def inv(self):
        """Return the inverse of this element. Only works for Fields."""
        absqr = self.sqr_abs_val()
        conj = self.conj()
        return conj.scalar_mult(self.algebra.mult_inv(absqr))

    def __truediv__(self, other):
        """Return the quotient of this and other. Only works for Fields."""
        return self * other.inv()


class Complex:

    def __init__(self, a, b, algebra):
        self.__real = a
        self.__imag = b
        self.__alg = algebra
        self.__dp_delimiter = '_'  # name delimiter used when creating a Complex

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

    def __arithmetic_inputs_ok(self, other):
        if isinstance(other, Complex):
            if self.algebra == other.algebra:
                return True
            else:
                raise ValueError(f"{self.algebra.name} != {other.algebra.name}")
        else:
            raise ValueError(f"{other} is not a Complex")

    def __add__(self, other):
        if self.__arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.add(a, c)
            v = alg.add(b, d)
            return Complex(u, v, alg)

    def __mul__(self, other):
        if self.__arithmetic_inputs_ok(other):
            alg = self.algebra
            a, b = self.unpack()
            c, d = other.unpack()
            u = alg.sub(alg.mult(a, c), alg.mult(b, d))
            v = alg.add(alg.mult(a, d), alg.mult(b, c))
            return Complex(u, v, alg)

    @property
    def __key(self):
        return tuple([self.real, self.imag])

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.__key == other.__key and self.__alg == other.__alg
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    # def complex_delimiter(self, delimiter=None):
    #     """If no input, then the current complex element name delimiter will be returned (default is '_').
    #     Otherwise, if a string is input (e.g., ":") it will become the new delimiter for complex element
    #     names, and then it will be returned."""
    #     if delimiter:
    #         self.__dp_delimiter = delimiter
    #         return self.__dp_delimiter
    #     else:
    #         return self.__dp_delimiter

    def complex_delimiter(self, delimiter=None):
        """If no input, then the current complex element name delimiter will be returned (default is '_').
        Otherwise, if a string is input (e.g., ":") it will become the new delimiter for complex element
        names, and then it will be returned."""
        if delimiter:
            self.__dp_delimiter = delimiter
        return self.__dp_delimiter

