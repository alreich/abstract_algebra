#!/usr/bin/env python
# coding: utf-8

# New Object Hierarchy (WORK-IN-PROGRESS)

import functools as fnc
import numpy as np
import table_utils


# =========
#   Magma
# =========

class Magma:
    
    def __init__(self, elems, tbl):
        self.__elements = elems
        self.__table = np.array(tbl)
        
    def __contains__(self, element):
        return element in self.__elements

    def __getitem__(self, index):
        return self.__elements[index]

    def __repr__(self):
        return f"{self.__class__.__name__}(\n{self.__elements},\n{self.__table.tolist()}\n)"

    @property
    def elements(self):
        return self.__elements
    
    def set_elements(self, new_elements):
        if isinstance(new_elements, list):
            self.__elements = new_elements
        elif isinstance(new_elements, dict):
            self.__elements = [new_elements[elem] for elem in self.__elements]
        return self
    
    @property
    def table(self):
        return self.__table

    def op(self, *args):
        if len(args) == 1:
            if args[0] in self.__elements:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid element name")
        elif len(args) == 2:
            row = self.__elements.index(args[0])
            col = self.__elements.index(args[1])
            index = self.__table[row, col]
            return self.__elements[index]
        else:
            return fnc.reduce(lambda a, b: self.op(a, b), args)
    
    def table_with_names(self):
        return [[self.__elements[index] for index in row] for row in self.__table]


# =============
#   Semigroup
# =============

class Semigroup(Magma):

    def __init__(self, elems, tbl):
        if table_utils.is_associative(tbl):
            super().__init__(elems, tbl)
        else:
            raise ValueError("Table does not support associativity")


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):

    def __init__(self, elems, tbl):
        self.identity = table_utils.has_identity(tbl)
        if self.identity:
            super().__init__(elems, tbl)
        else:
            raise ValueError("Table has no identity element")


# =========
#   Group
# =========

class Group(Monoid):

    def __init__(self, elems, tbl):
        if table_utils.has_inverses(tbl):
            super().__init__(elems, tbl)
        else:
            raise ValueError("Table has insufficient inverses")


if __name__ == '__main__':

    print("\n=======================================================================")

    print("\n--------------")
    print("START OF TESTS")
    print("--------------")

    print("\n----------------------------------------------------------------------")
    print("\nMagma Tests:\n")

    # Rock-Paper-Scissors Magma
    rps = Magma(['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])
    print(rps)
    ps = rps.op('p', 's')
    rp = rps.op('r', 'p')
    r_ps = rps.op('r', ps)
    rp_s = rps.op(rp, 's')
    print(f"    r(ps) = r{ps} = {r_ps}, \nbut (rp)s = {rp}s = {rp_s}")

    print("\n----------------------------------------------------------------------")
    print("\nSemigroup Tests:\n")

    ex141_tbl = [[0, 3, 0, 3, 0, 3], [1, 4, 1, 4, 1, 4], [2, 5, 2, 5, 2, 5],
                 [3, 0, 3, 0, 3, 0], [4, 1, 4, 1, 4, 1], [5, 2, 5, 2, 5, 2]]

    ex141_sg = Semigroup(['a', 'b', 'c', 'd', 'e', 'f'], ex141_tbl)
    print(ex141_sg)
    print(f"Commutative?: {table_utils.is_commutative(ex141_sg.table)}")

    print("\n------------")
    print("END OF TESTS")
    print("------------")
