"""
@author: Alfred J. Reich

"""

import numpy as np


class CayleyTable:
    """
    Here is the definition of a Cayley table in Wikipedia, edited to refer
    to finite algebras, in general, not just finite groups:

    'A Cayley table describes the structure of a finite algebra by arranging
    all the possible products of all [the algebra's] elements in a square table
    reminiscent of an addition or multiplication table. Many properties of
    [an algebra] – such as whether or not it is abelian, which elements are
    inverses of which elements, [etc.] – can be discovered from its Cayley table.'
    (https://en.wikipedia.org/wiki/Cayley_table)

    The actual table, within a CayleyTable instance, is stored as a square
    NumPy array of int, where the integers correspond to the positions of
    elements in a list of element names (str).

    Regarding the interpretation of a Cayley table, the row element is "multiplied"
    on the left and the column element on the right, e.g., row * col.  Or, assuming
    functions written on the left, such as permutations, this means that the column
    element is applied first and the row element is applied next, e.g., row(col(x)).
    """

    def __init__(self, arr):
        tmp = np.array(arr, dtype=int)
        nrows, ncols = tmp.shape
        if nrows == ncols:
            if (np.min(tmp) >= 0) and (np.max(tmp) < nrows):
                self.__order = nrows
                self.__table = tmp
            else:
                raise Exception(f"All integers must be between 0 and {nrows - 1}, inclusive.")
        else:
            raise Exception(f"Input arrays must be square; this one is {nrows}x{ncols}.")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__table.tolist()})"

    def __str__(self):
        n = self.__order
        return f"<{self.__class__.__name__}, order {n}, ID:{id(self)}>"

    def __eq__(self, other):
        compare = (self.__table == other.table)
        return compare.all()

    def __getitem__(self, tup):
        row, col = tup
        return self.__table[row][col]

    @property
    def order(self):
        """Returns the order of the table, e.g., a 3x3 table has order 3."""
        return self.__order

    @property
    def table(self):
        """Returns the table, i.e., NumPy array."""
        return self.__table

    def tolist(self):
        """Converts the CayleyTable into a list of lists of ints."""
        return self.__table.tolist()

    def to_list_with_names(self, elements):
        """Returns the Cayley Table as a regular Python array where the element indices have been
        replaces by the element names (str)."""
        return [[elements[index] for index in row] for row in self.__table]

    def is_associative(self):
        """Returns True or False, depending on whether the table supports an associative
        binary operation."""
        indices = range(len(self.__table))
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

    def is_commutative(self):
        """Returns True or False, depending on whether the table supports a commutative
        binary operation."""
        n = self.__table.shape[0]
        result = True
        # Loop over the table's upper off-diagonal elements
        for a in range(n):
            for b in range(a + 1, n):
                if self.__table[a][b] != self.__table[b][a]:
                    result = False
                    break
        return result

    def distributes_over(self, other, verbose=False):
        """This method determines whether this CayleyTable distributes over an
        'other', equal-sized CayleyTable.  Think of 'self' as multiplication and
        'other' as addition.
        """
        n = self.__order
        m = other.order
        if n != m:
            raise ValueError(f"{n} != {m}, but table sizes must be the same.")
        else:
            is_distributive = True
            for a in range(n):
                for b in range(n):
                    for c in range(n):
                        other_bc = other[b, c]  # e.g., b + c
                        ab = self[a, b]  # e.g., a * b
                        ac = self[a, c]  # e.g., a * c
                        if self[a, other_bc] != other[ab, ac]:  # a(b + c) != ab + ac
                            if verbose:
                                print(f"\na = {a}; b = {b}; c = {c}")
                                print(f"{a} x {other_bc} != {ab} + {ac}")
                            is_distributive = False
                            break
        return is_distributive

    def left_identity(self):
        """Returns the table's left identity element, if it exists, otherwise None is returned."""
        indices = range(len(self.__table))
        lid = None
        for x in indices:
            if all(self.__table[x][y] == y for y in indices):
                lid = x
                break
        return lid

    def right_identity(self):
        """Returns the table's right identity element, if it exists, otherwise None is returned."""
        indices = range(len(self.__table))
        rid = None
        for x in indices:
            if all(self.__table[y][x] == y for y in indices):
                rid = x
                break
        return rid

    def identity(self):
        """Returns the table's identity element, if it exists, otherwise None is returned."""
        left_id = self.left_identity()
        right_id = self.right_identity()
        if (left_id is not None) and (right_id is not None):
            # If both left and right identities exist, then they are necessarily equal.
            return left_id
        else:
            return None

    def has_inverses(self):
        """Returns True or False, depending on whether the table supports inverses for
        all elements."""
        if self.identity() is not None:
            row_indices, col_indices = np.where(self.__table == self.identity())
            if set(row_indices) == set(col_indices):
                if len(row_indices) == self.__order:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def inverse_lookup_dict(self, identity):
        elements = range(len(self.__table))
        row_indices, col_indices = np.where(self.__table == identity)
        return {elements[elem_index]: elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def about(self, printout=False):
        """Printout information about the CayleyTable: order, associativity,
        commutativity, left/right identities, full identity, and whether
        inverses exist."""
        n = str(self.order)
        ass = str(self.is_associative())
        co = str(self.is_commutative())
        lid = str(self.left_identity())
        rid = str(self.right_identity())
        ident = str(self.identity())
        invs = str(self.has_inverses())
        if printout:
            print("  Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?")
            print('-' * 85)
            print(f"{n :>{6}} {ass :>{11}} {co :>{12}} {lid :>{12}} {rid :>{9}} {ident :>{10}} {invs :>{10}}")
            return None
        else:
            return n, ass, co, lid, rid, ident, invs


# Utility

def about_tables(list_of_cayley_tables):
    print("   Table  Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?")
    print('-' * 85)
    for tbl in list_of_cayley_tables:
        i = list_of_cayley_tables.index(tbl) + 1
        n, ass, co, lid, rid, ident, invs = tbl.about()
        print(f"{i :>{6}} {n :>{6}} {ass :>{11}} {co :>{12}} {lid :>{12}} {rid :>{9}} {ident :>{10}} {invs :>{10}}")


# END OF FILE
