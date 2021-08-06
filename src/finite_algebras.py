"""
@summary:  Finite Algebras: Magma, Semigroup, Monoid, Group, Ring, and Field
@author:   Alfred J. Reich, Ph.D.
@contact:  al.reich@gmail.com
@copyright: Copyright (C) 2021 Alfred J. Reich, Ph.D.
@license:  MIT
@requires: Python 3.7.7 or higher
@since:    2021.04
@version:  0.1.0
"""

import copy
import collections as co
import functools
import itertools as it
import json
import numpy as np
import os
import pprint as pp

from cayley_table import CayleyTable
from permutations import Perm


class Operator:
    """A callable class that implements a binary operation based on a Cayley table.
    It can be called with zero, one, or two (or more) arguments; and it will return
    the identity (if one exists; or None), the calling argument itself (if it's a
    valid element), or the sum of the two (or more) arguments, respectively."""

    def __init__(self, elements, identity, table):
        self.__elements = elements
        self.__identity = identity
        self.__table = table

    def __call__(self, *args):
        return self.__op(*args)

    def __binary_operation(self, elem1, elem2):
        """Returns the 'sum' of exactly two elements."""
        row = self.__elements.index(elem1)
        col = self.__elements.index(elem2)
        index = self.__table[row, col]
        return self.__elements[index]

    def __op(self, *args):
        if len(args) == 0:
            return self.__identity
        elif len(args) == 1:
            if args[0] in self.__elements:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid element name")
        elif len(args) == 2:
            return self.__binary_operation(args[0], args[1])
        else:
            return functools.reduce(lambda a, b: self.__op(a, b), args)


# =================
#   FiniteAlgebra
# =================

