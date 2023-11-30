"""
@author: Alfred J. Reich

"""

import numpy as np


class AbstractMatrix:
    """The abstract matrix class supports the creation of matrices composed of abstract
    Ring elements, along with operations such as addition, subtraction, multiplication,
    determinants, etc.
    """

    def __init__(self, array, ring):
        if isinstance(array, np.ndarray):
            arr = array
        else:
            arr = np.array(array)
        self.__ring = ring
        self.__array = np.array(arr, dtype='<U32')

    @classmethod
    def zeros(cls, shape, ring):
        """Creates and returns an abstract matrix filled with the ring's zero element.
        """
        arr = np.full(shape, ring.zero, dtype='<U32')
        return cls(arr, ring)

    @classmethod
    def random(cls, shape, ring):
        """Creates and returns an abstract matrix containing randomly chosen ring elements.
        """
        rand_indices = np.random.randint(ring.order, size=shape)
        rand_array = np.full(shape, ring.zero, dtype='<U32')
        for i in range(shape[0]):
            for j in range(shape[1]):
                rand_array[i, j] = ring.elements[rand_indices[i, j]]
        return cls(rand_array, ring)

    def array(self):
        """Returns the abstract matrix's numpy array."""
        return self.__array

    def shape(self):
        """Returns the shape of the abstract matrix's numpy array"""
        return self.__array.shape

    def nrows(self):
        """Returns the number of rows in the abstract matrix's numpy array"""
        return self.__array.shape[0]

    def ncols(self):
        """Returns the number of columns in the abstract matrix's numpy array"""
        return self.__array.shape[1]

    def algebra(self):
        """Returns the ring, over which the abstract matrix is defined."""
        return self.__ring

    def ring(self):
        """Returns the ring, over which the abstract matrix is defined."""
        return self.__ring

    def copy(self):
        """Returns a copy of the abstract matrix."""
        return AbstractMatrix(np.copy(self.__array), self.__ring)

    def transpose(self):
        """Transposes the rows and columns of the abstract matrix"""
        return AbstractMatrix(np.transpose(self.__array), self.__ring)

    def __mul__(self, other):  # Matrix multiplication using Ring operations
        """Return the product of two abstract matrices."""
        # X * Y
        xarr  = self.__array
        xrows = self.nrows()
        xcols = self.ncols()
        yarr  = other.array()
        yrows = other.nrows()
        ycols = other.ncols()
        if xcols == yrows:
            print(self.__ring)
            print(other.ring())
            if self.__ring == other.ring():
                ring = self.__ring
                product = np.full((xrows, ycols), ring.zero, dtype='U32')
                for i in range(xrows):
                    for j in range(ycols):
                        for k in range(xcols):
                            product[i, j] = ring.add(product[i, j], ring.mult(xarr[i, k], yarr[k, j]))
            else:
                raise ValueError(f"The array algebras must be equal: {self.ring().name} != {other.ring().name}")
        else:
            raise ValueError(f"The array shapes are incompatible: {xcols} columns vs {yrows} rows")
        return AbstractMatrix(product, ring)

    def __add__(self, other):  # Matrix addition using Ring operations
        """Return the sum of two abstract matrices."""
        # X + Y
        xarr = self.__array
        yarr = other.__array
        xshape = xarr.shape
        yshape = yarr.shape
        if xshape == yshape:
            if self.__ring == other.__ring:
                ring = self.__ring
                result = np.full(xshape, ring.zero, dtype='U32')
                for i in range(xshape[0]):
                    for j in range(xshape[1]):
                        result[i, j] = ring.add(xarr[i, j], yarr[i, j])
            else:
                raise ValueError("The array algebras must be equal")
        else:
            raise ValueError(f"The array shapes are not equal: {xshape} != {yshape}")
        return AbstractMatrix(result, ring)

    def __sub__(self, other):  # Matrix subtraction using Ring operations
        """Return the difference of two abstract matrices."""
        # X - Y
        xarr = self.__array
        yarr = other.__array
        xshape = xarr.shape
        yshape = yarr.shape
        if xshape == yshape:
            if self.__ring == other.__ring:
                ring = self.__ring
                result = np.full(xshape, ring.zero, dtype='U32')
                for i in range(xshape[0]):
                    for j in range(xshape[1]):
                        result[i, j] = ring.sub(xarr[i, j], yarr[i, j])
            else:
                raise ValueError("The array algebras must be equal")
        else:
            raise ValueError(f"The array shapes are not equal: {xshape} != {yshape}")
        return AbstractMatrix(result, ring)

    def __str__(self):
        """Returns the string representation of the numpy array contained in the abstract matrix."""
        return str(self.__array)

    def __repr__(self):
        """Similar to 'str', but also includes the name of the ring over which the abstract matrix is defined."""
        return self.__ring.name + " Matrix:\n" + str(self.__array)

    def determinant(self):
        """Returns the ring element that represents the determinant of the square abstract matrix"""
        return array_determinant(self.__array, self.__ring)

    def cofactor_matrix(self):
        """Returns the abstract cofactor matrix of the square abstract matrix."""
        return AbstractMatrix(array_cofactor(self.__array, self.__ring), self.__ring)

    def scalar_mult(self, scalar, left=True):
        """Multiplies every element of an abstract array by a single element from the ring, over which
        the abstract matrix is defined. Default is left multiplication, i.e., scalar * self, otherwise
        right multiplication is used, i.e., self * scalar.
        """
        if scalar not in self.__ring.elements:
            raise ValueError(f"{scalar} is not one of the matrix algebra elements")
        array = self.copy().array()
        for i in range(self.nrows()):
            for j in range(self.ncols()):
                if left:
                    array[i, j] = self.__ring.mult(scalar, array[i, j])  # scalar * self
                else:
                    array[i, j] = self.__ring.mult(array[i, j], scalar)  # self * scalar
        return AbstractMatrix(array, self.__ring)


def array_determinant(array, ring):
    """Returns the determinant of a square NumPy array of ring elements."""
    nrows = array.shape[0]
    ncols = array.shape[1]
    if nrows != ncols:
        raise ValueError(f"Array must be square: ({nrows}, {ncols})")
    elif nrows == 1:
        return array[0, 0]
    elif nrows == 2:  # Recursion will stop here
        return ring.sub(ring.mult(array[0, 0], array[1, 1]), ring.mult(array[0, 1], array[1, 0]))
    else:
        # Use the Laplace expansion to recursively compute the determinant
        det = ring.zero  # The ring's "zero" element
        arr = np.delete(array, 0, 0)  # Copy array & delete first row
        for i in range(ncols):
            minor = np.delete(arr, i, 1)  # Copy arr & delete the ith column
            # Alternate "adding" and "subtracting", per the Laplace expansion
            if (-1) ** i == 1:
                det = ring.add(det, ring.mult(array[0, i], array_determinant(minor, ring)))
            else:
                det = ring.sub(det, ring.mult(array[0, i], array_determinant(minor, ring)))
        return det


def array_cofactor(array, ring):
    """Returns the cofactor array of an array of ring elements."""
    nrows = array.shape[0]
    ncols = array.shape[1]
    cof = AbstractMatrix.zeros(array.shape, ring).array()
    for i in range(nrows):
        for j in range(ncols):
            arr1 = np.delete(array, i, 0)
            arr2 = np.delete(arr1, j, 1)
            if (-1) ** (i + j) == 1:
                cof[i, j] = array_determinant(arr2, ring)
            else:
                cof[i, j] = ring.inv(array_determinant(arr2, ring))
    return cof
