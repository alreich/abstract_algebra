"""
@author: Alfred J. Reich

"""

import json
import functools
import pprint as pp
import numpy as np
import itertools as it
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
        if isinstance(table, CayleyTable):
            self.__table = table
        elif isinstance(table[0][0], str):
            index_tbl = index_table_from_name_table(elements, table)
            self.__table = CayleyTable(index_tbl)
        else:
            self.__table = CayleyTable(table)

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
    
    @property
    def order(self):
        return len(self.__elements)

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

    def about(self, max_size=12, use_table_names=False):
        print(f"\n{self.__class__.__name__}: {self.name}\n{self.description}")
        print(f"Abelian? {self.is_abelian()}")
        spc = 7
        print("Elements:")
        print("   Index   Name   Inverse  Order")
        for elem in self:
            idx_elem = self.elements.index(elem)
            if isinstance(self, Group):
                inv_elem = self.inv(elem)
            else:
                inv_elem = "-"
            ord_elem = self.elements(elem)
            print(f"{idx_elem :>{spc}} {elem :>{spc}} {inv_elem :>{spc}} {ord_elem :>{spc}}")
        size = len(self.elements)
        if size <= max_size:
            if use_table_names:
                print(f"Cayley Table (showing names):")
                pp.pprint(self.table_as_list_with_names())
            else:
                print(f"Cayley Table (showing indices):")
                pp.pprint(self.table.tolist())
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so no further info calculated/printed.")
        return None


# =========
#   Magma
# =========

class Magma(FiniteAlgebra):

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        self.__element_orders = {elem: None for elem in self.elements}
        self.__dp_delimiter = ':'  # name delimiter used when creating Direct Products

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

    def element_order(self, element):
        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.op(prod, elem), order + 1)
        if self.__element_orders[element] is None:
            self.__element_orders[element] = order_aux(element, element, 1)
        return self.__element_orders[element]

    def direct_product_delimiter(self, delimiter=None):
        """If no input, then the current direct product element name delimiter will be returned (default is ':').
        Otherwise, if a string is input (e.g., "-") it will become the new delimiter for direct product element
        names, and then it will be returned."""
        if delimiter:
            self.__dp_delimiter = delimiter
            return self.__dp_delimiter
        else:
            return self.__dp_delimiter

    def __mul__(self, other):  # Direct Product of two Magmas
        """Return direct product of this algebra with the `other` algebra."""
        dp_name = f"{self.name}_x_{other.name}"
        dp_description = "Direct product of " + self.name + " & " + other.name
        dp_element_names = list(it.product(self.elements, other.__element_names))  # Cross product
        dp_mult_table = list()
        for a in dp_element_names:
            dp_mult_table_row = list()  # Start a new row
            for b in dp_element_names:
                dp_mult_table_row.append(dp_element_names.index((self.op(a[0], b[0]), other.mult(a[1], b[1]))))
            dp_mult_table.append(dp_mult_table_row)  # Append the new row to the table
        return self.__class__(dp_name,
                              dp_description,
                              list([f"{elem[0]}{self.__dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                              dp_mult_table)


# =============
#   Semigroup
# =============

class Semigroup(Magma):
    """A semigroup is an associative magma."""

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        if not self.table.is_associative():
            raise ValueError("Table does not support associativity")


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):
    """A monoid is a semigroup with an identity element."""

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        self.__identity = self.table.identity()
        if self.__identity is None:
            raise ValueError("Table has no identity element")

    @property
    def identity(self):
        return self.__identity

    # ---------------------
    # FINDING ISOMORPHISMS
    # ---------------------
    #
    # Assumes that the identity is the first element in the elements list.
    #
    # TODO: Remove this assumption

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all possible permutations
        of other's elements, where the identity of this algebra is always mapped to the identity of other."""
        if self.order == other.order:
            elems0 = self.elements
            elems1 = other.__element_names
            mappings = [dict(zip(elems0[1:], perm)) for perm in it.permutations(elems1[1:])]
            for mapping in mappings:
                mapping[elems0[0]] = elems1[0]
            return mappings
        else:
            raise Exception(f"Algebras must be of the same order: {self.order} != {other.order}")

    def isomorphic_mapping(self, other, mapping):
        """Returns True if the input mapping from this algebra to the other algebra is isomorphic."""
        elems = self.elements
        return all([mapping[self.op(x, y)] == other.mult(mapping[x], mapping[y]) for x in elems for y in elems])

    def isomorphic(self, other):
        """If there is a mapping from elements of this algebra to the other algebra's elements,
        return it; otherwise return False."""
        if self.order == other.order:
            maps = self.element_mappings(other)
            for mp in maps:
                if self.isomorphic_mapping(other, mp):
                    return mp
            return False
        else:
            return False


# =========
#   Group
# =========

class Group(Monoid):
    """A group is a monoid with inverses."""

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        if not self.table.has_inverses():
            raise ValueError("Table has insufficient inverses")
        else:
            self.__inverses = self.create_inverse_lookup_dict()

    def create_inverse_lookup_dict(self):
        row_indices, col_indices = np.where(self.table.table == self.identity)
        return {self.elements[elem_index]: self.elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def inv(self, element):
        """Return the inverse of an element"""
        return self.__inverses[element]

    def conj(self, a, g):
        """Return g * a * inv(g), the conjugate of a with respect to g"""
        return self.op(g, self.op(a, self.inv(g)))


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
