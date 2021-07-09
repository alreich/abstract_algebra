#!/usr/bin/env python
# coding: utf-8

# New Object Hierarchy (WORK-IN-PROGRESS)

import functools as fnc
from cayley_table import CayleyTable


# A useful pattern
def get_cached_value(cached_value, accessor):
    if cached_value is None:
        cached_value = accessor()
    return cached_value


# =========
#   Magma
# =========

class Magma:
    
    def __init__(self, elems, tbl):
        self.__elements = elems
        self.__table = CayleyTable(tbl)
        self.__is_associative = None
        self.__is_commutative = None
        self.__has_identity = None
        self.__identity = None

    def __eq__(self, other):
        if self.__elements == other.elements:  # Same elements in the same order
            if self.__table == other.table:  # Same tables
                return True
            else:
                return False
        else:
            return False

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
        return [[self.__elements[index] for index in row] for row in self.__table.tolist()]

    def is_associative(self):
        return get_cached_value(self.__is_associative, self.__table.is_associative)

    def is_commutative(self):
        return get_cached_value(self.__is_commutative, self.__table.is_commutative)

    def identity(self):
        pass

    # def is_associative(self):
    #     if self.__is_associative is None:  # Check for no cached value
    #         self.__is_associative = self.__table.is_associative()
    #     return self.__is_associative
    #
    # def is_commutative(self):
    #     if self.__is_commutative is None:  # Check for no cached value
    #         self.__is_commutative = self.__table.is_commutative()
    #     return self.__is_commutative


# =============
#   Semigroup
# =============

class Semigroup(Magma):

    def __init__(self, elems, tbl):
        super().__init__(elems, tbl)
        if not self.table.is_associative():
            raise ValueError("Table does not support associativity")


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):

    def __init__(self, elems, tbl):
        super().__init__(elems, tbl)
        if not self.table.identity():
            raise ValueError("Table has no identity element")


# =========
#   Group
# =========

class Group(Monoid):

    def __init__(self, elems, tbl):
        super().__init__(elems, tbl)
        if not self.table.has_inverses():
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
    print(f"Commutative?: {ex141_sg.table.is_commutative()}")

    # print("\n----------------------------------------------------------------------")
    # print("\nGroup Tests:\n")
    #
    # ex141_sg = Group(['a', 'b', 'c', 'd', 'e', 'f'], ex141_tbl)
    # print(ex141_sg)
    # print(f"Has inverses?: {ex141_sg.table.is_commutative()}")

    print("\n------------")
    print("END OF TESTS")
    print("------------")
