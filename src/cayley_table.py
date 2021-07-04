#!/usr/bin/env python
# coding: utf-8
import numpy as np


class CayleyTable:

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], list):
                if all(isinstance(row, list) for row in args[0]):
                    self.order = len(args[0])
                    if all(len(row) == self.order for row in args[0]):
                        self.__table = np.array(args[0])
                    else:
                        raise Exception("Input must represent a square tabl")
                else:
                    raise Exception("All table rows must be lists")
            else:
                raise Exception(f"Single argument type, {type(args[0])}, not supported")
        else:
            raise Exception(f"Incorrect number of arguments")

    def __repr(self):
        print(f"CayleyTable(\n{self.__table}\n)")

    def is_associative(self):
        indices = range(len(self.__table))
        result = True
        for a in indices:
            for b in indices:
                for c in indices:
                    ab = self[a][b]
                    bc = self[b][c]
                    if not (self[ab][c] == self[a][bc]):
                        result = False
                        break
        return result

    def is_commutative(self):
        indices = range(len(self.__table))
        result = True
        for a in indices:
            for b in indices:
                if self[a][b] != self[b][a]:
                    result = False
                    break
        return result

    def has_left_identity(self):
        indices = range(len(self.__table))
        identity = None
        for x in indices:
            if all(self[x][y] == y for y in indices):
                identity = x
                break
        return identity

    def has_right_identity(self):
        indices = range(len(self.__table))
        identity = None
        for x in indices:
            if all(self[y][x] == y for y in indices):
                identity = x
                break
        return identity

    def has_identity(self):
        left_id = self.has_left_identity()
        right_id = self.has_right_identity()
        if (left_id is not None) and (right_id is not None):
            return left_id
        else:
            return None

    # def has_inverses(table):
    #     return False

    def inverse_lookup_dict(self, identity):
        elements = range(len(self.__table))
        row_indices, col_indices = np.where(self == identity)
        return {elements[elem_index]: elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

if __name__ == '__main__':

    import pprint as pp

    print('=' * 75)

    # not assoc; is comm; no identity -- the RPS magma table, above
    tbl1 = [[0, 1, 0], [1, 1, 2], [0, 2, 2]]

    # is assoc; not comm; has identity (0) --- the S3 group table
    tbl2 = [[0, 1, 2, 3, 4, 5], [1, 2, 0, 5, 3, 4], [2, 0, 1, 4, 5, 3],
            [3, 4, 5, 0, 1, 2], [4, 5, 3, 2, 0, 1], [5, 3, 4, 1, 2, 0]]

    # is assoc; is comm; has identity (0) --- the Z4 group table
    tbl3 = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]

    # powerset(3) group table
    tbl4 = [[0, 1, 2, 3, 4, 5, 6, 7], [1, 0, 4, 5, 2, 3, 7, 6], [2, 4, 0, 6, 1, 7, 3, 5],
            [3, 5, 6, 0, 7, 1, 2, 4], [4, 2, 1, 7, 0, 6, 5, 3], [5, 3, 7, 1, 6, 0, 4, 2],
            [6, 7, 3, 2, 5, 4, 0, 1], [7, 6, 5, 4, 3, 2, 1, 0]]

    tbl5 = [[0, 3, 0, 3, 0, 3], [1, 4, 1, 4, 1, 4], [2, 5, 2, 5, 2, 5],
            [3, 0, 3, 0, 3, 0], [4, 1, 4, 1, 4, 1], [5, 2, 5, 2, 5, 2]]

    test_arrays = [tbl1, tbl2, tbl3, tbl4, tbl5]

    test_cayley_tables = [CayleyTable(tbl) for tbl in test_arrays]

    for tbl in test_cayley_tables:
        pp.pprint(tbl)
        print()

    print("   Table     Associative?  Commutative?   Left Id?   Right Id?  Identity?")
    print('-' * 75)
    for tbl in test_cayley_tables:
        i = test_cayley_tables.index(tbl) + 1
        is_assoc = str(tbl.is_associative())
        is_comm = str(tbl.is_commutative())
        lft_id = str(tbl.has_left_identity())
        rgt_id = str(tbl.has_right_identity())
        ident = str(tbl.has_identity())
        print(f"{i :>{6}} {is_assoc :>{14}} {is_comm :>{12}} {lft_id :>{12}} {rgt_id :>{12}} {ident :>{10}}")

    print("\n------------")
    print("END OF TESTS")
    print("------------")
