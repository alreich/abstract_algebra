#!/usr/bin/env python
# coding: utf-8

import numpy as np


# Table Utilities

def is_associative(table):
    indices = range(len(table))
    result = True
    for a in indices:
        for b in indices:
            for c in indices:
                ab = table[a][b]
                bc = table[b][c]
                if not (table[ab][c] == table[a][bc]):
                    result = False
                    break
    return result


def is_commutative(table):
    indices = range(len(table))
    result = True
    for a in indices:
        for b in indices:
            if table[a][b] != table[b][a]:
                result = False
                break
    return result


def has_left_identity(table):
    indices = range(len(table))
    identity = None
    for x in indices:
        if all(table[x][y] == y for y in indices):
            identity = x
            break
    return identity


def has_right_identity(table):
    indices = range(len(table))
    identity = None
    for x in indices:
        if all(table[y][x] == y for y in indices):
            identity = x
            break
    return identity


def has_identity(table):
    left_id = has_left_identity(table)
    right_id = has_right_identity(table)
    if (left_id is not None) and (right_id is not None):
        return left_id
    else:
        return None


def has_inverses(table):
    return False


def inverse_lookup_dict(table, identity):
    elements = range(len(table))
    row_indices, col_indices = np.where(table == identity)
    return {elements[elem_index]: elements[elem_inv_index]
            for (elem_index, elem_inv_index)
            in zip(row_indices, col_indices)}


if __name__ == '__main__':

    print("\n=======================================================================")

    print("\n--------------")
    print("START OF TESTS")
    print("--------------")

    import pprint as pp

    # Table Tests

    print("\nTable Tests:\n")

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

    test_tables = [tbl1, tbl2, tbl3, tbl4, tbl5]

    for tbl in test_tables:
        pp.pprint(tbl)
        print()

    print("   Table     Associative?  Commutative?   Left Id?   Right Id?  Identity?")
    print('-' * 75)
    for tbl in test_tables:
        i = test_tables.index(tbl) + 1
        is_assoc = str(is_associative(tbl))
        is_comm = str(is_commutative(tbl))
        lft_id = str(has_left_identity(tbl))
        rgt_id = str(has_right_identity(tbl))
        ident = str(has_identity(tbl))
        print(f"{i :>{6}} {is_assoc :>{14}} {is_comm :>{12}} {lft_id :>{12}} {rgt_id :>{12}} {ident :>{10}}")

    print("\n------------")
    print("END OF TESTS")
    print("------------")
