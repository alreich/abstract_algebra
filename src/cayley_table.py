"""
@author: Alfred J. Reich

"""

import numpy as np
import itertools as it

class CayleyTable:
    """
    Here is the definition of a Cayley table in Wikipedia, edited to refer
    to finite algebras, in general, not just finite groups:

    'A Cayley table describes the structure of a finite algebra by arranging
    all the possible products of all [the algebra's] elements in a square table
    reminiscent of an addition or multiplication table. Many properties of
    [an algebra] - such as whether or not it is abelian, which elements are
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
                self._table = tmp
            else:
                raise Exception(f"All integers must be between 0 and {nrows - 1}, inclusive.")
        else:
            raise Exception(f"Input arrays must be square; this one is {nrows}x{ncols}.")

    def __repr__(self):
        return f"{self.__class__.__name__}({self._table.tolist()})"

    def __str__(self):
        n = self._table.shape[0]
        return f"<{self.__class__.__name__}, order {n}, ID:{id(self)}>"

    def __getitem__(self, tup):
        row, col = tup
        return self._table[row][col]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, CayleyTable):
            return self.__key() == other.__key()
        return NotImplemented

    def __key(self):
        return tuple(self._table.tolist())

    @property
    def order(self):
        """Returns the order of the table, e.g., a 3x3 table has order 3."""
        return self._table.shape[0]

    @property
    def table(self):
        """Returns the table, i.e., NumPy array."""
        return self._table

    def tolist(self):
        """Converts the CayleyTable into a list of lists of ints."""
        return self._table.tolist()

    def to_list_with_names(self, elements):
        """Returns the Cayley Table as a regular Python array where the element indices have been
        replaces by the element names (str)."""
        return [[elements[index] for index in row] for row in self._table]

    def is_associative(self):
        """Returns True or False, depending on whether the table supports an associative
        binary operation."""
        indices = range(len(self._table))
        # result = True
        for a in indices:
            for b in indices:
                for c in indices:
                    ab = self._table[a][b]
                    bc = self._table[b][c]
                    if not (self._table[ab][c] == self._table[a][bc]):
                        # result = False
                        # break
                        return False
        # return result
        return True

    def is_commutative(self):
        """Returns True or False, depending on whether the table supports a commutative
        binary operation."""
        n = self._table.shape[0]
        # result = True
        # Loop over the table's upper off-diagonal elements
        for a in range(n):
            for b in range(a + 1, n):
                if self._table[a][b] != self._table[b][a]:
                    # result = False
                    # break
                    return False
        return True

    def distributes_over(self, other, verbose=False):
        """This method determines whether this CayleyTable distributes over an
        'other', equal-sized CayleyTable.  Think of 'self' as multiplication and
        'other' as addition.
        """
        n = self.order
        m = self.order
        if n != m:
            raise ValueError(f"{n} != {m}, but table sizes must be the same.")
        else:
            # is_distributive = True
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
                            # is_distributive = False
                            # break
                            return False
            return True
        # return is_distributive

    def has_cancellation(self, verbose=False):
        """Return True if, for every a & b in the algebra, there are unique x and y in the algebra
        such that ax=b and ya=b. Otherwise, return False. Set verbose to True to see intermediate
        calculations."""
        result = True
        n = self.table.shape[0]  # Number of elements represented by table
        n_sqr = n ** 2
        elems = list(range(n))  # The indices of the elements
        count = 0  # number of successes
        for ab in it.product(elems, elems):
            a = ab[0]
            b = ab[1]
            ab_ok = False
            for xy in it.product(elems, elems):
                x = xy[0]
                y = xy[1]
                # if self.op(a, x) == b and self.op(y, a) == b:
                if int(self[a, x]) == b and int(self[y, a]) == b:
                    count += 1
                    if verbose:
                        print(f"{ab} & {xy}")
                    ab_ok = True
                    # break
            if not ab_ok:
                result = False
                if verbose:
                    print(f"{ab} fail")
        if verbose:
            print(f"Number of successes, {count}, should equal {n_sqr}")
        if result:
            if count == n_sqr:
                return True
            elif count > n_sqr:
                if verbose:
                    print(f"Count of {count} > {n_sqr} means some cancellations are not unique.")
                return False
            else:
                raise Exception(f"A True result with count {count} < {n_sqr} means something went wrong.")
        else:
            return False

    def left_identity(self):
        """Returns the table's left identity element, if it exists, otherwise None is returned."""
        indices = range(len(self._table))
        # lid = None
        for x in indices:
            if all(self._table[x][y] == y for y in indices):
                # lid = x
                # break
                return x
        # return lid
        return None

    def right_identity(self):
        """Returns the table's right identity element, if it exists, otherwise None is returned."""
        indices = range(len(self._table))
        # rid = None
        for x in indices:
            if all(self._table[y][x] == y for y in indices):
                # rid = x
                # break
                return x
        # return rid
        return None

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
            row_indices, col_indices = np.where(self._table == self.identity())
            if set(row_indices) == set(col_indices):
                if len(row_indices) == self.order:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def inverse_lookup_dict(self, identity, elements=None):
        if elements is None:
            elements = range(len(self._table))
        row_indices, col_indices = np.where(self._table == identity)
        return {elements[elem_index]: elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def table_entries_where_equal_to(self, val):
        """Return all (row, col) pairs where table entries equal val."""
        row_indices, col_indices = np.where(self.table == val)
        index_pairs = list(zip(row_indices, col_indices))
        return index_pairs

    def type_of_algebra(self):
        if self.is_associative():
            if self.identity() is not None:
                if self.has_inverses():
                    # result = "Group"
                    return "Group"
                else:
                    # result = "Monoid"
                    return "Monoid"
            else:
                # result = "Semigroup"
                return "Semigroup"
        else:
            # result = "Magma"
            return "Magma"
        # return result

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
        alg = self.type_of_algebra()
        if printout:
            print("  Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?  Algebra?")
            print('-' * 100)
            print(f"{n :>{6}} {ass :>{11}} {co :>{12}} {lid :>{12}} {rid :>{9}} {ident :>{10}} {invs :>{10}} {alg :>{10}}")
            return None
        else:
            return n, ass, co, lid, rid, ident, invs, alg


# Utility

def about_tables(list_of_cayley_tables):
    print("   Table  Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?  Algebra?")
    print('-' * 100)
    for tbl in list_of_cayley_tables:
        i = list_of_cayley_tables.index(tbl) + 1
        n, ass, co, lid, rid, ident, invs, alg = tbl.about()
        print(f"{i :>{6}} {n :>{6}} {ass :>{11}} {co :>{12}} {lid :>{12}} {rid :>{9}} {ident :>{10}} {invs :>{10}} {alg :>{10}}")


# END OF FILE