class FiniteAlgebra:
    """A top-level container class for functionality that is common to all finite algebras:
    THIS CLASS IS NOT INTENDED TO BE INSTANTIATED.  (It is not actually an algebra; it lacks
    a binary operation.)

    Class Hierarchy:
       FiniteAlgebra --> Magma --> Semigroup --> Monoid --> Group --> Ring --> Field
    """

    def __init__(self, name, description, elements, table):
        self.name = name
        self.description = description
        self.__elements = elements

        # Setup the multiplication table
        if isinstance(table, CayleyTable):
            self.__table = table
        else:
            self.__table = make_cayley_table(table, elements)

        # If it exists, setup the algebra's identity element
        id_index = self.table.identity()
        if id_index is not None:
            self.__identity = self.elements[id_index]
        else:
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
        nm, desc, elems, tbl = get_name_desc_elements_table(self)
        return f"{self.__class__.__name__}(\n'{nm}',\n'{desc}',\n{elems},\n{tbl}\n)"

    def __str__(self):
        return f"<{self.__class__.__name__}:{self.name}, ID:{id(self)}>"

    def deepcopy(self):
        """Returns a deep copy of this algebra."""
        return self.__class__(copy.deepcopy(self.name),
                              copy.deepcopy(self.description),
                              copy.deepcopy(self.elements),
                              copy.deepcopy(self.table.tolist()))

    @property
    def elements(self):
        """Returns the algebra's element names (list of strings)."""
        return self.__elements
    
    @property
    def table(self):
        """Returns the algebra's Cayley Table ('multiplication' table)."""
        return self.__table

    @property
    def identity(self):
        """Returns the algebra's identity element, if it exists; otherwise, it returns None."""
        return self.__identity

    @property
    def order(self):
        """Returns the order of the algebra."""
        return len(self.__elements)

    def table_as_list_with_names(self):
        """Returns the Cayley Table as a regular Python array where the element indices have been
        replaces by the element names (str)."""
        return [[self.__elements[index] for index in row] for row in self.__table.tolist()]

    def is_associative(self):
        """Returns True if the algebra is associative; returns False otherwise."""
        return self.__table.is_associative()

    def is_commutative(self):
        """Returns True if the algebra is commutative; returns False otherwise."""
        return self.__table.is_commutative()

    def is_abelian(self):
        """Returns True if the algebra is abelian; returns False otherwise."""
        return self.is_commutative()

    def has_inverses(self):
        """Returns True if every element in the algebra has an inverse that is also in the algebra;
        returns False otherwise."""
        return self.__table.has_inverses()

    def to_dict(self):
        """Returns a Python dictionary that represents the algebra."""
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'elements': self.__elements,
                'table': self.__table.tolist()
                }

    def dumps(self):
        """Returns a JSON string that represents the algebra."""
        return json.dumps(self.to_dict())

    def dump(self, json_filename):
        """Writes the algebra to the given filename in JSON format."""
        with open(json_filename, 'w') as fout:
            json.dump(self.to_dict(), fout)

    def about(self, max_size=12, use_table_names=False):
        """Prints out information about the algebra."""
        print(f"\n{self.__class__.__name__}: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"Elements: {self.elements}")
        if self.identity is None:
            print("Identity: None")
        else:
            print(f"Identity: {self.identity}")
        print(f"Associative? {yes_or_no(self.is_associative())}")
        print(f"Commutative? {yes_or_no(self.is_commutative())}")
        print(f"Has Inverses? {yes_or_no(self.has_inverses())}")
        size = len(self.elements)
        if size <= max_size:  # Don't print table if too large
            if use_table_names:
                print(f"Cayley Table (showing names):")
                pp.pprint(self.table_as_list_with_names())
            else:
                print(f"Cayley Table (showing indices):")
                pp.pprint(self.table.tolist())
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so the table is not output.")
        return None


# =========
#   Magma
# =========

class Magma(FiniteAlgebra):
    """A magma is a finite algebra with a binary operation that returns a unique value, in the algebra,
    for all pairs in the cross-product of the algebra's set of elements with itself.  With a binary
    operation we can compute the direct product of two or more algebras.  Also, we can check to see
    if two Magmas are isomorphic."""

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        self.op = Operator(self.elements, self.identity, self.table)
        self.__dp_delimiter = ':'  # name delimiter used when creating Direct Products

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
        return make_finite_algebra(dp_name,
                                   dp_description,
                                   list([f"{elem[0]}{self.__dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                                   dp_mult_table)

    def reorder_elements(self, reordered_elements):
        """Return a new group made from this one with the elements reordered."""
        n = self.order
        if n == len(reordered_elements):
            new_table = np.full((n, n), 0)
            for row in range(n):
                for col in range(n):
                    prod = self.op(reordered_elements[row], reordered_elements[col])
                    new_table[row, col] = reordered_elements.index(prod)
            new_name = str(self.name) + '_REORDERED'
            new_desc = str(self.description) + ' (elements reordered)'
            return self.__class__(new_name, new_desc, reordered_elements, new_table)
        else:
            raise ValueError(f"There are {len(reordered_elements)} reordered elements.  There should be {n}.")

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all
        possible permutations of other's elements.
        """
        return [dict(zip(self.elements, perm)) for perm in it.permutations(other.elements)]

    def isomorphic_mapping(self, other, mapping):
        """Returns True if the input mapping from this algebra to the other algebra is isomorphic."""
        return all([mapping[self.op(x, y)] == other.op(mapping[x], mapping[y])
                    for x in self.elements for y in self.elements])

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


# =============
#   Semigroup
# =============

class Semigroup(Magma):
    """A semigroup is an associative magma.  Not much else happens here.  But still,
    associativity is a pretty big deal."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table)
        if check_inputs:
            if not self.table.is_associative():
                raise ValueError("CHECK INPUTS: Table does not support associativity")


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):
    """A monoid is a semigroup with an identity element.  With an identity element
    we can compute element orders.  So, that happens here."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table, check_inputs)
        self.__element_orders = {elem: None for elem in self.elements}  # Cached on first access
        if check_inputs:
            if self.identity is None:
                raise ValueError("CHECK INPUTS: A monoid must have an identity element")

    def element_order(self, element):
        """Returns the order of the given element within the algebra."""
        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.op(prod, elem), order + 1)
        if self.__element_orders[element] is None:  # If not cached yet...
            self.__element_orders[element] = order_aux(element, element, 1)
        return self.__element_orders[element]

    # ---------------------
    # Monoid Isomorphisms
    # ---------------------

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all possible permutations
        of other's elements, where the identity of this algebra is always mapped to the identity of other."""
        if self.order == other.order:
            # Identities map to identities, so remove them
            id0 = self.identity
            id1 = other.identity
            elems0 = self.elements.copy()
            elems1 = other.elements.copy()
            elems0.remove(id0)
            elems1.remove(id1)
            # Compute all possible mappings
            mappings = [dict(zip(elems0, perm)) for perm in it.permutations(elems1)]
            # Add the identities back in
            for mapping in mappings:
                mapping[id0] = id1
            return mappings
        else:
            raise ValueError(f"Algebras must be of the same order: {self.order} != {other.order}")


# =========
#   Group
# =========

class Group(Monoid):
    """A group is a monoid with inverses."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table, check_inputs)
        if check_inputs:
            if self.table.has_inverses():
                self.__inverses = self.create_inverse_lookup_dict()
            else:
                raise ValueError("CHECK INPUTS: Table has insufficient inverses")
        else:
            self.__inverses = self.create_inverse_lookup_dict()

    def create_inverse_lookup_dict(self):
        """Returns a dictionary that maps each of the algebra's elements to its inverse element."""
        row_indices, col_indices = np.where(self.table.table == self.table.identity())
        return {self.elements[elem_index]: self.elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def inv(self, element):
        """Return the inverse of an element"""
        return self.__inverses[element]

    def conj(self, a, g):
        """Return g * a * inv(g), the conjugate of a with respect to g"""
        return self.op(g, self.op(a, self.inv(g)))

    def is_normal(self, subgrp):
        """Return True if the subgroup is normal."""
        result = True
        for x in self:
            for a in subgrp:
                if not self.conj(a, x) in subgrp:
                    result = False
                    break
        return result

    # TODO: Look into pushing closure and related functionality up the hierarchy

    def closure(self, subset_of_elements):
        """Given a subset (in list form) of the group's elements (name strings),
        return the smallest possible set of elements, containing the subset,
        that is closed under group multiplication, with inverses."""

        # Make sure inverses are considered
        result = set(subset_of_elements)
        for elem in subset_of_elements:
            result.add(self.inv(elem))

        # Add the products of all possible pairs
        for pair in it.product(result, result):
            result.add(self.op(*pair))

        # If the input set of elements increased, recurse ...
        if len(result) > len(subset_of_elements):
            return self.closure(list(result))

        # ...otherwise, stop and return the result
        else:
            return list(result)

    # TODO: Write a method, is_closed, using closure, above.  Use this method in the
    #       subgroup method, below.

    def closed_proper_subsets_of_elements(self):
        """Return all unique, closed, proper subsets of the Group's elements.
        This returns a list of lists. Each list represents the elements of a subgroup."""
        closed = set()  # Build the result as a set of sets to avoid duplicates
        all_elements = self.elements
        n = len(all_elements)
        for i in range(2, n - 1):  # avoids trivial closures, {'e'} & set of all elements
            # Look at all combinations of elements: pairs, triples, quadruples, etc.
            for combo in it.combinations(all_elements, i):
                clo = frozenset(self.closure(list(combo)))  # freezing required to add a set to a set
                if len(clo) < n:  # Don't include closures consisting of all elements
                    closed.add(clo)
        return list(map(lambda x: list(x), closed))

    def subgroup_from_elements(self, closed_subset_of_elements, name="No name", desc="No description"):
        """Return the Group constructed from the given closed subset of elements."""
        # Make sure the elements are sorted according to their order in the parent Group (self)
        # TODO: Check whether the input elements are indeed closed (make this check optional)
        #       Use the is_closed method (To Be Written) defined, above.
        elements_sorted = sorted(closed_subset_of_elements, key=lambda x: self.elements.index(x))
        table = []
        for a in elements_sorted:
            row = []
            for b in elements_sorted:
                # The table entry is the index of the product in the sorted elements list
                row.append(elements_sorted.index(self.op(a, b)))
            table.append(row)
        return Group(name, desc, elements_sorted, table)

    # TODO: Generalize the concept of subgroups to subalgebras and move it up the hierarchy.

    def proper_subgroups(self):
        """Return a list of proper subgroups of the group."""
        desc = f"Subgroup of: {self.description}"
        count = 0
        list_of_subgroups = []
        for closed_element_set in self.closed_proper_subsets_of_elements():
            name = f"{self.name}_subgroup_{count}"
            count += 1
            list_of_subgroups.append(self.subgroup_from_elements(closed_element_set, name, desc))
        return list_of_subgroups

    def trivial_subgroups(self):
        """Return the group's two trivial subgroups."""
        name = f"Subgroup of {self.name}"
        desc = f"Trivial subgroup: {self.description}"
        trivial = Group(name, desc, [self.identity], [[0]])
        return [trivial, self]

    def subgroups(self):
        """Return a list of all subgroups, including trivial subgroups."""
        return self.proper_subgroups() + self.trivial_subgroups()

    def unique_proper_subgroups(self, subgroups=None):
        """Return a list of proper subgroups that are unique, up to isomorphism.
        If no subgroups are provided, then they will be derived."""
        if subgroups:
            partitions = partition_into_isomorphic_lists(subgroups)
        else:
            partitions = partition_into_isomorphic_lists(self.proper_subgroups())
        # Return a list of the first subgroups from each sublist of proper subgroups
        return [partition[0] for partition in partitions]

    def about(self, max_size=12, use_table_names=False):
        """Print information about the Group."""
        print(f"\n{self.__class__.__name__}: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"Identity: {self.identity}")
        print(f"Associative? {yes_or_no(self.is_associative())}")
        print(f"Commutative? {yes_or_no(self.is_commutative())}")
        spc = 7
        print("Elements:")
        print("   Index   Name   Inverse  Order")
        for elem in self:
            idx_elem = self.elements.index(elem)
            inv_elem = self.inv(elem)
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

    # TODO: about_proper_subgroups is still a work-in-progress.  Finish it.
    def about_proper_subgroups(self, unique=False, show_elements=True):
        """Print info about proper subgroups of this group."""
        if unique:
            subgrps = self.unique_proper_subgroups()
        else:
            subgrps = self.proper_subgroups()
        print(f"\nSubgroups of {self.name}:")
        for subgrp in subgrps:
            print(f"\n  {subgrp.name}:")
            print(f"       order: {subgrp.order}")
            if show_elements:
                print(f"    elements: {subgrp.elements}")
            print(f"    abelian?: {subgrp.is_abelian()}")
            print(f"     normal?: {self.is_normal(subgrp)}")
        return None


# TODO: See if this can be applied higher up in the class hierarchy (e.g., to Magmas, perhaps)
def partition_into_isomorphic_lists(list_of_groups):
    """Partition the list of groups into sub-lists of groups that are isomorphic to each other.
    The purpose of this function is operate on the proper subgroups of a group to determine
    the unique subgroups, up to isomorphism."""

    def iso_and_not_iso(gp, gps):
        """Partition the list of groups, gps, into two lists, those that are isomorphic to gp
        and those that are not."""
        iso_to_grp = []
        not_iso_to_grp = []
        for g in gps:
            if gp.isomorphic(g):
                iso_to_grp.append(g)
            else:
                not_iso_to_grp.append(g)
        return iso_to_grp, not_iso_to_grp

    def aux(result, remainder):
        """Recursively partition 'remainder' into lists that are isomorphic to its first member of the
        remainder list and those that are not.  Then, put those that are isomorphic to the first member
        into the 'result' list, and recurse on the remainder."""
        if len(remainder) == 0:
            return result
        else:
            first = remainder[0]
            rest = remainder
            iso_to_first, not_iso_to_first = iso_and_not_iso(first, rest)
            result.append(iso_to_first)
            return aux(result, not_iso_to_first)

    return aux([], list_of_groups)


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
        desc = f"Autogenerated cyclic Group of order {order}"
    elements = [identity_name, elem_name] + [f"{elem_name}^" + str(i) for i in range(2, order)]
    table = [[((a + b) % order) for b in range(order)] for a in range(order)]
    return make_finite_algebra(nm, desc, elements, table)


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
        desc = f"Autogenerated symmetric Group on {n} elements"
    ident = tuple(range(base, n + base))
    perms = list(it.permutations(ident))
    elem_dict = {str(p): Perm(p) for p in perms}
    rev_elem_dict = {val: key for key, val in elem_dict.items()}
    mul_tbl = [[rev_elem_dict[elem_dict[a] * elem_dict[b]]
                for b in elem_dict]
               for a in elem_dict]
    index_table = index_table_from_name_table(list(elem_dict.keys()), mul_tbl)
    return make_finite_algebra(nm, desc, list(elem_dict.keys()), index_table)


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
        desc = f"Autogenerated Group on the powerset of {n} elements, with symmetric difference operator"
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    table = [[pset.index(a ^ b) for b in pset] for a in pset]
    elements = [str(elem) for elem in pset]
    elements[0] = "{}"  # Because otherwise it would be "set()"
    return make_finite_algebra(nm, desc, elements, table)


def generate_commutative_monoid(order, elem_name='a', name=None, description=None):
    """Generates a commutative monoid over {0,1,2,...,n-1}, where op(a,b) = (a * b) % n."""
    if name:
        nm = name
    else:
        nm = "M" + str(order)
    if description:
        desc = description
    else:
        desc = f"Autogenerated commutative Monoid of order {order}"
    elements = [elem_name + str(i) for i in range(order)]
    table = [[(a * b) % order for b in range(order)] for a in range(order)]
    return make_finite_algebra(nm, desc, elements, table)


# ========
#   Ring
# ========

class Ring(Group):
    """A Ring is a commutative Group with an 'addition' operator, along with an
    associative 'multiplication' operator, where addition distributes over
    multiplication."""

    def __init__(self, name, description, elements, table, table2, check_inputs=True):

        super().__init__(name, description, elements, table, check_inputs)

        if isinstance(table2, CayleyTable):
            self.__ring_mult_table = table2
        else:
            self.__ring_mult_table = CayleyTable(table2)

        self.__mult_identity = self.__ring_mult_table.identity()
        self.__ring_mult = Operator(self.elements, self.__mult_identity, self.__ring_mult_table)

        if check_inputs:
            if not super().is_commutative():
                raise ValueError(f"CHECK INPUTS: The ring addition operation is not commutative. {self}")
            if not self.__ring_mult_table.is_associative():
                raise ValueError(f"CHECK INPUTS: The ring multiplication operation is not associative. {self}")
            if not self.__ring_mult_table.distributes_over(self.table):
                raise ValueError(f"CHECK INPUTS: Multiplication does not distribute over addition. {self}")

    def __repr__(self):
        nm, desc, elems, tbl = get_name_desc_elements_table(self)
        tbl2 = self.mult_table.tolist()
        return f"{self.__class__.__name__}(\n'{nm}',\n'{desc}',\n{elems},\n{tbl},\n{tbl2}\n)"

    @property
    def add_identity(self):
        """Returns the additive identity element"""
        return self.identity

    @property
    def zero(self):
        """Another way to get the additive identity element"""
        return self.identity

    @property
    def mult_identity(self):
        """Returns the multiplicative identity element"""
        return self.__mult_identity

    @property
    def one(self):
        """Another way to get the multiplicative identity element"""
        return self.__mult_identity

    def has_mult_identity(self):
        """A convenience function, so that others don't have to check for 'not None'."""
        if self.mult_identity is not None:
            return True
        else:
            return False

    @property
    def add_table(self):
        """Returns the CayleyTable for addition."""
        return self.table

    @property
    def mult_table(self):
        """Returns the CayleyTable for multiplication"""
        return self.__ring_mult_table

    def add(self, *args):
        """Use the inherited group operator as the ring's addition operator."""
        return self.op(*args)

    def mult(self, *args):
        """Ring multiplication, based on the second table."""
        return self.__ring_mult(*args)

    # TODO: Combine this with the one that does the same thing for Groups and such.
    def ring_mult_table_with_names(self):
        return [[self.elements[elem_pos] for elem_pos in row] for row in self.__ring_mult_table.tolist()]

    def extract_additive_algebra(self):
        """A Ring's elements over addition, alone, should be a commutative Group.  This function
        returns that Group."""
        nm = f"{self.name}.Add"
        desc = f"Additive-only portion of {self.name}"
        return make_finite_algebra(nm, desc, self.elements, self.table.table)

    def extract_multiplicative_algebra(self):
        """A Ring's elements over multiplication, alone, should be a Semigroup.  This function
        returns that Semigroup."""
        nm = f"{self.name}.Mult"
        desc = f"Multiplicative-only portion of {self.name}"
        return make_finite_algebra(nm, desc, self.elements, self.mult_table.table)

    def about(self, max_size=12, use_table_names=False):
        """Print information about the Ring."""
        super().about(max_size, use_table_names)
        if self.mult_identity is not None:
            print(f"Mult. Identity: {self.elements[self.mult_identity]}")
        else:
            print(f"Mult. Identity: None")
        print(f"Mult. Commutative? {yes_or_no(self.mult_table.is_commutative())}")
        size = len(self.elements)
        if size <= max_size:
            if use_table_names:
                print(f"Multiplicative Cayley Table (showing names):")
                pp.pprint(self.ring_mult_table_with_names())
            else:
                print(f"Multiplicative Cayley Table (showing indices):")
                pp.pprint(self.mult_table.tolist())
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so no further info calculated/printed.")
        return None


def generate_commutative_ring(order, elem_name='a', name=None, description=None):
    """Generates a commutative ring over {0,1,2,...,n-1}, where addition and multiplication
    are over the integers modulo n."""
    if name:
        nm = name
    else:
        nm = "R" + str(order)
    if description:
        desc = description
    else:
        desc = f"Autogenerated commutative Ring of order {order}"
    elements = [elem_name + str(i) for i in range(order)]
    add_table =  [[(a + b) % order for b in range(order)] for a in range(order)]
    mult_table = [[(a * b) % order for b in range(order)] for a in range(order)]
    return make_finite_algebra(nm, desc, elements, add_table, mult_table)


# TODO: The tables here should be CayleyTables
def generate_powerset_ring(n, name=None, description=None):
    """Generates a ring on the powerset of {0, 1, 2, ..., n-1}, where n is a positive integer,
    symmetric difference is the addition operator, and intersection is the multiplication operator."""
    if name:
        nm = name
    else:
        nm = "PSRing" + str(n)
    if description:
        desc = description
    else:
        if n < 1:
            raise ValueError(f"n = {n} is invalid; n must be a positive integer")
        elif n == 1:
            desc = f"Autogenerated Ring on powerset of {{0}} w/ symm. diff. (add) & intersection (mult)"
        elif n == 2:
            desc = f"Autogenerated Ring on powerset of {{0, 1}} w/ symm. diff. (add) & intersection (mult)"
        elif n == 3:
            desc = f"Autogenerated Ring on powerset of {{0, 1, 2}} w/ symm. diff. (add) & intersection (mult)"
        else:
            desc = f"Autogenerated Ring on powerset of {{0,...,{n-1}}} w/ symm. diff. (add) & intersection (mult)"
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    addition_table = [[pset.index(a ^ b) for b in pset] for a in pset]
    mult_table = [[pset.index(a & b) for b in pset] for a in pset]
    elements = [str(elem) for elem in pset]
    elements[0] = '{}'  # Because 'set()' doesn't look cool
    return make_finite_algebra(nm, desc, elements, addition_table, mult_table)


# ---------------------------------
#         EXPERIMENTAL
# Find all groups of a given order
# ---------------------------------

def __no_conflict(p1, p2):
    """Returns True only if no element of p1 equals the corresponding element of p2."""
    return all([p1[i] != p2[i] for i in range(len(p1))])


def __no_conflicts(items):
    """Return True if each possible pair, from a list of items, has no conflicts."""
    return all(__no_conflict(combo[0], combo[1]) for combo in it.combinations(items, 2))


def __filter_out_conflicts(perms, perm, n):
    """Filter out all permutations in perms that conflict with perm,
    and don't have n as the first element."""
    nperms = [q for q in perms if q[0] == n]
    return [p for p in nperms if __no_conflict(p, perm)]


def generate_all_group_tables(order):
    """Experimental Code: Return a list of all arrays that correspond to multiplication tables for groups
    of a specific order.

    WARNING: The algorithm here is not efficient, so even very small values of 'order' will result in very
    long runtimes (e.g., order=6 ==> ~5-6 hrs runtime).
    """
    row0 = list(range(order))
    row_candidates = [[row0]]
    for row_num in range(1, order):
        row_candidates.append(__filter_out_conflicts(it.permutations(row0), row0, row_num))
    table_candidates = [cand for cand in it.product(*row_candidates) if is_table_associative(list(cand))]  # ***
    return [tbl for tbl in table_candidates if __no_conflicts(tbl)]


# TODO: Reconcile this version with the similar method in CayleyTable.
def is_table_associative(table):
    """Tests whether a table supports associativity

    Parameters
    ----------
    table : np.array
      A list of lists of ints, representing a group's table

    Returns
    -------
    bool
      True if the table supports associativity; False, otherwise
    """
    result = True
    elements = table[0]  # The first row should correspond to the elements of a group
    for a in elements:
        for b in elements:
            for c in elements:
                ab = table[a][b]
                bc = table[b][c]
                if not (table[ab][c] == table[a][bc]):
                    result = False
                    break
    return result


def tables_to_groups(tables, identity_name="e", elem_name="a"):
    """Given a list of multiplication tables, all of the same size, turn them into a list of groups."""
    order = len(tables[0])
    groups = []
    for j in range(len(tables)):
        gname = f"G{j}"
        desc = f"Group {j} of order {order}"
        ename = elem_name + str(j) + "_"
        elements = [identity_name + str(j)] + [f"{ename}" + str(i) for i in range(1, order)]
        groups.append(Group(gname, desc, elements, tables[j]))
    return groups


def get_integer_form(elem_list):
    """For an element list like ['e1', 'a1_2', 'a1_1', 'a1_3'],
    return the integer 213, i.e., the 'subscripts' of the elements that
    follow the identity element."""
    return int(''.join(map(lambda x: x.split("_")[1], elem_list[1:])))


def get_int_forms(ref_group, isomorphisms):
    """Return a list of integer forms ('permutations') for a list of isomorphisms,
    i.e., mappings, based on a reference group."""
    return [get_integer_form([iso[elem] for elem in ref_group.elements])
            for iso in isomorphisms]


# =========
#   Field
# =========

# TODO: Implement Field
class Field(Ring):
    """WRITE ME"""
    pass


# =====================
# Make Finite Algebra
# =====================

def make_finite_algebra(*args):
    """Analyzes the input table and returns the appropriate finite algebra.

    A finite algebra consists of four items: name (str), description (str),
    elements (list of str), and table (list of lists of int/str).

    This function either takes all four items in the order described, above,
    or a single JSON file name, or a single Python dictionary, where the latter
    two contain definitions of the four items.

    See the examples in the documentation.
    """

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
                       'elements': args[2],
                       'table': args[3]
                       }

    elif len(args) == 5:

        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'elements': args[2],
                       'table': args[3],
                       'table2': args[4]
                       }
    else:
        raise ValueError("Incorrect number of input arguments.")

    name = finalg_dict['name']
    desc = finalg_dict['description']
    elems = finalg_dict['elements']
    tbl = finalg_dict['table']

    # Check for duplicate element names
    dups = get_duplicates(elems)
    if len(dups) == 0:
        pass
    else:
        raise ValueError(f"Duplicate element names: {dups}")

    table = make_cayley_table(tbl, elems)

    table2 = None
    is_assoc2 = False
    if 'table2' in finalg_dict:
        table2 = make_cayley_table(finalg_dict['table2'], elems)
        is_assoc2 = table2.is_associative()

    is_assoc = table.is_associative()
    has_id = table.identity()
    if has_id is not None:
        inverses = table.has_inverses()
    else:
        inverses = None

    if is_assoc:
        if has_id is not None:
            if inverses:
                if table2 is not None and is_assoc2:
                    return Ring(name, desc, elems, table, table2, check_inputs=False)
                else:
                    return Group(name, desc, elems, table, check_inputs=False)
            else:
                return Monoid(name, desc, elems, table, check_inputs=False)
        else:
            return Semigroup(name, desc, elems, table, check_inputs=False)
    else:
        return Magma(name, desc, elems, table)


# ==========
# Utilities
# ==========

def get_name_desc_elements_table(finalg):
    name = finalg.name
    description = finalg.description
    elements = finalg.elements
    table_as_list = finalg.table.tolist()
    return name, description, elements, table_as_list


def make_cayley_table(table, elements):
    """Return a CayleyTable from a table of indices or a table of strings."""
    if isinstance(table[0][0], str):
        index_table = index_table_from_name_table(elements, table)
        ct = CayleyTable(index_table)
    else:
        ct = CayleyTable(table)
    return ct


def index_table_from_name_table(elements, name_table):
    return [[elements.index(elem_name) for elem_name in row] for row in name_table]


def get_duplicates(lst):
    """Return a list of the duplicate items in the input list."""
    return [item for item, count in co.Counter(lst).items() if count > 1]


def yes_or_no(true_or_false):
    if true_or_false:
        return "Yes"
    else:
        return "No"


# See https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))


def make_table(table_string):
    """This function helps turn the XML-based tables at https://groupprops.subwiki.org/wiki/Main_Page
    into a list of lists for use here.

    Instructions for use:
    1. Copy the table from there and paste it here;
    2. Find & Replace the strings, "<row>" and "</row>", with nothing;
    3. Place triple quotes around the result and give it a variable name;
    4. Then run make_table on the variable.

    Parameters
    ----------
    table_string : str
      XML-based table at https://groupprops.subwiki.org/wiki/Main_Page

    Returns
    -------
    list
      A list of lists of ints, representing a group's multiplication table.
    """
    return [[int(n) for n in row.strip().split(" ")]
            for row in table_string.splitlines()]


class Examples:
    """A convenience class for accessing some of the example algebras in the algebras
    directory.  To add or subtract algebras to its default list, see the file,
    'examples.json', in the algebras directory."""

    def __init__(self, algebras_dir, filenames_json='examples.json'):
        examples_path = os.path.join(algebras_dir, filenames_json)
        with open(examples_path, 'r') as fin:
            self.filenames_list = json.load(fin)
        self.algebras = [make_finite_algebra(os.path.join(algebras_dir, filename))
                         for filename in self.filenames_list]
        self.about()

    def get_example(self, index):
        return self.algebras[index]

    def about(self):
        n = 70
        print("=" * n)
        print(" " * (int(n / 2) - 8) + "Example Algebras")  # centered
        print("-" * n)
        print(f"  {len(self.algebras)} example algebras are available.")
        print("  Use \"get_example(INDEX)\" to get a specific example,")
        print("  where INDEX is the first number on each line below:")
        print("-" * n)
        index = 0
        for alg in self.algebras:
            print(f"{index}: {alg.name} -- {alg.description}")
            index += 1
        print("=" * n)


# End of File
