"""
@author: Alfred J. Reich

"""

# New Object Hierarchy (WORK-IN-PROGRESS)

import json
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
    
    def __init__(self, elements, table, metadata=None):
        self.__elements = elements
        self.__table = CayleyTable(table)
        self.metadata = metadata  # dictionary with, say, name, description, etc.
        # The following values, if they exist, are cached on first access
        self.__is_associative = None
        self.__is_commutative = None
        self.__has_identity = None
        self.__identity = None
        self.__inverses = None

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

    def __str__(self):
        return f"{self.__class__.__name__}({self.__elements}, {self.__table.tolist()})"

    @property
    def elements(self):
        return self.__elements
    
    @property
    def table(self):
        return self.__table

    def set_elements(self, new_elements):
        if isinstance(new_elements, list):
            self.__elements = new_elements
        elif isinstance(new_elements, dict):
            self.__elements = [new_elements[elem] for elem in self.__elements]
        return self
    
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
    
    def table_as_list_with_names(self):
        return [[self.__elements[index] for index in row] for row in self.__table.tolist()]

    def is_associative(self):
        return get_cached_value(self.__is_associative, self.__table.is_associative)

    def is_commutative(self):
        return get_cached_value(self.__is_commutative, self.__table.is_commutative)

    def identity(self):
        return self.__table.identity()

    def has_inverses(self):
        return self.__table.has_inverses()


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


# ====================
# Finite Algebra Maker
# ====================

def finite_algebra_maker(*args):

    if len(args) == 1:

        # Create from a JSON file
        if isinstance(args[0], str):
            with open(args[0], 'r') as fin:
                finalg_dict = json.load(fin)

        # Create from a dictionary
        elif isinstance(args[0], dict):
            finalg_dict = args[0]

        # Create from a list of lists of element names (str)
        elif isinstance(args[0], list):
            finalg_dict = {'name': "no name",
                           'description': "Constructed from multiplication table",
                           'elements': args[0][0],
                           'table': args[0]
                           }

        # No other type of single argument can create a Finite Algebra
        else:
            raise Exception("Single argument must be a string or a dictionary.")

    # If 3 args, then they are: name, description, & table element names (list of lists of str)
    elif len(args) == 3:
        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'elements': args[2][0],  # top row of table input
                       'table': index_table_from_name_table(args[2])
                       }

    # If 4 args, then they are: name, description, list of element names, & table (ints)
    else:
        # Assumes all four possible fields were input
        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'elements': args[2],
                       'table': args[3]
                       }

    # Create the list of element names
    if finalg_dict.get('elements') is None:
        finalg_dict['elements'] = finalg_dict['table'][0]  # First row of table

    # Create a CayleyTable object
    tbl = finalg_dict['table']
    if isinstance(tbl[0][0], str):
        finalg_dict['table'] = index_table_from_name_table(tbl)

    return finalg_dict


def print_finite_algebra(finalg_dict):
    nm = finalg_dict['name']
    desc = finalg_dict['description']
    elems = finalg_dict['element_names']
    tbl = finalg_dict['cayley_table']
    return f"FiniteAlgebra('{nm}',\n'{desc}',\n{elems},\n{tbl}) "


def index_table_from_name_table(name_table):
    top_row = name_table[0]
    return [[top_row.index(elem_name) for elem_name in row] for row in name_table]



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
