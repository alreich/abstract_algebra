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
    def identity(cls, size, ring):
        """Create and return an abstract identity matrix using the ring's multiplicative
        identity element, if one exists; otherwise return None."""
        if ring.has_mult_identity():
            id = cls.zeros((size, size), ring)
            for i in range(size):
                id[i, i] = ring.one
            return id
        else:
            print(f"{ring.name} has no unit element for multiplication")
            return None

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

    @property
    def array(self):
        """Returns the abstract matrix's numpy array."""
        return self.__array

    @property
    def shape(self):
        """Returns the shape of the abstract matrix's numpy array"""
        return self.__array.shape

    @property
    def nrows(self):
        """Returns the number of rows of the abstract matrix"""
        return self.__array.shape[0]

    @property
    def ncols(self):
        """Returns the number of columns of the abstract matrix"""
        return self.__array.shape[1]

    @property
    def algebra(self):
        """Returns the ring, over which the abstract matrix is defined."""
        return self.__ring

    @property
    def ring(self):
        """Returns the ring, over which the abstract matrix is defined."""
        return self.__ring

    def copy(self):
        """Returns a copy of the abstract matrix."""
        return AbstractMatrix(np.copy(self.__array), self.__ring)

    def transpose(self):
        """Transposes the rows and columns of the abstract matrix"""
        return AbstractMatrix(np.transpose(self.__array), self.__ring)

    def __getitem__(self, rowcol):
        i, j = rowcol
        return self.__array[i][j]

    def __setitem__(self, rowcol, value):
        if value in self.__ring.elements:
            i, j = rowcol
            self.__array[i][j] = value
        else:
            raise ValueError(f"{value} is not an element of {self.__ring.name}")
        return value

    def __mul__(self, other):
        """Return the product of two abstract matrices."""
        # X * Y
        xarr = self.__array
        xrows = self.nrows
        xcols = self.ncols
        yarr = other.array
        yrows = other.nrows
        ycols = other.ncols
        if xcols == yrows:
            if self.__ring == other.ring:
                ring = self.__ring
                product = np.full((xrows, ycols), ring.zero, dtype='U32')
                for i in range(xrows):
                    for j in range(ycols):
                        for k in range(xcols):
                            product[i, j] = ring.add(product[i, j], ring.mult(xarr[i, k], yarr[k, j]))
            else:
                raise ValueError(f"The array algebras must be equal: {self.ring.name} != {other.ring.name}")
        else:
            raise ValueError(f"The array shapes are incompatible: {xcols} columns vs {yrows} rows")
        return AbstractMatrix(product, ring)

    def __add__(self, other):
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

    def __sub__(self, other):
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
        """Returns a pretty printed representation of the abstract matrix's internal array."""
        return str(self.__array)

    def __repr__(self):
        """Returns a copy-and-paste-able representation of the matrix's internal array,
        NOT a copy-and-paste-able representation of the abstract matrix."""
        return np.array2string(self.__array, separator=', ')

    def __key(self):
        return tuple(self.__array.tolist())

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        if isinstance(other, AbstractMatrix):
            return self.__key() == other.__key() and self.__ring == other.__ring
        else:
            return NotImplemented

    def scalar_mult(self, scalar, left=True):
        """Multiplies every element of an abstract matrix by a single element from the ring, over which
        the abstract matrix is defined. Default is left multiplication, i.e., scalar * self, otherwise
        right multiplication is used, i.e., self * scalar.
        """
        if scalar not in self.__ring.elements:
            raise ValueError(f"{scalar} is not one of the matrix algebra elements")
        array = self.copy().array
        for i in range(self.nrows):
            for j in range(self.ncols):
                if left:
                    array[i, j] = self.__ring.mult(scalar, array[i, j])  # scalar * self
                else:
                    array[i, j] = self.__ring.mult(array[i, j], scalar)  # self * scalar
        return AbstractMatrix(array, self.__ring)

    def minor(self, i, j):
        """Returns the i,j_th minor of the matrix"""
        if 0 <= i < self.nrows:
            if 0 <= j < self.ncols:
                arr1 = np.delete(self.array, i, 0)
                arr2 = np.delete(arr1, j, 1)
            else:
                raise ValueError(f"{j} is not a valid column index")
        else:
            raise ValueError(f"{i} is not a valid row index")
        return AbstractMatrix(arr2, self.__ring)

    def determinant(self):
        """Returns the determinant of a square abstract matrix."""
        if self.nrows != self.ncols:
            raise ValueError(f"Array must be square: ({self.nrows}, {self.ncols})")
        elif self.nrows == 1:
            return self[0, 0]
        elif self.nrows == 2:  # Recursion will stop here
            return self.ring.sub(self.ring.mult(self[0, 0], self[1, 1]),
                                 self.ring.mult(self[0, 1], self[1, 0]))
        else:
            # Use the Laplace expansion to recursively compute the determinant
            det = self.ring.zero  # Start sum using the ring's "zero" element
            for j in range(self.ncols):
                # Alternate "adding" and "subtracting", per the Laplace expansion
                mnr = self.minor(0, j)  # Expand minors along the first row
                mnr_det = mnr.determinant()
                if (-1) ** j == 1:
                    det = self.ring.add(det, self.ring.mult(self[0, j], mnr_det))
                else:
                    det = self.ring.sub(det, self.ring.mult(self[0, j], mnr_det))
        return det

    def cofactor_matrix(self):
        """Returns the cofactor matrix of an abstract matrix"""
        cof = AbstractMatrix.zeros(self.shape, self.__ring)
        for i in range(self.nrows):
            for j in range(self.ncols):
                det = self.minor(i, j).determinant()
                if (-1) ** (i + j) == 1:
                    cof[i, j] = det
                else:
                    cof[i, j] = self.ring.inv(det)
        return cof

    def inverse(self):
        """If the abstract matrix is defined over a field and the matrix's determinant is equal
        to the field's multiplicative identity, '1', then this method returns the matrix's inverse,
        otherwise it returns an inverse-like matrix that, when multiplied by the original matrix,
        yields a diagonal matrix (not necessarily an abstract identity matrix)."""
        det = self.determinant()
        cof = self.cofactor_matrix()
        adj = cof.transpose()
        return adj.scalar_mult(self.ring.inv(det))
