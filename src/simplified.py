import numpy as np
import itertools as it
import pprint as pp

class CayleyTable:
    """Represents a finite algebra's binary operation as a square array of integers, 0...n-1,
    where n is the order of the algebra, and the integers are indices, NOT algebraic elements.
    The indices denote the positions of the algebra's elements in a list."""

    def __init__(self, array: list[list[int]]):
        tmp = np.array(array, dtype=int)
        nrows, ncols = tmp.shape
        if nrows == ncols:
            if (np.min(tmp) >= 0) and (np.max(tmp) < nrows):
                self.__table = tmp
            else:
                raise ValueError(f"Array elements must be integers between 0 and {nrows - 1}, inclusive.")
        else:
            raise ValueError(f"The array must be square.")

    def __repr__(self):
        """Returns a text representation of the Cayley table that can be copied and pasted."""
        return f"{self.__class__.__name__}({self.__table.tolist()})"

    def __getitem__(self, tup: tuple[int, int]) -> int:
        """Accesses a table element given its row & column indices"""
        row, col = tup
        return self.__table[row][col]

    @property
    def size(self) -> int:
        """Returns the number of rows, or columns, of the table"""
        return self.__table.shape[0]

    def tolist(self) -> list[list[int]]:
        """Returns the table's nparray as a list of lists of ints."""
        return self.__table.tolist()

    @property
    def is_associative(self) -> bool:
        """Returns True if the table represents an associative algebra, otherwise returns False"""
        indices = range(self.size)
        result = True
        for a in indices:
            for b in indices:
                for c in indices:
                    ab = self.__table[a][b]
                    bc = self.__table[b][c]
                    if not (self.__table[ab][c] == self.__table[a][bc]):
                        result = False
                        break
        return result

    @property
    def is_commutative(self) -> bool:
        """Returns True if the table supports a commutative algebra, otherwise returns False"""
        n = self.size
        result = True
        for a in range(n):
            # Loop over the table's upper off-diagonal elements
            for b in range(a + 1, n):
                if self.__table[a][b] != self.__table[b][a]:
                    result = False
                    break
        return result


class BinaryOperator:
    """Implements an algebra's a binary operator. To instantiate this requires the algebra's
    list of elements and Cayley table, where the order of elements in the list matches the
    order of rows and columns in the Cayley table."""

    def __init__(self, elements: list[str], cayley_table: CayleyTable):
        self.__elements = elements
        self.__table = cayley_table

    def __call__(self, elem1: str, elem2: str) -> str:
        """Returns the algebra's sum of elem1 and elem2, according to its Cayley table."""
        row = self.__elements.index(elem1)
        col = self.__elements.index(elem2)
        index = self.__table[row, col]
        return self.__elements[index]

    @property
    def elements(self) -> list[str]:
        """Returns the algebra's list of elements."""
        return self.__elements

    @property
    def table(self) -> CayleyTable:
        """Returns the algebra's Cayley table."""
        return self.__table


class FiniteAlgebra:
    """Represents a finite algebra. To instantiate this requires a list of the algebra's
    elements and its Cayley table."""

    def __init__(self, elements: list[str], array: list[list[int]]):
        self.__binop = BinaryOperator(elements, CayleyTable(array))

    def __getitem__(self, index: int) -> str:
        return self.__binop.elements[index]

    def __repr__(self) -> str:
        elems = self.__binop.elements
        tbl = self.__binop.table.tolist()
        return f"{self.__class__.__name__}(\n{elems},\n{tbl}\n)"

    @property
    def elements(self) -> list[str]:
        """Returns the algebra's list of elements."""
        return self.__binop.elements

    @property
    def order(self) -> int:
        """Returns the number of elements in the algebra."""
        return len(self.elements)

    @property
    def table(self) -> CayleyTable:
        """Returns the algebra's Cayley table."""
        return self.__binop.table

    @property
    def is_associative(self) -> bool:
        """Returns True if the algebra is associative, otherwise returns False."""
        return self.__binop.table.is_associative

    @property
    def is_commutative(self) -> bool:
        """Returns True if the algebra is commutative, otherwise returns False."""
        return self.__binop.table.is_commutative

    def op(self, elem1: str, elem2: str) -> str:
        """Return the sum (or product) of the two algebra elements"""
        return self.__binop(elem1, elem2)

    def __mul__(self, other):
        """Return the direct product (a FiniteAlgebra) of self with other. Other must be an algebra"""
        dp_elements = list(it.product(self.elements, other.elements))  # cross-product of elements
        dp_table = list()  # start a new table
        for a in dp_elements:
            dp_table_row = list()  # Start a new row
            for b in dp_elements:
                dp_table_row.append(dp_elements.index((self.op(a[0], b[0]), other.op(a[1], b[1]))))
            dp_table.append(dp_table_row)  # Append the new row to the table
        return FiniteAlgebra(list([f"{elem[0]}:{elem[1]}" for elem in dp_elements]), dp_table)

    def info(self) -> None:
        """Printout information about this instance of an Algebra, including its elements and Cayley table."""
        print(f"\n** {self.__class__.__name__} **")
        print(f"Instance ID: {id(self)}")
        print(f"Order: {self.order}")
        print(f"Associative? {self.is_associative}")
        print(f"Commutative? {self.is_commutative}")
        print(f"Elements: {self.elements}")
        print("Table:")
        pp.pprint(self.table.tolist())
        return None

    def element_map(self):
        """Returns a dictionary where element names (str) are keys and the corresponding
        Element instances are the values. This method's intended use is within the
        definition of a Context."""
        return {elem: Element(elem, self) for elem in self.elements}


class Element:
    """This class is used to turn the usual string elements of an algebra into a class
    that can have arithmetic methods, like + or *."""
    def __init__(self, elem_name: str, algebra: FiniteAlgebra):
        self.__algebra = algebra
        if isinstance(elem_name, str):
            if elem_name in self.__algebra:
                self.__name = elem_name
            else:
                raise ValueError(f"name must be an element of algebra")
        else:
            raise ValueError(f"name must be a string")

    def __repr__(self):
        return repr(self.__name)

    @property
    def name(self) -> str:
        """Returns the Element's name, a string."""
        return self.__name

    def __add__(self, other):
        elem = self.__algebra.op(self.__name, other.name)
        return Element(elem, self.__algebra)


class Context:

    def __init__(self, algebra: FiniteAlgebra):
        self.element_map = algebra.element_map()

    def __enter__(self):
        return self.element_map

    def __exit__(self, _type, value, traceback):
        pass
