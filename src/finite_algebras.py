"""
@author: Alfred J. Reich

"""

import json
import functools
import pprint as pp
import numpy as np
import itertools as it

from cayley_table import CayleyTable
from permutations import Perm


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

    def identity_index(self):
        if self.__table.identity() is not None:
            return self.__table.identity()

    @property
    def identity(self):
        if self.__table.identity() is not None:
            return self.__elements[self.__table.identity()]
        else:
            return None

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
            ord_elem = self.element_order(elem)
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
        """Return the 'product' or 'sum' of 1 or more algebra elements as defined by the
        algebra's CayleyTable."""
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
        dp_element_names = list(it.product(self.elements, other.elements))  # Cross product
        dp_mult_table = list()
        for a in dp_element_names:
            dp_mult_table_row = list()  # Start a new row
            for b in dp_element_names:
                dp_mult_table_row.append(dp_element_names.index((self.op(a[0], b[0]), other.op(a[1], b[1]))))
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
        # self.__identity = self.table.identity()
        if self.identity is None:
            raise ValueError("Table has no identity element")

    # @property
    # def identity(self):
    #     return self.__identity

    # @property
    # def identity(self):
    #     return self.elements[self.table.identity()]

    def element_order(self, element):
        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.op(prod, elem), order + 1)
        if self.__element_orders[element] is None:
            self.__element_orders[element] = order_aux(element, element, 1)
        return self.__element_orders[element]

    # ---------------------
    # Monoid Isomorphisms
    # ---------------------
    # Assumes that the identity is the first element in the elements list
    # TODO: Remove this assumption

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all possible permutations
        of other's elements, where the identity of this algebra is always mapped to the identity of other."""
        if self.order == other.order:
            elems0 = self.elements
            elems1 = other.elements
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
        row_indices, col_indices = np.where(self.table.table == self.identity_index())
        return {self.elements[elem_index]: self.elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def inv(self, element):
        """Return the inverse of an element"""
        return self.__inverses[element]

    def conj(self, a, g):
        """Return g * a * inv(g), the conjugate of a with respect to g"""
        return self.op(g, self.op(a, self.inv(g)))


# -----------------
# Group Generators
# -----------------

def generate_cyclic_group(order, identity_name="e", elem_name="a", name=None, description=None):
    """Generates a cyclic group with the given order."""
    if name:
        nm = name
    else:
        nm = "Z" + str(order)
    if description:
        desc = description
    else:
        desc = f"Autogenerated cyclic group of order {order}"
    elements = [identity_name, elem_name] + [f"{elem_name}^" + str(i) for i in range(2, order)]
    table = [[((a + b) % order) for b in range(order)] for a in range(order)]
    return Group(nm, desc, elements, table)


def generate_symmetric_group(n, name=None, description=None, base=1):
    """Generates a symmetric group on n elements. The 'base' is a non-negative integer
    (typically, 0 or 1), so permutations will be tuples, like (1, 2, 3, ..., n), where
    n is the order, or (0, 1, 2, ..., n-1)."""

    if name:
        nm = name
    else:
        nm = "S" + str(n)
    if description:
        desc = description
    else:
        desc = f"Autogenerated symmetric group on {n} elements"
    ident = tuple(range(base, n + base))
    perms = list(it.permutations(ident))
    elem_dict = {str(p): Perm(p) for p in perms}
    rev_elem_dict = {val: key for key, val in elem_dict.items()}
    mul_tbl = [[rev_elem_dict[elem_dict[a] * elem_dict[b]]
                for b in elem_dict]
               for a in elem_dict]
    index_table = index_table_from_name_table(list(elem_dict.keys()), mul_tbl)
    return Group(nm, desc, list(elem_dict.keys()), index_table)


# See https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))


def generate_powerset_group(n, name=None, description=None):
    """Generates a group on the powerset of {0, 1, 2, ..., n-1},
    where symmetric difference is the operator."""
    if name:
        nm = name
    else:
        nm = "PS" + str(n)
    if description:
        desc = description
    else:
        desc = f"Autogenerated group on the powerset of {n} elements, with symmetric difference operator"
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    table = [[pset.index(a ^ b) for b in pset] for a in pset]
    elements = [str(elem) for elem in pset]
    elements[0] = "{}"  # Because otherwise it would be "set()"
    return Group(nm, desc, elements, table)


# ========
#   Ring
# ========

class Ring(Group):

    def __init__(self, *args):

        if len(args) == 5:
            super().__init__(*args[:4])

        self.ring_mult_table = np.array(args[4], dtype=np.int64)
        self.__has_mult_identity = None
        self.__mult_identity = None
        self.__is_distributive = None

        if not super().is_abelian():
            raise Exception("The ring addition operation is not abelian.")

        if not self.is_distributive():
            raise Exception("The ring addition operation does not distribute over multiplication.")

    @property
    def ring_elements(self):
        return super().elements

    @property
    def add_identity(self):
        return super().identity

    def add(self, *args):
        """Use the parent's (group) mult. operation as the ring's addition operator."""
        return super().op(*args)

    def ring_op(self, *args):

        if len(args) == 1:
            if args[0] in self.ring_elements:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid Group element name")
        elif len(args) == 2:
            row = self.ring_elements.index(args[0])
            col = self.ring_elements.index(args[1])
            index = self.ring_mult_table[row, col]
            return self.ring_elements[index]
        else:
            return functools.reduce(lambda a, b: self.ring_op(a, b), args)

    @property
    def mult_identity(self):
        """If it exists, find the identity element for the given operation, op.
        Developer Note: This value is computed, and if it exists, it is cached
        the first time it is accessed."""
        if self.__has_mult_identity is None:
            # Look for a multiplicative identity
            for x in self:
                xy = [self.ring_op(x, y) for y in self]
                if xy == self.ring_elements:
                    # Found one
                    self.__has_mult_identity = True
                    self.__mult_identity = x
                    return self.__mult_identity
            # Didn't find one
            if self.__has_mult_identity is None:
                self.__has_mult_identity = False
                return self.__mult_identity
        return self.__mult_identity

    @property
    def has_mult_identity(self):
        return self.__has_mult_identity

    def is_distributive(self, verbose=False):
        """Check that a(b + c) = ab + ac for all elements, in the Ring."""
        if self.__is_distributive is None:
            self.__is_distributive = True
            for a in self:
                for b in self:
                    for c in self:
                        b_plus_c = self.add(b, c)
                        ab = self.ring_op(a, b)
                        ac = self.ring_op(a, c)
                        if self.ring_op(a, b_plus_c) != self.add(ab, ac):
                            if verbose:
                                print(f"\na = {a}; b = {b}; c = {c}")
                                print(f"{a} x {b_plus_c} != {ab} + {ac}")
                            self.__is_distributive = False
                            break
            return self.__is_distributive
        else:
            return self.__is_distributive

    def ring_mult_table_with_names(self):
        return [[self.ring_elements[elem_pos]
                 for elem_pos in row]
                for row in self.ring_mult_table]

    def pprint(self, use_element_names=False):
        print(f"{self.__class__.__name__}('{self.name}',")
        print(f"'{self.description}',")
        if use_element_names:
            pp.pprint(self.table_as_list_with_names())
            pp.pprint(self.ring_mult_table_with_names())
        else:
            print(f"{self.ring_elements},")
            print("")
            pp.pprint(self.table.tolist())
            print("")
            pp.pprint(self.ring_mult_table.tolist())
        print(")")
        return None


def powerset_mult_table(n):
    """Return the multiplication table for the powerset of {0, 1, 2, ..., n-1},
    where intersection is the multiplication operation."""
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    return [[pset.index(a & b) for b in pset] for a in pset]


def generate_powerset_ring(n, name=None, description=None):
    """Generates a ring on the powerset of {0, 1, 2, ..., n-1},
    where symmetric difference is the operator."""
    if name:
        nm = name
    else:
        nm = "PSRing" + str(n)
    if description:
        desc = description
    else:
        desc = f"Autogenerated ring on powerset of {n} elements w/ ops: symm. diff. (+) & intersection (*)"
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    addition_table = [[pset.index(a ^ b) for b in pset] for a in pset]
    mult_table = powerset_mult_table(n)
    elements = [str(elem) for elem in pset]
    elements[0] = "{}"  # Because otherwise it would be "set()"
    return Ring(nm, desc, elements, addition_table, mult_table)


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
