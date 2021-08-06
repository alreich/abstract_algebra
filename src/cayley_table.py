"""
@author: Alfred J. Reich

"""

import numpy as np
import collections as co


class CayleyTable:

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
        return f"{self.__class__.__name__}({self.__table.tolist()})"

    def __eq__(self, other):
        compare = (self.__table == other.table)
        return compare.all()

    def __getitem__(self, tup):
        row, col = tup
        return self.__table[row][col]

    @property
    def order(self):
        return self.__order

    @property
    def table(self):
        return self.__table

    def tolist(self):
        return self.__table.tolist()

    def is_associative(self):
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
        indices = range(len(self.__table))
        lid = None
        for x in indices:
            if all(self.__table[x][y] == y for y in indices):
                lid = x
                break
        return lid

    def right_identity(self):
        indices = range(len(self.__table))
        rid = None
        for x in indices:
            if all(self.__table[y][x] == y for y in indices):
                rid = x
                break
        return rid

    def identity(self):
        left_id = self.left_identity()
        right_id = self.right_identity()
        if (left_id is not None) and (right_id is not None):
            return left_id
        else:
            return None

    def has_inverses(self):
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


def get_duplicates(lst):
    """Return a list of the duplicate items in the input list."""
    return [item for item, count in co.Counter(lst).items() if count > 1]


# END OF FILE
