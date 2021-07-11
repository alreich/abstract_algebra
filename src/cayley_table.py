"""
@author: Alfred J. Reich

"""

import numpy as np
import pprint as pp


class CayleyTable:

    def __init__(self, arr):
        tmp = np.array(arr, dtype=int)
        nrows, ncols = tmp.shape
        if nrows == ncols:
            if (tmp.min() >= 0) and (tmp.max() < nrows):
                self.__order = nrows
                self.__table = tmp
            else:
                raise Exception(f"All integers must be between 0 and {nrows - 1}, inclusive.")
        else:
            raise Exception(f"Input arrays must be square; this one is {nrows}x{ncols}.")

    def __repr__(self):
        return f"{self.__class__.__name__}(\n{pp.pformat(self.__table.tolist())}\n)"

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

    def left_identity(self):
        indices = range(len(self.__table))
        identity = None
        for x in indices:
            if all(self.__table[x][y] == y for y in indices):
                identity = x
                break
        return identity

    def right_identity(self):
        indices = range(len(self.__table))
        identity = None
        for x in indices:
            if all(self.__table[y][x] == y for y in indices):
                identity = x
                break
        return identity

    def identity(self):
        left_id = self.left_identity()
        right_id = self.right_identity()
        if (left_id is not None) and (right_id is not None):
            return left_id
        else:
            return None

    def has_inverses(self):
        if self.identity:
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


# END OF FILE
