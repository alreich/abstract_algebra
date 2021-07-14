"""
@author: Alfred J. Reich

"""

import json
import functools
from cayley_table import CayleyTable


# A useful pattern
# def get_cached_value(cached_value, accessor):
#     if cached_value is None:
#         cached_value = accessor()
#     return cached_value


# =================
#   FiniteAlgebra
# =================

class FiniteAlgebra:

    def __init__(self, name, description, elements, table):
        self.name = name
        self.description = description
        self.__elements = elements
        # if isinstance(table, CayleyTable):
        #     self.__table = table
        # else:
        #     self.__table = CayleyTable(table)
        if isinstance(table, CayleyTable):
            self.__table = table
        elif isinstance(table[0][0], str):
            index_tbl = index_table_from_name_table(elements, table)
            self.__table = CayleyTable(index_tbl)
        else:
            self.__table = CayleyTable(table)

    # def init(self, *args):
    #
    #     if len(args) == 1:
    #
    #         # Create from a JSON file
    #         if isinstance(args[0], str):
    #             with open(args[0], 'r') as fin:
    #                 finalg_dict = json.load(fin)
    #
    #         # Create from a dictionary
    #         elif isinstance(args[0], dict):
    #             finalg_dict = args[0]
    #
    #         else:
    #             raise ValueError("If there's a single input, then it must be a string or a dictionary.")
    #
    #     elif len(args) == 4:
    #
    #         finalg_dict = {'name': args[0],
    #                        'description': args[1],
    #                        'element_names': args[2],
    #                        'mult_table': args[3]
    #                        }
    #     else:
    #         raise ValueError("Incorrect number of input arguments.")
    #
    #     self.name = finalg_dict['name']
    #     self.description = finalg_dict['description']
    #     self.__elements = finalg_dict['element_names']
    #     tbl = finalg_dict['mult_table']
    #     # Check if first element in table is a string
    #     if isinstance(tbl[0][0], str):
    #         index_tbl = index_table_from_name_table(self.elements, tbl)
    #         self.__table = CayleyTable(index_tbl)
    #     else:
    #         self.__table = CayleyTable(tbl)

    # def __init__(self, name, description, elements, table):

    # def __init__(self, *args):
    #
    #     if len(args) == 1:
    #         if isinstance(args[0], str):
    #             with open(args[0], 'r') as fin:
    #                 finalg_dict = json.load(fin)
    #                 self.name = finalg_dict['name']
    #                 self.description = finalg_dict['description']
    #                 self.__elements = finalg_dict['element_names']
    #                 self.__table = finalg_dict['mult_table']
    #
    #     if len(args) == 4:
    #         name = args[0]
    #         description = args[1]
    #         elements = args[2]
    #         table = args[3]
    #         self.name = name
    #         self.description = description
    #         self.__elements = elements
    #         if isinstance(table, CayleyTable):
    #             self.__table = table
    #         elif isinstance(table[0][0], str):
    #             index_tbl = index_table_from_name_table(elements, table)
    #             self.__table = CayleyTable(index_tbl)
    #         else:
    #             self.__table = CayleyTable(table)

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
        nm = self.name
        desc = self.description
        elems = self.__elements
        tbl = self.__table.tolist()
        return f"{self.__class__.__name__}(\n{nm},\n{desc},\n{elems},\n{tbl}\n)"

    def __str__(self):
        nm = self.name
        desc = self.description
        elems = self.__elements
        tbl = self.__table.tolist()
        return f"{self.__class__.__name__}({nm}, {desc}, {elems}, {tbl})"

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
    
    def table_as_list_with_names(self):
        return [[self.__elements[index] for index in row] for row in self.__table.tolist()]

    def is_associative(self):
        return self.__table.is_associative()

    def is_commutative(self):
        return self.__table.is_commutative()

    def is_abelian(self):
        return self.is_commutative()

    def identity(self):
        return self.__table.identity()

    def has_inverses(self):
        return self.__table.has_inverses()

    def to_dict(self):
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'element_names': self.__elements,
                'mult_table': self.__table.tolist()
                }

    def dumps(self):
        return json.dumps(self.to_dict())

    def dump(self, json_filename):
        with open(json_filename, 'w') as fout:
            json.dump(self.to_dict(), fout)


# =========
#   Magma
# =========

class Magma(FiniteAlgebra):

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)

    # def __init__(self, *args):
    #     super().__init__(*args)

    def op(self, *args):
        if len(args) == 1:
            if args[0] in self.elements:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid element name")
        elif len(args) == 2:
            row = self.elements.index(args[0])
            col = self.elements.index(args[1])
            index = self.table[row, col]
            return self.elements[index]
        else:
            return functools.reduce(lambda a, b: self.op(a, b), args)


# =============
#   Semigroup
# =============

class Semigroup(Magma):
    """A semigroup is an associative magma."""
    # def __init__(self, *args):
    #     super().__init__(*args)
    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        if not self.table.is_associative():
            raise ValueError("Table does not support associativity")


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):
    """A monoid is a semigroup with an identity element."""
    # def __init__(self, *args):
    #     super().__init__(*args)
    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        if self.table.identity() is None:
            raise ValueError("Table has no identity element")


# =========
#   Group
# =========

class Group(Monoid):
    """A group is a monoid with inverses."""
    # def __init__(self, *args):
    #     super().__init__(*args)
    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        if not self.table.has_inverses():
            raise ValueError("Table has insufficient inverses")


# =====================
# Make Finite Algebra
# =====================

def make_finite_algebra(*args):

    if len(args) == 1:

        # Create from a JSON file
        if isinstance(args[0], str):
            with open(args[0], 'r') as fin:
                finalg_dict = json.load(fin)

        # Create from a dictionary
        elif isinstance(args[0], dict):
            finalg_dict = args[0]

        else:
            raise ValueError("If there's a single input, then it must be a string or a dictionary.")

    elif len(args) == 4:

        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'element_names': args[2],
                       'mult_table': args[3]
                       }
    else:
        raise ValueError("Incorrect number of input arguments.")

    name = finalg_dict['name']
    desc = finalg_dict['description']
    elems = finalg_dict['element_names']
    tbl = finalg_dict['mult_table']
    # Check if first element in table is a string
    if isinstance(tbl[0][0], str):
        index_tbl = index_table_from_name_table(elems, tbl)
        table = CayleyTable(index_tbl)
    else:
        table = CayleyTable(tbl)

    is_assoc = table.is_associative()
    has_id = table.identity()
    if has_id is not None:
        inverses = table.has_inverses()
    else:
        inverses = None

    if is_assoc:
        if has_id is not None:
            if inverses:
                return Group(name, desc, elems, table)
            else:
                return Monoid(name, desc, elems, table)
        else:
            return Semigroup(name, desc, elems, table)
    else:
        return Magma(name, desc, elems, table)


def index_table_from_name_table(elements, name_table):
    return [[elements.index(elem_name) for elem_name in row] for row in name_table]


# End of File
