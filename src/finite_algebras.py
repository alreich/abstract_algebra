"""
@summary:  Finite Algebras: Magma, Semigroup, Monoid, Group, Ring, Field, Module, VectorSpace
@author:   Alfred J. Reich, Ph.D.
@contact:  al.reich@gmail.com
@copyright: Copyright (C) 2021 Alfred J. Reich, Ph.D.
@license:  MIT
@requires: Python 3.7.7 or higher
@since:    2021.04
@version:  0.1.0
"""

import copy
import collections
from functools import reduce
import itertools as it
import json
import numpy as np
import scipy.sparse as sp
import os
import pprint as pp
import re

from sympy.ntheory import isprime
from my_math import divisors, relative_primes
from cayley_table import CayleyTable
from permutations import Perm
from abstract_matrix import AbstractMatrix
# from abc import ABC


class FiniteOperator:
    """A callable class that implements a binary operation based on a multiplication
    table (i.e., Cayley table).  Although intended for use as the binary operation
    of a finite algebra (e.g., Group operation), the implementation here can be called
    with zero, one, two, or more arguments (similar to how arithmetic operators work in
    Lisp).

    If no arguments are provided, it will return the identity element if it exists;
    otherwise it will return None.  e.g., op() ==> e | None

    If only one argument is provided, it will check whether the argument is a valid
    element of the algebra, and if so, return the same value, otherwise it will
    raise an exception.  e.g., op(a) ==> a | ValueError

    If two arguments are provided, it will return their 'product'.
    e.g., op(a, b) ==> ab

    If more than two arguments are provided, it will return their product by associating
    left-to-right. e.g., op(a, b, c, d) = (((ab)c)d). The order of association is
    only important for a Magma, because it is the only non-associative algebraic structure
    supported here.
    """

    def __init__(self, elements, identity, table):
        self._elements = elements
        self._identity = identity
        self._table = table

    def __call__(self, *args):
        return self._op(*args)

    def _binary_operation(self, elem1, elem2):
        """Returns the 'sum' of exactly two elements."""
        row = self._elements.index(elem1)
        col = self._elements.index(elem2)
        index = self._table[row, col]
        return self._elements[index]

    def _op(self, *args):
        if len(args) == 0:
            return self._identity
        elif len(args) == 1:
            if args[0] in self._elements:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid element name")
        elif len(args) == 2:
            return self._binary_operation(args[0], args[1])
        else:
            return reduce(lambda a, b: self._op(a, b), args)


# =================
#   FiniteAlgebra
# =================

class FiniteAlgebra:
    """The top-level class for all algebras in this module.
    THIS CLASS IS NOT INTENDED TO BE INSTANTIATED.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class SingleElementSetAlgebra(FiniteAlgebra):
    """A top-level container class for functionality that is common to all finite algebras
    that only have one set of elements. THIS CLASS IS NOT INTENDED TO BE INSTANTIATED.
    """

    def __init__(self, name, description, elements, table):
        super().__init__(name, description)
        self._elements = tuple(elements)
        self._inverses = dict()

        # Set up the multiplication table
        if isinstance(table, CayleyTable):
            self._table = table
        else:
            self._table = make_cayley_table(table, elements)

        # If it exists, setup the algebra's identity element
        id_index = self.table.identity()
        if id_index is not None:
            self._identity = self.elements[id_index]
        else:
            self._identity = None

    def __contains__(self, element):
        return element in self._elements

    def __getitem__(self, index):
        return self._elements[index]

    def __repr__(self):
        nm, desc, elems, tbl = unpack_components(self)
        return f"{self.__class__.__name__}(\n'{nm}',\n'{desc}',\n{elems},\n{tbl}\n)"

    def __str__(self):
        return f"<{self.__class__.__name__}:{self.name}, ID:{id(self)}>"

    # deepcopy is deprecated
    # def deepcopy(self):
    #     """Returns a deep copy of this algebra."""
    #     return self.__class__(copy.deepcopy(self.name),
    #                           copy.deepcopy(self.description),
    #                           copy.deepcopy(self.elements),
    #                           copy.deepcopy(self.table.tolist()))

    def copy_algebra(self, new_elements=(), new_name=False, new_description=False):
        """Creates a copy of the input algebra where, optionally, the existing element
        list can be replaced by a new element list. Same for the name & description.
        If there is a new element list, then it must be a list of strings and have
        the same length as the existing one.
        """
        if new_name:
            name = new_name
        else:
            name = copy.deepcopy(self.name)

        if new_description:
            desc = new_description
        else:
            desc = copy.deepcopy(self.description)

        if len(new_elements) != 0:
            if all(map(lambda x: isinstance(x, str), new_elements)):
                if len(set(new_elements)) == self.order:
                    elems = new_elements
                else:
                    raise ValueError(f"New element set must be same size as existing one.")
            else:
                raise ValueError(f"All elements must be strings.")
        else:
            elems = copy.deepcopy(self.elements)

        if isinstance(self, Ring):
            return make_finite_algebra(name, desc, elems,
                                       copy.deepcopy(self.table.tolist()),
                                       copy.deepcopy(self.mult_table.tolist()))
        else:
            return make_finite_algebra(name, desc, elems,
                                       copy.deepcopy(self.table.tolist()))

    @property
    def elements(self):
        """Returns the algebra's element names (list of strings)."""
        return self._elements

    def element_map(self):
        """Instantiates an Element for each element name and returns a dictionary, where
         the element names are keys and corresponding Elements are the values. This method
         is used within the context manager, InfixNotation, to perform arithmetic using
         infix notation."""
        return {elem: Element(elem, self) for elem in self.elements}

    @property
    def table(self):
        """Returns the algebra's Cayley Table ('multiplication' table)."""
        return self._table

    @property
    def identity(self):
        """Returns the algebra's identity element if it exists; otherwise, it returns None."""
        return self._identity

    def has_identity(self):
        """A convenience function that returns True or False, depending on whether the algebra
        has an identity element."""
        if self.identity is None:
            return False
        else:
            return True

    @property
    def order(self):
        """Returns the order of the algebra."""
        return len(self._elements)

    def is_associative(self):
        """Returns True if the algebra is associative; returns False otherwise."""
        return self._table.is_associative()

    def is_commutative(self):
        """Returns True if the algebra is commutative; returns False otherwise."""
        return self._table.is_commutative()

    def is_abelian(self):
        """Returns True if the algebra is abelian; returns False otherwise."""
        return self.is_commutative()

    def has_inverses(self):
        """Returns True if every element in the algebra has an inverse that is also in the algebra;
        returns False otherwise."""
        return self._table.has_inverses()

    def inv(self, element):
        """Return the inverse of an element"""
        if self.has_inverses():
            if element in self._inverses:
                return self._inverses[element]
            else:
                return None
        else:
            return None

    def to_dict(self, include_classname=False):
        """Returns a dictionary that represents the algebra.  The dictionary
        can be fed back into make_finite_algebra, and it will return a copy of
        this algebra."""
        result = {'name': self.name,
                  'description': self.description,
                  'elements': self.elements,
                  'table': self.table.tolist()
                  }
        if isinstance(self, Ring):
            result['table2'] = self.mult_table.tolist()
            if self.conjugates() is not None:
                result['conj_map'] = self.conjugates()
        if include_classname:
            result['type'] = self.__class__.__name__
        return result

    def dumps(self):
        """Returns a JSON string that represents the algebra."""
        return json.dumps(self.to_dict())

    def dump(self, json_filename):
        """Writes the algebra to the given filename in JSON format."""
        with open(json_filename, 'w') as fout:
            json.dump(self.to_dict(), fout)


# =========
#   Magma
# =========

class Magma(SingleElementSetAlgebra):
    """A Magma is a finite algebra with a binary operation that returns a unique value, in the algebra,
    for all pairs in the cross-product of the algebra's set of elements with itself.  With a binary
    operation, we can compute the direct product of two or more algebras.  Also, we can check to see
    if two Magmas are isomorphic."""

    def __init__(self, name, description, elements, table):
        super().__init__(name, description, elements, table)
        self.op = FiniteOperator(self.elements, self.identity, self.table)
        self._dp_delimiter = ':'  # name delimiter used when creating Direct Products

    def _key(self):
        return tuple([self.elements, self.table.tolist()])

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        if isinstance(other, Magma):
            return self._key() == other._key()
        else:
            return NotImplemented

    def direct_product_delimiter(self, delimiter=None):
        """If no input, then the current direct product element name delimiter will be returned (default is ':').
        Otherwise, if a string is input (e.g., "-") it will become the new delimiter for direct product element
        names, and then it will be returned."""
        if delimiter:
            self._dp_delimiter = delimiter
            return self._dp_delimiter
        else:
            return self._dp_delimiter

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
                                   list([f"{elem[0]}{self._dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                                   dp_mult_table)

    def __pow__(self, n, modulo=None):
        """Return the direct product of this algebra with itself, n times.
        Ignore the modulo argument for algebras."""
        result = self
        if isinstance(n, int) and n > 0:
            for _ in range(n - 1):
                result = result * self
        else:
            raise ValueError(f"n = {n}, but the power must be a positive integer.")
        return result

    def element_to_power(self, elem, n, left_associative=True):
        """Return the n_th power of the given element. n must be an integer. If n == 0 and an
        identity element exists, then it will be returned; otherwise, a ValueError is raised.
        If n < 0, and the algebra has inverses, then the inverse of the element raised to the
        absolute value of the power is returned, e.g., b^-4 = inv(b^4). If n < 0 and the algebra
        does not have inverses, then a ValueError is raised. For non-associative algebras (Magmas),
        the default is for products to be associated from the left, e.g., b^4 = ((b * b) * b) * b.
        Set left_associative to False, to associate from the right, instead."""
        result = elem
        if elem in self.elements:
            if isinstance(n, int):  # Or, raise an exception if not an integer
                if n == 0:
                    if self.has_identity():  # Or, raise an exception if no identity exists
                        result = self.identity
                    else:
                        raise ValueError(f"n = {n}. But, {self.name} does not have an identity element.")
                elif n > 0:
                    for _ in range(n - 1):
                        if left_associative:
                            result = self.op(result, elem)
                        else:
                            result = self.op(elem, result)
                elif n < 0:  # Or, raise an exception if inverses do not exist
                    if self.has_inverses():
                        result = self.inv(self.element_to_power(elem, abs(n), left_associative))
                    else:
                        raise ValueError(f"n = {n}. But, {self.name} does not have inverses.")
            else:
                raise ValueError(f"n = {n}. The power must be an integer.")
        else:
            raise ValueError(f"{elem} is not an element of {self.name}.")
        return result

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
            return self.__class__(new_name, new_desc, tuple(reordered_elements), new_table)
        else:
            raise ValueError(f"There are {len(reordered_elements)} reordered elements.  There should be {n}.")

    def _element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all
        possible permutations of other's elements.  The orders of self and other must
        be equal."""
        return [dict(zip(self.elements, perm)) for perm in it.permutations(other.elements)]

    def _isomorphic_mapping(self, other, mapping):
        """Returns True if the input mapping from this algebra to the other algebra is isomorphic."""
        return all([mapping[self.op(x, y)] == other.op(mapping[x], mapping[y])
                    for x in self.elements for y in self.elements])

    def isomorphic(self, other):
        """If there is a mapping from elements of this algebra to the other algebra's elements,
        return it; otherwise return False."""
        if (self.__class__.__name__ == other.__class__.__name__) and (self.order == other.order):
            maps = self._element_mappings(other)
            for mp in maps:
                if self._isomorphic_mapping(other, mp):
                    return mp
            return False
        else:
            return False

    def closure(self, subset_of_elements, include_inverses):
        """Given a subset (in list form) of the group's elements (name strings),
        return the smallest possible set of elements containing the subset
        that is closed under the algebra's operation(s).  If include_inverses
        is True and the algebra has inverses, then they will be added to the
        closure."""

        result = set(subset_of_elements)

        # Include inverses, maybe.
        if include_inverses and self.has_inverses():
            for elem in subset_of_elements:
                result.add(self.inv(elem))

        # Add the products (sums, if rings) of all possible pairs
        for pair in it.product(result, result):
            result.add(self.op(*pair))

        # For rings, add the products of all possible pairs
        if isinstance(self, Ring):
            for pair in it.product(result, result):
                result.add(self.mult(*pair))

        # If the input set of elements increased, recurse ...
        if len(result) > len(subset_of_elements):
            return self.closure(list(result), include_inverses)

        # ...otherwise, stop and return the result
        else:
            return list(result)

    def closed_subsets_of_elements(self, divisors_only, include_inverses):
        """Return all unique, closed, proper subsets of the algebra's elements.
        This returns a list of lists. Each list represents the elements of a subalgebra.
        If divisors_only is True, then only subalgebras of orders that are divisors of
        self will be examined."""
        closed = set()  # Build the result as a set of sets to avoid duplicates
        all_elements = self.elements
        n = len(all_elements)
        if divisors_only:
            range_ = divisors(n, non_trivial=True)
        else:
            range_ = range(2, n - 1)
        for i in range_:
            # Look at all combinations of elements: pairs, triples, quadruples, etc.
            for combo in it.combinations(all_elements, i):
                # Freezing is required to add a set to a set
                clo = frozenset(self.closure(list(combo), include_inverses))
                if len(clo) < n:  # Don't include closures consisting of all elements
                    closed.add(clo)
        return list(map(lambda x: list(x), closed))

    def subalgebra_from_elements(self, closed_subset_of_elements, name="No name", desc="No description"):
        """Return the algebra constructed from the given closed subset of elements."""
        # Make sure the elements are sorted according to their order in the parent Group (self)
        elements_sorted = sorted(closed_subset_of_elements, key=lambda x: self.elements.index(x))
        table = []
        for a in elements_sorted:
            row = []
            for b in elements_sorted:
                # The table entry is the index of the product in the sorted elements list
                row.append(elements_sorted.index(self.op(a, b)))
            table.append(row)
        if isinstance(self, Ring):
            table2 = []
            for c in elements_sorted:
                row2 = []
                for d in elements_sorted:
                    # The table entry is the index of the product in the sorted elements list
                    row2.append(elements_sorted.index(self.mult(c, d)))
                table2.append(row2)
            return make_finite_algebra(name, desc, elements_sorted, table, table2)
        else:
            return make_finite_algebra(name, desc, elements_sorted, table)

    def proper_subalgebras(self, divisors_only=True, include_inverses=True):
        """Return a list of proper subalgebras of the algebra."""
        desc = f"Subalgebra of: {self.description}"
        count = 0
        list_of_subalgebras = []
        for closed_element_set in self.closed_subsets_of_elements(divisors_only, include_inverses):
            name = f"{self.name}_subalgebra_{count}"
            count += 1
            list_of_subalgebras.append(self.subalgebra_from_elements(closed_element_set, name, desc))
        return list_of_subalgebras

    def generates(self, set_of_elems):
        """Returns True if a set of one or more elements generates the algebra,
        otherwise False is returned.
        """
        clo = self.closure(set_of_elems, include_inverses=False)
        return set(clo) == set(self.elements)

    # TODO: Review this method and the is_cyclic method for issues (see notebook)
    def generators(self, start_of_range=1):
        """If the algebra is cyclic, then a list of individual elements that each
        generate the algebra is returned; otherwise, a list of lists of elements,
        is returned, where each sublist generates the algebra."""
        gens = list()
        n = None  # define n outside the scope of the loop below
        for k in range(start_of_range, self.order):
            n = k  # Save for test later
            combos = list(it.combinations(self.elements, k))
            stop = False
            for combo in combos:
                if self.generates(combo):
                    gens.append(combo)
                    stop = True
            if stop:
                break
        if n == 1:
            return [gen[0] for gen in gens]  # The grp is cyclic
        else:
            return gens  # The grp is not cyclic

    def is_cyclic(self):
        """Returns False if this algebra is not cyclic; otherwise a list of elements
        is returned, where each one can generate the entire algebra."""
        elemset = set(self.elements)
        gens = [x for x in elemset if set(self.closure([x], False)) == elemset]
        if len(gens) == 0:
            return False
        else:
            return gens

    def center(self):
        """Return the list of elements that commute with every element of the algebra.
        In Pinter's book, chapter 5, exercise D3, the 'center' is defined for Groups,
        but the definition also works for any Magma."""
        return [a for a in self if all([self.op(a, x) == self.op(x, a) for x in self])]

    def center_algebra(self, verbose=False):
        """Return the subalgebra that is the center of this algebra.  If the center is part of a
        Semigroup, then (due to associativity) it will be closed wrt the Semigroup operation,
        and hence form a sub-semigroup, but the center of a Magma will not necessarily be closed.
        Note also that, if the algebra is commutative, then the entire algebra is its center."""
        ctr = self.center()

        if len(ctr) == 0:  # If there is no center...
            if verbose:
                print(f"{self} does not have a Center.")
            return None

        # Being lazy (or careful) and checking closure, regardless of the type of algebra
        elif set(ctr) == set(self.closure(ctr, False)):
            return self.subalgebra_from_elements(ctr, self.name + '_CENTER', 'Center of ' + self.name)
        else:
            if verbose:
                print(f"The Center of {self} is not closed.")
            return None

    def is_division_algebra(self, verbose=False):
        """Return True if, for every a & b in the algebra, there is an x and y in the algebra
        such that ax=b and ya=b. Otherwise, return False.  If False is returned, and you need to
        see why, set verbose to True and look for 'fail' in the output."""
        if verbose:
            print(f"\n{self}\n")
        result = True
        elems = self.elements
        for ab in it.product(elems, elems):
            ab_ok = False
            for xy in it.product(elems, elems):
                a = ab[0]
                b = ab[1]
                x = xy[0]
                y = xy[1]
                if self.op(a, x) == b and self.op(y, a) == b:
                    if verbose:
                        print(f"{ab} & {xy}")
                    ab_ok = True
                    break
            if not ab_ok:
                result = False
                if verbose:
                    print(f"{ab} fail")
        return result

    def _element_pairs_where_table_equals(self, cayley_table, elem_name):
        """Utility function that returns all pairs of elements where the cayley_table entries
         are equal to elem."""
        elems = self.elements
        index = elems.index(elem_name)
        pairs = cayley_table.table_entries_where_equal_to(index)
        return [(elems[pair[0]], elems[pair[1]]) for pair in pairs]

    def element_pairs_where_sum_equals(self, elem_name):
        """Return all pairs of elements where the sums are equal to elem_name. The 'sum' here
        refers to the binary operation of a Magma, Semigroup, Group, or to the additive binary
        operation of a Ring or Field.
        """
        return self._element_pairs_where_table_equals(self.table, elem_name)

    def left_cosets(self, subalgebra):
        """Returns an iterator that returns lists of left cosets."""
        return map(lambda s: sorted(list(s)),
                   {frozenset([self.op(x, y) for y in subalgebra])
                    for x in self})

    def right_cosets(self, subalgebra):
        """Returns an iterator that returns lists of right cosets."""
        return map(lambda s: sorted(list(s)),
                   {frozenset([self.op(y, x) for y in subalgebra])
                    for x in self})

    # This 'about' method differs from the one in Groups in that it does not print out
    # as much detailed information about elements.
    # TODO: Combine the 'about' method, below, with the one in Groups.
    def about(self, max_size=12, max_gens=2, use_table_names=False, show_tables=True, show_elements=True,
              show_generators=False):
        """Prints out information about the algebra. Tables larger than
        max_size are not printed out."""
        print(f"\n** {self.__class__.__name__} **")
        print(f"Name: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"Order: {self.order}")
        if self.identity is None:
            print("Identity: None")
        else:
            print(f"Identity: {self.identity}")
        print(f"Associative? {yes_or_no(self.is_associative())}")
        print(f"Commutative? {yes_or_no(self.is_commutative())}")
        # is_cyclic, gens = self.generators()
        single_gens = self.is_cyclic()
        if single_gens:
            print("Cyclic?: Yes")
            print(f"Generators: {single_gens}")
        else:
            print("Cyclic?: No")
            if show_generators:
                gens = self.generators(2)
                num_gens = len(gens)
                gens_sorted = sorted(gens)
                if num_gens > max_gens:
                    print(f"Generators: {gens_sorted[:max_gens]}, plus {num_gens - max_gens} more.")
                elif num_gens == 0:
                    print("Generators: None")
                else:
                    print(f"Generators: {gens_sorted}")
        if show_elements:
            print(f"Elements: {self.elements}")
        print(f"Has Inverses? {yes_or_no(self.has_inverses())}")
        size = len(self.elements)
        if show_tables:
            if size <= max_size:  # Don't print table if too large
                if use_table_names:
                    print(f"Cayley Table (showing names):")
                    pp.pprint(self.table.to_list_with_names(self.elements))
                else:
                    print(f"Cayley Table (showing indices):")
                    pp.pprint(self.table.tolist())
            else:
                print(f"{self.__class__.__name__} order is {size} > {max_size}, so the table is not output.")
        return None

    # The following three methods (sub, mult, & div) are stubbed out here to eliminate
    # warnings from the Element class regarding them not being defined for Magma.

    def sub(self, x, y):
        raise NotImplementedError(f"{self.__class__.__name__} sub cannot be implemented.")

    def mult(self, x, y):
        raise NotImplementedError(f"{self.__class__.__name__} mult cannot be implemented.")

    def div(self, x, y):
        raise NotImplementedError(f"{self.__class__.__name__} div cannot be implemented.")


# =============
#   Semigroup
# =============

class Semigroup(Magma):
    """A Semigroup is an associative Magma."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table)
        if check_inputs:
            if not self.table.is_associative():
                raise ValueError("CHECK INPUTS: Table does not support associativity")

    def is_regular(self):
        """Returns True if for all elements, a, there exists an element, x, such that axa=a.
        Otherwise, False is returned."""
        return all([any([self.op(self.op(a, x), a) == a for x in self]) for a in self])

    def weak_inverses(self):
        """Returns a dictionary of weak inverses, where each key is one of the algebra's
        elements and its value is a list of its weak inverses.  If the algebra is
        regular, then there will be at least 1 weak inverse for each element. Otherwise,
        some elements may not have a weak inverse."""
        return {a: [x for x in self if self.op(self.op(a, x), a) == a] for a in self}


# ==========
#   Monoid
# ==========

class Monoid(Semigroup):
    """A Monoid is a Semigroup with an identity element.  With an identity element,
    we can compute element orders.  So, that happens here."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table, check_inputs)
        self._element_orders = {elem: 0 for elem in self.elements}  # Cached on first access
        if check_inputs:
            if self.identity is None:
                raise ValueError("CHECK INPUTS: A monoid must have an identity element")

    def element_order(self, element) -> int:
        """Returns the order of the given element within the algebra."""

        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.op(prod, elem), order + 1)

        if self._element_orders[element] != 0:  # if already cached, return value
            return self._element_orders[element]
        else:  # else if not cached, compute it, cache it, and return value
            self._element_orders[element] = order_aux(element, element, 1)
            return self._element_orders[element]

    def units(self, return_names=True):
        """Return a sorted list of the Monoid's units.
        By default, the names of elements are returned.
        Setting 'return_names' to False will return element indices instead.
        NOTE: This method is used to compute the units of a Ring.
        """
        # Find the xy-pairs whose product is the Monoid's identity element
        xs, ys = np.where(self.table.table == self.elements.index(self.identity))
        xy_pairs = list(zip(xs, ys))  # e.g., [(1, 2), (2, 1), (5,3), (7, 4), (4, 7)]

        # Collect all x for (x,y) in xy_pairs, if (y,x) is also in xy_pairs
        # e.g., [(1, 2), (2, 1), (5,3), (7, 4), (4, 7)] ==> [1, 2, 4, 7]
        unit_indices = sorted(list({xy[0] for xy in xy_pairs if (xy[1], xy[0]) in xy_pairs}))
        if return_names:
            return [self.elements[index] for index in unit_indices]
        else:
            return unit_indices

    def units_subgroup(self):
        """Return the Unit Subgroup of this algebra.  Makes sense for Monoids or Rings, where
        the multiplicative portion of the Ring is a Monoid.  It will also work for Groups and
        Fields, but will return the entire Group or the entire multiplicative Group of a Field.
        """
        nm = f"{self.name}_Units"
        description = f"Unit subgroup of {self.__class__.__name__}: {self.name}"

        monoid = self
        if isinstance(self, Ring):
            monoid = self.extract_multiplicative_algebra()

        return monoid.subalgebra_from_elements(monoid.units(), name=nm, desc=description)

    def regular_representation(self, sparse=""):
        """Given a group, this function returns four things: (1) A dictionary that maps each group
        element to its corresponding regular representation, (2) A (reverse) dictionary that maps each
        regular representation (in the form of a tuple of tuples) back to its corresponding group element,
        (3) A function that maps a group element to its corresponding regular representation matrix, and
        (4) Another function that maps in the opposite direction, from regular representation matrix to
        group element. By default, the matrices are dense arrays. SciPy sparse arrays can be output instead,
        by setting the input variable, "sparse", to one of the following seven strings: "BSR", "COO", "CSC",
        "CSR", "DIA", "DOK", or "LIL". Each of the seven strings corresponds to one of the seven classes of
        sparse array supported by SciPy.
        """
        A = self.elements
        N = self.order

        # Create a list of N Nx1 orthogonal unit vectors
        ident = np.eye(N, dtype=int)  # The NxN identity matrix
        # noinspection PyPep8Naming
        B = [ident[:, [i]] for i in range(N)]  # A list of columns extracted from the identity matrix

        # Create a dictionary that maps group elements to the column vectors created above.
        mapping = dict(zip(A, B))

        # Create a function that takes a group element and returns the corresponding Nx1
        # orthogonal unit vector.
        def V(elem):
            return mapping[elem]

        # Turn a column vector into a tuple, for use as a dict key
        def vector_to_tuple(vec):
            return tuple(map(lambda x: x[0], list(vec)))

        # map vectors to group elements
        inv_mapping = {vector_to_tuple(val): key for key, val in mapping.items()}

        # Given one of the Nx1 orthogonal unit vectors, return the corresponding group element
        def Vinv(vec):
            return inv_mapping[vector_to_tuple(vec)]

        # The seven SciPy sparse array class constructors
        sparse_array_classes = {
            "BSR": sp.bsr_array,
            "COO": sp.coo_array,
            "CSC": sp.csc_array,
            "CSR": sp.csr_array,
            "DIA": sp.dia_array,
            "DOK": sp.dok_array,
            "LIL": sp.lil_array}

        # Create a dictionary that maps each group element to its corresponding
        # regular representation (NxN) matrix.
        reg_rep = dict()
        for k in range(N):
            c_k = np.zeros((N, N))
            for i in range(N):
                for j in range(N):
                    c_k[i][j] = np.dot(B[i].transpose(), V(self.op(A[k], Vinv(B[j]))))
            if sparse in sparse_array_classes:
                reg_rep[A[k]] = sparse_array_classes[sparse](c_k, dtype=int)
            else:
                reg_rep[A[k]] = c_k

        # Create a function that takes a group element and returns the corresponding regular
        # representation matrix, using the dictionary created above.
        def element_to_array(elem):
            return reg_rep[elem]

        # Create a function that turns a 2-dimensional nd.array into a tuple of tuples,
        # for use as a dictionary key. This works for both dense and sparse arrays.
        def array_to_tuple(arr):
            return tuple(zip(*arr.nonzero()))

        # Create a reverse dictionary that maps each regular representation matrix (in tuple form)
        # to its corresponding group element.
        inv_reg_rep = {array_to_tuple(arr): key for key, arr in reg_rep.items()}

        # Create a function that takes a regular representation matrix and returns the corresponding
        # group element, using the reverse dictionary created above.
        def array_to_element(arr):
            return inv_reg_rep[array_to_tuple(arr)]

        return reg_rep, inv_reg_rep, element_to_array, array_to_element

    def verify_regular_representation(self, elem_to_arr, arr_to_elem):
        """Verifies that the regular representation satisfies the two requirements of it. This requires
        that the regular representation use dense matrices, NOT sparse matrices.
        """
        return ((self.identity == arr_to_elem(np.eye(self.order, dtype=int)))  # e == Vinv( identity_matrix )
                and
                # V(a) x V(b) == V(a * b)
                all([np.array_equal(np.dot(elem_to_arr(a), elem_to_arr(b)), elem_to_arr(self.op(a, b)))
                     for a in self
                     for b in self]))

    # ---------------------
    # Monoid Isomorphisms
    # ---------------------

    def _element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this algebra's elements to all possible permutations
        of other's elements, where the identity of this algebra is always mapped to the identity of other."""
        if self.order == other.order:
            # Identities map to identities, so remove them
            id0 = self.identity
            id1 = other.identity
            # elems0 = self.elements.copy()
            elems0copy = tuple(self.elements)
            # elems1 = other.elements.copy()
            elems1copy = tuple(other.elements)
            # elems0.remove(id0)
            list(elems0copy).remove(id0)
            # elems1.remove(id1)
            list(elems1copy).remove(id1)
            # Compute all possible mappings
            mappings = [dict(zip(elems0copy, perm)) for perm in it.permutations(elems1copy)]
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
    """A Group is a Monoid with inverses."""

    def __init__(self, name, description, elements, table, check_inputs=True):
        super().__init__(name, description, elements, table, check_inputs)
        if check_inputs:
            if self.table.has_inverses():
                self._inverses = self._create_inverse_lookup_dict()
            else:
                raise ValueError("CHECK INPUTS: Table has insufficient inverses")
        else:
            self._inverses = self._create_inverse_lookup_dict()

    def __truediv__(self, normal_subgroup):
        """Return the quotient group based on a given normal subgroup.

        Each element of the quotient group will be a representative element from
        one of the subgroup's cosets."""
        return self.quotient_group(normal_subgroup)

    def _create_inverse_lookup_dict(self):
        """Returns a dictionary that maps each of the algebra's elements to its inverse element."""
        row_indices, col_indices = np.where(self.table.table == self.table.identity())
        return {self.elements[elem_index]: self.elements[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def inverse_mapping(self):
        """Returns a dictionary that maps each element to its inverse."""
        return self._inverses

    def inv(self, element):
        """Return the inverse of an element"""
        return self._inverses[element]

    def sub(self, x, y):
        """Group subtraction:  Return x - y; i.e., x + inv(y)."""
        return self.op(x, self.inv(y))

    def conjugate(self, a, g):
        """Return g * a * inv(g), the conjugate of a with respect to g"""
        return self.op(g, self.op(a, self.inv(g)))

    def commutator(self, a, b):
        """Return [a, b] = a * b * inv(a) * inv(b), the commutator of a & b"""
        return self.op(a, b, self.inv(a), self.inv(b))

    def commutators(self):
        """Return the list of commutators of the group."""
        result = set()
        for a in self:
            for b in self:
                result.add(self.commutator(a, b))
        return result

    def commutator_subalgebra(self):
        """Return the commutator subalgebra (Group, Ring, or Field) of this Group, Ring, or Field."""
        commutators = self.commutators()
        return self.subalgebra_from_elements(self.closure(commutators, include_inverses=True),
                                             name=f"{self.name}_Comm",
                                             desc=f"{self.name} commutator subalgebra")

    def is_normal(self, subgrp):
        """Returns True if the subgroup is normal, otherwise False is returned"""
        result = True
        for x in self:
            for a in subgrp:
                if not self.conjugate(a, x) in subgrp:
                    result = False
                    break
        return result

    def trivial_subgroups(self):
        """Return the group's two trivial subgroups."""
        name = f"Subgroup of {self.name}"
        desc = f"Trivial subgroup: {self.description}"
        trivial = Group(name, desc, [self.identity], [[0]])
        return [trivial, self]

    def subgroups(self):
        """Return a list of all subgroups, including trivial subgroups."""
        return self.proper_subalgebras(divisors_only=True, include_inverses=True) + self.trivial_subgroups()

    def unique_proper_subgroups(self, subgroups=None):
        """Return a list of proper subgroups that are unique, up to isomorphism.
        If no subgroups are provided, then they will be derived."""
        if subgroups:
            partitions = partition_into_isomorphic_lists(subgroups)
        else:
            partitions = partition_into_isomorphic_lists(self.proper_subalgebras(divisors_only=True,
                                                                                 include_inverses=True))
        # Return a list of the first subgroups from each sublist of proper subgroups
        return [partition[0] for partition in partitions]

    def quotient_group(self, subgroup):
        """Given a normal subgroup, return the quotient group of this group.
        The elements of the quotient group will be representative elements from
        cosets, prefixed with '~'."""

        def index_of_coset(elem, _cosets):
            """Given an element of an algebra and a list of cosets, find the position of the coset
            that contains the element in the list of cosets."""
            index = None
            for coset in _cosets:
                if elem in coset:
                    index = _cosets.index(coset)
            return index

        if self.is_normal(subgroup):
            cosets = list(self.left_cosets(subgroup))
        else:
            raise ValueError(f"{subgroup.name} is not a normal subgroup of {self.name}")

        # Make a list consisting of one representative element from each coset
        elems = [x[0] for x in cosets]
        n = len(elems)
        table = np.zeros((n, n))
        for b in elems:
            b_index = elems.index(b)
            for a in elems:
                a_index = elems.index(a)
                axb = self.op(a, b)
                axb_index = index_of_coset(axb, cosets)
                table[a_index][b_index] = axb_index

        name = f"{self.name}/{subgroup.name}"
        desc = f"Group {self.name} modulo subgroup {subgroup.name}"
        coset_elems = tuple("~" + elem for elem in elems)
        return make_finite_algebra(name, desc, coset_elems, table)

    # This 'about' method differs from the one in SingleElementSetAlgebra in that it prints out
    # more detailed information about elements.
    # TODO: It would be nice to combine the two someday.
    def about(self, max_size=12, max_gens=2, use_table_names=False, show_tables=True, show_elements=True,
              show_generators=False):
        """Print information about the Group."""
        print(f"\n** {self.__class__.__name__} **")
        print(f"Name: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"Order: {self.order}")
        print(f"Identity: {repr(self.identity)}")
        print(f"Commutative? {yes_or_no(self.is_commutative())}")
        single_gens = self.is_cyclic()
        if single_gens:
            print("Cyclic?: Yes")
            print(f"Generators: {single_gens}")
        else:
            print("Cyclic?: No")
            if show_generators:
                gens = self.generators(2)
                num_gens = len(gens)
                gens_sorted = sorted(gens)
                if num_gens > max_gens:
                    print(f"Generators: {gens_sorted[:max_gens]}, plus {num_gens - max_gens} more.")
                elif num_gens == 0:
                    print("Generators: None")
                else:
                    print(f"Generators: {gens_sorted}")
        spc = 7
        if show_elements:
            print("Elements:")
            print("   Index   Name   Inverse  Order")
            for elem in self:
                idx_elem = self.elements.index(elem)
                inv_elem = self.inv(elem)
                ord_elem = self.element_order(elem)
                # repr is used below to make strings explicit by printing out their quotation marks.
                print(f"{idx_elem :>{spc}} {repr(elem) :>{spc}} {repr(inv_elem) :>{spc}} {ord_elem :>{spc}}")
        size = len(self.elements)
        if show_tables:
            if size <= max_size:
                if use_table_names:
                    print(f"Cayley Table (showing names):")
                    pp.pprint(self.table.to_list_with_names(self.elements))
                else:
                    print(f"Cayley Table (showing indices):")
                    pp.pprint(self.table.tolist())
            else:
                print(f"{self.__class__.__name__} order is {size} > {max_size}, so no table is printed.")
        return str(self)


def partition_into_isomorphic_lists(list_of_groups):
    """Partition the list of groups into sub-lists of groups that are isomorphic to each other.
    The purpose of this function is to operate on the proper subgroups of a group to determine
    the unique subgroups, up to isomorphism.
    """
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
        into the 'result' list, and recurse on the remainder.
        """
        if len(remainder) == 0:
            return result
        else:
            first = remainder[0]
            rest = remainder
            iso_to_first, not_iso_to_first = iso_and_not_iso(first, rest)
            result.append(iso_to_first)
            return aux(result, not_iso_to_first)

    return aux([], list_of_groups)


def about_isomorphic_partition(alg, part):
    """Print a summary of a particular partition of isomorphic subalgebras of an algebra.
    """
    size = len(part)

    # All the algebras in a partition are isomorphic to each other,
    # so, get (most) properties from the first algebra in the partition
    sub0 = part[0]
    classname = f"{sub0.__class__.__name__}"
    order = sub0.order

    comm = "Isomorphic "
    comm1 = ""
    if sub0.is_commutative():
        comm = "Isomorphic Commutative "
        comm1 = "Commutative "

    # See if there are different identity elements for each algebra in the partition
    identities = False
    single_id = False
    if sub0.has_identity():
        identities = {sub.identity for sub in part}
        if len(identities) == 1:
            single_id = sub0.identity

    norm = ""
    if alg.has_inverses() and alg.is_normal(sub0):
        norm = "Normal "

    if size > 1:
        if identities:
            if single_id:
                print(f"{size} {comm}{norm}{classname}s of order {order} with identity '{single_id}':")
                for sub in part:
                    sub_cname = sub.__class__.__name__
                    print(f"      {sub_cname}: {sub.name}: {sub.elements}")
                print("")
            else:
                print(f"{size} {comm}{norm}{classname}s of order {order}:")
                for sub in part:
                    sub_cname = sub.__class__.__name__
                    print(f"      {sub_cname}: {sub.name}: {sub.elements} with identity '{sub.identity}'")
                print("")
        else:
            print(f"{size} {comm}{norm}{classname}s of order {order}:")
            for sub in part:
                sub_cname = sub.__class__.__name__
                print(f"      {sub_cname}: {sub.name}: {sub.elements}")
            print("")
    elif size == 1:
        if identities:
            print(f"{size} {comm1}{norm}{classname} of order {order} with identity '{sub0.identity}':")
        else:
            print(f"{size} {comm1}{norm}{classname} of order {order}:")
        sub0_cname = sub0.__class__.__name__
        print(f"      {sub0_cname}: {sub0.name}: {sub0.elements}\n")
    else:
        raise ValueError("A partition must have at least one member.")


def are_n(n):
    """A bit of grammar.  This function returns a string with the appropriate
    singular or plural present indicative form of 'to be', along with 'n'.
    """
    choices = ['are no', 'is 1', f'are {n}']
    if n < 2:
        return choices[n]
    else:
        return choices[2]


def add_s(string, n):
    """Make a string plural by adding an 's' to it, or not, depending on 'n'."""
    if n == 1:
        return string
    else:
        return string + 's'


def about_isomorphic_partitions(alg, partitions):
    """Print a summary of the isomorphic partitions of an algebra."""
    if len(partitions) != 0:
        n_subs = reduce(lambda x, y: x + y, [len(p) for p in partitions])
        n_parts = len(partitions)
        print(f"\nSubalgebras of {alg}")
        what = f"  There {are_n(n_parts)} unique proper {add_s('subalgebra', n_parts)}, up to isomorphism, "
        out_of = f"out of {n_subs} total subalgebras."
        print(what + out_of)
        print(f"  as shown by the partitions below:\n")
        for partition in partitions:
            about_isomorphic_partition(alg, partition)
    else:
        print("There are no proper subalgebras.")


def about_subalgebras(alg):
    """A convenience function that finds and summarizes all proper subalgebras
    of the input SingleElementSetAlgebra.  The list of isomorphic partitions is
    returned and a summary of it is printed out.
    """
    alg_subs = alg.proper_subalgebras()
    partitions = partition_into_isomorphic_lists(alg_subs)
    about_isomorphic_partitions(alg, partitions)
    return partitions


# def left_cosets(group, subgroup):
#     """Returns an iterator that returns lists of left cosets."""
#     return map(lambda s: sorted(list(s)),
#                {frozenset([group.op(x, y) for y in subgroup])
#                 for x in group})
#
# def right_cosets(group, subgroup):
#     """Returns an iterator that returns lists of right cosets."""
#     return map(lambda s: sorted(list(s)),
#                {frozenset([group.op(y, x) for y in subgroup])
#                 for x in group})

# -----------------
# Group Generators
# -----------------


def generate_cyclic_group(order, elem_name='', name=None, description=None, zfill=False):
    """Generates a cyclic group with the given order. If zfill is True, then left fill element
    names with zeros."""
    if name:
        nm = name
    else:
        nm = "Z" + str(order)
    if description:
        desc = description
    else:
        desc = f"Autogenerated cyclic Group of order {order}"
    if zfill:
        nfill = len(str(order - 1))  # Number of zeros to left-fill integers in element names
        elements = [elem_name + str(i).zfill(nfill) for i in range(order)]
    else:
        elements = [elem_name + str(i) for i in range(order)]
    table = [[((a + b) % order) for b in range(order)] for a in range(order)]
    return make_finite_algebra(nm, desc, elements, table)


# def generate_symmetric_group(n, name=None, description=None, base=1):
#     """Generates a symmetric group on n elements. The 'base' is a non-negative integer
#     (typically, 0 or 1), so permutations will be tuples, like (1, 2, 3, ..., n), where
#     n is the order, or (0, 1, 2, ..., n-1).
#     """
#     if name:
#         nm = name
#     else:
#         nm = "S" + str(n)
#     if description:
#         desc = description
#     else:
#         desc = f"Autogenerated symmetric Group on {n} elements"
#     ident = tuple(range(base, n + base))
#     perms = list(it.permutations(ident))
#     elem_dict = {str(p): Perm(p) for p in perms}
#     rev_elem_dict = {val: key for key, val in elem_dict.items()}
#     mul_tbl = [[rev_elem_dict[elem_dict[a] * elem_dict[b]]
#                 for b in elem_dict]
#                for a in elem_dict]
#     index_table = index_table_from_name_table(list(elem_dict.keys()), mul_tbl)
#     return make_finite_algebra(nm, desc, list(elem_dict.keys()), index_table)

def generate_symmetric_group(n, name=None, description=None, alternating=False):
    """Generates a symmetric or alternating group on n elements."""
    if alternating:
        txt = ["A", "alternating"]
    else:
        txt = ["S", "symmetric"]
    if name:
        nm = name
    else:
        nm = txt[0] + str(n)
    if description:
        desc = description
    else:
        desc = f"Autogenerated {txt[1]} Group on {n} elements"
    ident = tuple(range(n))
    mappings = list(it.permutations(ident))
    perms = map(lambda x: Perm(x), mappings)
    if alternating:
        elem_dict = {str(p): p for p in perms if p.is_even}
        # elem_dict = {str(p): Perm(p) for p in perms if Perm(p).is_even}
    else:
        elem_dict = {str(p): p for p in perms}
        # elem_dict = {str(p): Perm(p) for p in perms}
    rev_elem_dict = {val: key for key, val in elem_dict.items()}
    mul_tbl = [[rev_elem_dict[elem_dict[a] * elem_dict[b]]
                for b in elem_dict]
               for a in elem_dict]
    index_table = index_table_from_name_table(list(elem_dict.keys()), mul_tbl)
    return make_finite_algebra(nm, desc, list(elem_dict.keys()), index_table)


def generate_powerset_group(n, name=None, description=None):
    """Generates a group on the powerset of {0, 1, 2, ..., n-1},
    where symmetric difference is the operator.
    """
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
    nfill = len(str(order - 1))  # Number of zeros to left-fill integers in element names
    elements = [elem_name + str(i).zfill(nfill) for i in range(order)]
    table = [[(a * b) % order for b in range(order)] for a in range(order)]
    return make_finite_algebra(nm, desc, elements, table)


def generate_relative_primes_group(n, name=None, description=None):
    """Generates a group based on mult mod n of relatively-prime numbers < n.
    In keeping with the convention in this module, the elements are converted to strings."""
    if name:
        nm = name
    else:
        nm = "RelPrimes<" + str(n)
    if description:
        desc = description
    else:
        desc = f"Autogenerated group based on relative primes < {n}"
    elems = relative_primes(n)
    elem_dict = dict(zip(elems, range(len(elems))))  # rel_prime : index_in_elem_list
    table = [[elem_dict[(a * b) % n] for b in elems] for a in elems]
    elems_as_str = [str(elem) for elem in elems]
    return make_finite_algebra(nm, desc, elems_as_str, table)


# ========
#   Ring
# ========

class Ring(Group):
    """A Ring is a commutative Group with an 'addition' operator, along with an
    associative 'multiplication' operator, where multiplication distributes over
    addition.  The operator inherited from Group becomes 'addition', while
    'multiplication' is defined by table2."""

    def __init__(self, name, description, elements, table, table2, check_inputs=True,
                 conjugate_mapping=None):

        super().__init__(name, description, elements, table, check_inputs)

        self._conjugates = conjugate_mapping

        if isinstance(table2, CayleyTable):
            self._ring_mult_table = table2
        else:
            self._ring_mult_table = make_cayley_table(table2, elements)

        # If it exists, set up the Ring's multiplicative identity element
        mult_id_index = self._ring_mult_table.identity()
        if mult_id_index is not None:
            self._mult_identity = self.elements[mult_id_index]
        else:
            self._mult_identity = None

        self._ring_mult = FiniteOperator(self.elements, self._mult_identity, self._ring_mult_table)

        if check_inputs:
            if not super().is_commutative():
                raise ValueError(f"CHECK INPUTS: The ring addition operation is not commutative. {self}")
            if not self._ring_mult_table.is_associative():
                raise ValueError(f"CHECK INPUTS: The ring multiplication operation is not associative. {self}")
            if not self._ring_mult_table.distributes_over(self.table):
                raise ValueError(f"CHECK INPUTS: Multiplication does not distribute over addition. {self}")

    def __repr__(self):
        nm, desc, elems, tbl, tbl2, conjmap = unpack_components(self)
        if conjmap is not None:
            return f"{self.__class__.__name__}(\n'{nm}',\n'{desc}',\n{elems},\n{tbl},\n{tbl2},\n{conjmap}\n)"
        else:
            return f"{self.__class__.__name__}(\n'{nm}',\n'{desc}',\n{elems},\n{tbl},\n{tbl2}\n)"

    def __mul__(self, other):  # Direct Product of two Rings
        """Return direct product of this Ring with the `other` Ring."""
        if not isinstance(other, Ring):
            raise ValueError(f"{other.name} must be a Ring")
        dp_name = f"{self.name}_x_{other.name}"
        dp_description = "Direct product of " + self.name + " & " + other.name
        dp_element_names = list(it.product(self.elements, other.elements))  # Cross product
        dp_add_table = list()
        dp_mul_table = list()
        for a in dp_element_names:
            dp_add_table_row = list()  # Start new rows in the add and mult tables
            dp_mul_table_row = list()
            for b in dp_element_names:
                dp_add_table_row.append(dp_element_names.index((self.add(a[0], b[0]),
                                                                other.add(a[1], b[1]))))
                dp_mul_table_row.append(dp_element_names.index((self.mult(a[0], b[0]),
                                                                other.mult(a[1], b[1]))))
            dp_add_table.append(dp_add_table_row)  # Append the new rows to each table
            dp_mul_table.append(dp_mul_table_row)
        return make_finite_algebra(dp_name,
                                   dp_description,
                                   list([f"{elem[0]}{self.direct_product_delimiter()}{elem[1]}"
                                         for elem in dp_element_names]),
                                   dp_add_table,
                                   dp_mul_table)

    def _key(self):
        return tuple([self.elements, self.table.tolist(), self._ring_mult_table.tolist()])

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        if isinstance(other, Ring):
            return self._key() == other._key()
        else:
            return NotImplemented

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
        """Returns the multiplicative identity element, if it exists.
        If it doesn't exist, then None is returned."""
        return self._mult_identity

    @property
    def one(self):
        """Another way to get the multiplicative identity element"""
        return self._mult_identity

    def has_mult_identity(self):
        """A convenience function that returns True or False, depending on whether the algebra
        has a multiplicative identity element, in addition to its additive identity element."""
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
        return self._ring_mult_table

    def add(self, *args):
        """Use the inherited group operator as the ring's addition operator."""
        return self.op(*args)

    def mult(self, *args):
        """Ring multiplication, based on the second table."""
        return self._ring_mult(*args)

    def element_to_power(self, elem, n, left_associative=True):
        """Overrides the Magma method by the same name, so that we use
        the multiplication operation of the Ring to raise an element to
        a power.
        """
        mult_alg = self.extract_multiplicative_algebra()
        return mult_alg.element_to_power(elem, n, left_associative)

    def mult_is_commutative(self):
        """By definition, Ring addition is commutative, but Ring multiplication only needs to be
        associative.  This method tells us whether multiplication is commutative for this Ring."""
        return self.mult_table.is_commutative()

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

    # TODO: Write a method that returns non-zero pairs whose product is zero
    def zero_divisors(self):
        """Return the Ring's zero divisors. i.e., if neither a nor b are 0, but a*b == 0, then
        a and b are zero divisors."""

        # Get the index of the additive identity element ("zero")
        zero_index = self.elements.index(self.zero)

        # Delete the zero element's row & column in the multiplication table.
        # (NOTE: This operation leaves the original mult. table unchanged.)
        mult_table_without_add_id = delete_row_col(self.mult_table.table, zero_index, zero_index)

        # Get the row & column indices where the product equals "zero" in the remaining table
        a, b = list(map(lambda x: set(x), np.where(mult_table_without_add_id == zero_index)))
        #
        # Return all elements corresponding to the union of the row & column indices
        return [self.elements[index + 1] for index in list(a | b)]

    def units(self, return_names=True, verbose=False):
        """Return a list of the Ring's units."""
        mult_alg = self.extract_multiplicative_algebra()
        if mult_alg.has_identity():
            return mult_alg.units(return_names)
        else:
            if verbose:
                print(f"There is no multiplicative identity element.")
            return None

    def commutator(self, a, b):
        """Return [a, b] = (a * b) - (b * a), the ring commutator of a & b"""
        return self.sub(self.mult(a, b), self.mult(b, a))

    def element_pairs_where_product_equals(self, elem_name):
        """Return all pairs of elements where the product is equal to elem_name.
        """
        return self._element_pairs_where_table_equals(self.mult_table, elem_name)

    def zero_divisor_pairs(self):
        """Return a list of pairs of elements, neither one of which is zero, but whose
        product is zero.
        """
        zero_product_pairs = self.element_pairs_where_product_equals(self.identity)
        # return [pair for pair in zero_product_pairs if not self.identity in pair]
        return [pair for pair in zero_product_pairs if self.identity not in pair]

    def about(self, max_size=12, max_gens=2, use_table_names=False, show_tables=True, show_elements=True,
              show_conjugates=False, show_generators=False):
        """Print information about the Ring."""
        super().about(max_size, max_gens, use_table_names, show_tables, show_elements, show_generators)

        if self.mult_identity is not None:
            print(f"Mult. Identity: {repr(self.mult_identity)}")
        else:
            print(f"Mult. Identity: None")

        print(f"Mult. Commutative? {yes_or_no(self.mult_is_commutative())}")

        zero_divisors = self.zero_divisors()
        if len(zero_divisors) == 0:
            print("Zero Divisors: None")
        else:
            print(f"Zero Divisors: {zero_divisors}")

        size = len(self.elements)

        if show_tables:
            if size <= max_size:
                if use_table_names:
                    print(f"Multiplicative Cayley Table (showing names):")
                    pp.pprint(self._ring_mult_table.to_list_with_names(self.elements))
                else:
                    print(f"Multiplicative Cayley Table (showing indices):")
                    pp.pprint(self.mult_table.tolist())
            else:
                print(f"{self.__class__.__name__} order is {size} > {max_size}, so the mult. table is not printed.")

        # The conjugate mapping is only printed out if it exists, and we want to see it.
        if show_conjugates and self.conjugates() is not None:
            print(f"Conjugate Mapping: {self.conjugates()}")

        return None

    # ========================================================================
    # The following methods implement the Cayley-Dickson construction/algebra
    # ========================================================================

    def sqr(self):  # My original version of the Cayley-Dickson construction/algebra
        """The Cayley-Dickson construction/algebra. Returns the direct product of this Ring
        with itself, where multiplication is defined as: (a, b) * (c, d) = (ac - bd, ad + bc)
        """
        dp_name = f"{self.name}_SQR"
        dp_description = "Direct product of " + self.name + " with itself using complex multiplication"
        dp_element_names = list(it.product(self.elements, self.elements))  # Cross product
        dp_add_table = list()
        dp_mul_table = list()
        for a in dp_element_names:
            dp_add_table_row = list()  # Start new rows in the add and mult tables
            dp_mul_table_row = list()
            for b in dp_element_names:
                dp_add_table_row.append(dp_element_names.index((self.add(a[0], b[0]),
                                                                self.add(a[1], b[1]))))
                # (a[0], a[1]) * (b[0], b[1])
                #     = (a[0]b[0] - a[1]b[1], a[0]b[1] + a[1]b[0])
                dp_mul_table_row.append(dp_element_names.index(((self.sub(self.mult(a[0], b[0]),
                                                                          self.mult(a[1], b[1]))),
                                                                (self.add(self.mult(a[0], b[1]),
                                                                          self.mult(a[1], b[0]))))))
            dp_add_table.append(dp_add_table_row)  # Append the new rows to each table
            dp_mul_table.append(dp_mul_table_row)
        return make_finite_algebra(dp_name,
                                   dp_description,
                                   list([f"{elem[0]}{self.direct_product_delimiter()}{elem[1]}"
                                         for elem in dp_element_names]),
                                   dp_add_table,
                                   dp_mul_table)

    def split_element(self, element):
        """If the element is a compound element created by a direct product or the Cayley-Dickson
        construction, then it contains at least one delimiter (e.g., '1:2' or '1:2:3:4').
        This method splits the element at the middle delimiter and returns the two pieces
        (e.g., '1', '2' or '1:2', '3:4').  If the element is not a compound element, then
        it is returned unchanged.
        """
        delimiter = self.direct_product_delimiter()
        if delimiter in element:
            matches = list(re.finditer(delimiter, element))
            mid = matches[len(matches) // 2]
            return element[:mid.start()], element[mid.end():]
        else:
            return element

    def is_gaussian_prime(self, elem):
        """This method only works for elements of Rings or Fields created by the function,
        'generate_algebra_mod_n', or by a single application of the Ring method,
        'make_cayley_dickson_algebra', to the output of 'generate_algebra_mod_n'.
        That is, elements that look like 7 or 07:12.
        """
        delim = self.direct_product_delimiter()
        dimension = elem.count(delim)
        if dimension == 0:
            real = elem
            imag = 0
        elif dimension == 1:
            a, b = elem.split(delim)
            real = int(a)
            imag = int(b)
        else:
            raise ValueError(f"The dimension of {elem} is too high.")
        if real == 0:
            return isprime(imag) and imag % 4 == 3
        elif imag == 0:
            return isprime(real) and real % 4 == 3
        return isprime(real ** 2 + imag ** 2)

    def scalar_mult(self, scalar_name, elem_name):
        """ Scalar multiplication. 'a' * 'c:d' = 'a*c:a*d'
        Example: scalar_mult('2', '1:2', F3) ==> '2:1'
        """
        delimiter = self.direct_product_delimiter()
        scalarx = delimiter.join([scalar_name, self.zero[0]])  # eg: '2' --> '2:0'
        return self.mult(scalarx, elem_name)

    def elem_conj(self, elem):
        """For use only when making a Cayley-Dickson algebra.
        """
        delim = self.direct_product_delimiter()
        if delim in elem:
            a, b = self.split_element(elem)
            return delim.join([self.conj(a), self.inv(b)])
        else:
            return elem

    def conjugates(self):
        """Return the dictionary that maps elements to their conjugate values.
        If it's None, then the element is its own conjugate."""
        return self._conjugates

    def conj(self, elem):
        """Given an element name, return the element name of its conjugate value."""
        if self._conjugates is None:
            return elem
        else:
            return self._conjugates[elem]

    def norm(self, elem):
        """Return the product of the input element and its conjugate."""
        return self.mult(elem, self.conj(elem))

    def make_cayley_dickson_algebra(self, mu=None, version=1):
        """Constructs the Cayley-Dickson algebra using this Ring or Field.

        Several different versions of multiplication are supported:
        version=1: (DEFAULT) No mu & no conjugation are used
        version=2: Definition in Schafer, 1966
        version=3: Definition in Schafer, 1954
        version=4: Definition in Baez, 2001.

        See the documentation on readthedocs for more information regarding versions.

        Versions 2 & 3 require a value for mu. If mu is None (the default), then mu
        will be automatically set to be the additive inverse of the Ring's
        multiplicative identity element (i.e., "-1") if it exists. If it does not
        exist, then an exception will be raised.
        """
        if mu is None:
            if self.has_mult_identity():
                mu = self.inv(self.one)  # The additive inverse of the multiplicative identity
            else:
                if version == 2 or version == 3:
                    raise ValueError(f"Without a mult. identity, version {version} requires a specific value for mu")
        else:  # mu is not None
            if mu in self.elements:
                if version == 1 or version == 4:
                    print(f"** Version {version} ignores the value of mu. (mu = {mu})")
                    mu = None
            else:
                raise ValueError(f"mu = {mu} is not an element of {self.name}.")

        if version == 1:
            vers = "no mu and no conjugation were used."
            name_suffix = "_CDA_2024"
        elif version == 2:
            vers = f"mu = {mu}, Schafer 1966 version."
            name_suffix = "_CDA_1966"
        elif version == 3:
            vers = f"mu = {mu}, Schafer 1954 version."
            name_suffix = "_CDA_1954"
        elif version == 4:
            vers = f"mu = {mu}, Baez 2001 version."
            name_suffix = "_CDA_2001"
        else:
            raise ValueError(f"{version} is not a valid version #. Use 1, 2, or 3.")

        name = f"{self.name}{name_suffix}"
        description = f"Cayley-Dickson algebra based on {self.name}, where {vers}"
        element_names = list(it.product(self.elements, self.elements))  # Cross product
        elems = [f"{elem[0]}{self.direct_product_delimiter()}{elem[1]}" for elem in element_names]

        # The conjugate mapping created here will be passed, at the end, to the CD algebra
        # output by this method.  On the other hand, the self.conj method calls in the
        # multiplication section, below, refer to the conjugates of this ring itself, not
        # the ring to be output.
        conj_elems = [self.elem_conj(elem) for elem in elems]
        conj_map = dict(zip(elems, conj_elems))

        add_table = list()
        mul_table = list()
        for x in element_names:
            a = x[0]
            b = x[1]

            # Start new rows in the addition and multiplication tables
            add_table_row = list()
            mul_table_row = list()
            for y in element_names:
                c = y[0]
                d = y[1]

                # ADDITION: (a, b) + (c, d) = (a + b, c + d)
                add_table_row.append(element_names.index((self.add(a, c),
                                                          self.add(b, d))))
                # MULTIPLICATION:
                if version == 1:
                    # No mu and no conjugation used:
                    # Multiplication: (a, b) x (c, d) = (a x c  -  b x d,  a x d  +  b x c)
                    mul_table_row.append(element_names.index(((self.sub(self.mult(a, c),
                                                                        self.mult(b, d))),
                                                              (self.add(self.mult(a, d),
                                                                        self.mult(b, c))))))
                elif version == 2:
                    # See [Schafer, 1966]
                    # Conjugation: a* = a and (u, v)* = (u*, -v) recursively
                    # Multiplication: (a, b) x (c, d) = (a x c  +  mu x d x b*,  a* x d  +  c x b)
                    mul_table_row.append(element_names.index(((self.add(self.mult(a, c),
                                                                        self.mult(mu, d, self.conj(b)))),
                                                              (self.add(self.mult(self.conj(a), d),
                                                                        self.mult(c, b))))))
                elif version == 3:
                    # See [Schafer, 1954]
                    # Multiplication: (a, b) x (c, d) = (a x c  +  mu x d* x b,  d x a  +  b x c*)
                    mul_table_row.append(element_names.index(((self.add(self.mult(a, c),
                                                                        self.mult(mu, self.conj(d), b))),
                                                              (self.add(self.mult(d, a),
                                                                        self.mult(b, self.conj(c)))))))
                elif version == 4:
                    # See [Baez 2001]
                    # Multiplication: (a, b) x (c, d) = (a x c  -  d x b*,  a* x d  +  c x b)
                    mul_table_row.append(element_names.index(((self.sub(self.mult(a, c),
                                                                        self.mult(d, self.conj(b)))),
                                                              (self.add(self.mult(self.conj(a), d),
                                                                        self.mult(c, b))))))
                else:
                    raise ValueError(f"What happened?!?! We should never see this message. Version == {version}")

            # Append the new rows to each table
            add_table.append(add_table_row)
            mul_table.append(mul_table_row)

        return make_finite_algebra(name,
                                   description,
                                   elems,
                                   add_table,
                                   mul_table,
                                   conj_map)


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

def _no_conflict(p1, p2):
    """Returns True only if no element of p1 equals the corresponding element of p2."""
    return all([p1[i] != p2[i] for i in range(len(p1))])


def _no_conflicts(items):
    """Return True if each possible pair, from a list of items, has no conflicts."""
    return all(_no_conflict(combo[0], combo[1]) for combo in it.combinations(items, 2))


def _filter_out_conflicts(perms, perm, n):
    """Filter out all permutations in perms that conflict with perm,
    and don't have n as the first element."""
    nperms = [q for q in perms if q[0] == n]
    return [p for p in nperms if _no_conflict(p, perm)]


def generate_all_group_tables(order):
    """Experimental Code: Return a list of all arrays that correspond to multiplication tables for groups
    of a specific order.

    WARNING: The algorithm here is inefficient, so even very small values of 'order' will result in very
    long runtimes (e.g., order=6 ==> ~5-6 hrs runtime).
    """
    row0 = list(range(order))
    row_candidates = [[row0]]
    for row_num in range(1, order):
        row_candidates.append(_filter_out_conflicts(it.permutations(row0), row0, row_num))
    table_candidates = [cand for cand in it.product(*row_candidates) if is_table_associative(list(cand))]  # ***
    return [tbl for tbl in table_candidates if _no_conflicts(tbl)]


# TODO: Reconcile this version with the similar method in CayleyTable.
def is_table_associative(table):
    """Determine whether the table supports an associative operation."""
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
    """Given a list of multiplication tables, all the same size, turn them into a list of groups."""
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
    follow the identity element. Used by get_int_forms."""
    return int(''.join(map(lambda x: x.split("_")[1], elem_list[1:])))


def get_int_forms(ref_group, isomorphisms):
    """Return a list of integer forms ('permutations') for a list of isomorphisms,
    i.e., mappings, based on a reference group."""
    return [get_integer_form([iso[elem] for elem in ref_group.elements])
            for iso in isomorphisms]


# =========
#   Field
# =========

def is_field(add_id, elements, table):
    """The elements of a Field, minus the additive identity, form a commutative Group
    under multiplication. This function takes the additive identity, the list of all
    elements, and a field's multiplication table as input, and returns the Group under
    multiplication, if it exists, otherwise it returns False.  If the proposed Field
    inputs are trivial (only one element and a 1x1 table) then False is returned.  That
    is, a trivial Field is not allowed."""
    if len(elements) == 1:
        return False
    else:
        mult = make_finite_algebra("tmp", "temporary", elements, table)
        # elems_copy = elements.copy()
        # elems_copy.remove(add_id)

        # elements is a tuple, which is immutable. But we want to remove the
        # additive identity element from it, so first turn elements into a list
        # then remove the additive identity, and finally turn the result back
        # into a tuple. Whew!
        elems_list = list(elements)
        elems_list.remove(add_id)
        elems_copy = tuple(elems_list)

        elems_copy_clo = mult.closure(elems_copy, True)  # Includes inverse elements
        if set(elems_copy) == set(elems_copy_clo):
            mult_sub = mult.subalgebra_from_elements(elems_copy)
            if isinstance(mult_sub, Group) and mult_sub.is_commutative():
                return mult_sub
            else:
                return False
        else:
            return False


class Field(Ring):
    """A Field is a Ring, where the elements, minus the additive identity, form a commutative Group
    under multiplication."""

    def __init__(self, name, description, elements, table, table2, check_inputs=True, mult_sub_grp=None,
                 conjugate_mapping=None):

        super().__init__(name, description, elements, table, table2, check_inputs, conjugate_mapping)

        # This is the abelian Group defined by the Ring elements, minus the additive identity,
        # under Ring multiplication
        self._mult_sub_grp = mult_sub_grp

        if check_inputs or mult_sub_grp is None:
            abelian_group = is_field(self.identity, self.elements, self.mult_table.table)
            if abelian_group:
                self._mult_sub_grp = abelian_group
            else:
                raise ValueError(f"Inputs do not support the construction of a Field.")

        self._mult_sub_grp.name = f"{self.name}_G"
        self._mult_sub_grp.description = f"Multiplicative abelian Group of {self.name}"

    def mult_abelian_subgroup(self):
        """Return the abelian Group defined by the Ring elements, minus the additive identity,
        under Ring multiplication."""
        return self._mult_sub_grp

    def mult_inv(self, element):
        """Return the multiplicative inverse of 'element', unless it's the additive identity
        element, in which case, return None."""
        if element == self.add_identity:
            return None
        else:
            return self._mult_sub_grp.inv(element)

    def div(self, x, y):
        """Return x/y, if y is not the additive identity; otherwise return None."""
        if y == self.add_identity:
            return None
        else:
            return self.mult(x, self.mult_inv(y))

    def element_to_power(self, elem, n, left_associative=True):
        """Overrides the Ring method by the same name, so that we use
        don't recreate the multiplicative Abelian subgroup already contained
        in the field.
        """
        mult_alg = self.mult_abelian_subgroup()
        return mult_alg.element_to_power(elem, n, left_associative)


def generate_algebra_mod_n(n, elem_name='', name=None, description=None):
    """Generate a Ring (or Field) based on integer addition and multiplication modulo n.
    If n is prime, then result will be a Field, otherwise it will be a Ring."""

    if isprime(n):
        prime = True
    else:
        prime = False

    if name:
        nm = name
    elif prime:
        nm = "F" + str(n)
    else:
        nm = "R" + str(n)

    if description:
        desc = description
    elif prime:
        desc = f"Autogenerated Field of integers mod {n}"
    else:
        desc = f"Autogenerated Ring of integers mod {n}"

    nfill = len(str(n - 1))  # Number of zeros to left-fill integers in element names
    elements = [elem_name + str(i).zfill(nfill) for i in range(n)]
    add_table = [[(a + b) % n for b in range(n)] for a in range(n)]
    mult_table = [[(a * b) % n for b in range(n)] for a in range(n)]
    return make_finite_algebra(nm, desc, elements, add_table, mult_table)


def generate_nxn_matrix_algebra(ring, element_name_prefix='a'):
    """Generate a ring (or field) based on all possible 2x2 abstract matrices using
    elements from the input ring. For now, n is hardcoded to 2.
    Three items are returned:
    (1) the generated ring,
    (2) a dictionary of element names (keys) to matrices (values), and
    (3) a reverse dictionary of matrices (as tuples of tuples) to element names.
    """
    n = 2  # Square matrix dimension. Hardcoded to 2 for now.

    # Create all possible matrices, and give them names.
    # Then create a dictionary that maps each name (key) to its matrix (value).
    # Also, create a reverse dictionary of matrices (as tuples) mapped to names.
    count = 0
    elem_dict = dict()
    rev_dict = dict()
    elements = ring.elements
    for e00 in elements:  # TODO: Replace these for-loops so that n can be >= 2
        for e01 in elements:
            for e10 in elements:
                for e11 in elements:
                    mat = AbstractMatrix([[e00, e01], [e10, e11]], ring)
                    elem_name = element_name_prefix + str(count)
                    elem_dict[elem_name] = mat
                    rev_dict[mat.to_tuple()] = elem_name
                    count += 1

    # Create the Cayley table for addition of the matrix elements
    m = len(elem_dict)
    add_table = np.empty((m, m), AbstractMatrix)
    for row, elemr in enumerate(elem_dict.keys()):
        for col, elemc in enumerate(elem_dict.keys()):
            result = elem_dict[elemr] + elem_dict[elemc]
            name = rev_dict[result.to_tuple()]
            add_table[row][col] = name

    # Create the Cayley table for multiplication of the matrix elements
    mul_table = np.empty((m, m), AbstractMatrix)
    for row, elemr in enumerate(elem_dict.keys()):
        for col, elemc in enumerate(elem_dict.keys()):
            result = elem_dict[elemr] * elem_dict[elemc]
            name = rev_dict[result.to_tuple()]
            mul_table[row][col] = name

    name = f"{ring.name}_{n}x{n}"
    description = f"Algebra of {n}x{n} abstract matrices based on {ring.name}"
    elements = list(elem_dict.keys())
    algebra = make_finite_algebra(name, description, elements, add_table, mul_table)

    return algebra, elem_dict, rev_dict


# ==================================================================================
# Utilities for constructing Cayley-Dickson algebras (i.e., Squared Rings & Fields)
# ==================================================================================

def r2_scalar_mult(scalar_name, elem_name, algebra, delimiter=":"):
    """ Scalar multiplication. 'a' * 'c:d' = 'a*c:a*d'
    Example: scalar_mult('2', '1:2', F3) ==> '2:1'
    """
    components = elem_name.split(delimiter)
    return delimiter.join(map(lambda x: algebra.mult(scalar_name, x), components))


def r2_negate(elem_name, algebra, delimiter=":"):
    """ Negation:  -'a:b' = '-a:-b'
    Example: negate('1:2', F3) ==> '2:1'
    """
    components = elem_name.split(delimiter)
    return delimiter.join(map(lambda x: algebra.inv(x), components))


def r2_conjugate(elem_name, algebra, delimiter=":"):
    """ Conjugation: conj('a:b') = 'a:-b'
    Example: conjugate('0:1', F3) ==> '0:2'
    """
    components = elem_name.split(delimiter)
    head = components[0]
    tail = components[1:]
    tail_negated = list(map(lambda x: algebra.inv(x), tail))
    new_components = list(head) + tail_negated
    return delimiter.join(new_components)


def r2_sqr_abs_val(elem_name, algebra, alg_sqr, delimiter=':'):
    """Squared Absolute Value: 'a:b'^2 = 'a:b' * conj('a:b')
    Example: sqr_abs_val('1:2', F3, F3sqr) ==> '2'
    """
    val = alg_sqr.mult(elem_name, r2_conjugate(elem_name, algebra, delimiter))
    comp = val.split(delimiter)
    return comp[0]


# NOTE: The inverse function below is just for comparison/verification.
# The Field method, mult_inv, is the better way to compute the inverse of an element.
def r2_inverse(elem_name, algebra, alg_sqr, delimiter=':'):
    """ Inversion: inv('a:b') = conj('a:b') / sqr_abs_val('a:b')
    Only works for Fields, not Rings.
    Example: inverse('1:1', F3, F3sqr) ==> '2:1'
    """
    absvalsqr = r2_sqr_abs_val(elem_name, algebra, alg_sqr, delimiter)
    absvalsqrinv = algebra.mult_inv(absvalsqr)
    return r2_scalar_mult(absvalsqrinv, r2_conjugate(elem_name, algebra, delimiter), algebra)


# ==============
# Element Class
# ==============
class Element:
    """Elements of the algebras here must be strings. This class turns a string element,
    along with its algebra, into an object with infix arithmetic operators, +, -, *, /, **,
    etc.
    """

    def __init__(self, name, algebra):

        self._can_add = False
        self._can_subtract = False
        self._can_multiply = False
        self._can_divide = False

        if isinstance(algebra, Magma):
            self._algebra = algebra
            self._can_add = True
            self._can_subtract = self._algebra.has_inverses()
            if isinstance(algebra, Ring):
                self._can_multiply = True
                if isinstance(algebra, Field):
                    self._can_divide = True
        else:
            raise ValueError(f"algebra must be a FiniteAlgebra")

        if isinstance(name, str):
            if name in self._algebra:
                self._name = name
            else:
                raise ValueError(f"name must be an element of algebra")
        else:
            raise ValueError(f"name must be a string")

    @property
    def name(self):
        """Return the name of this Element."""
        return self._name

    @property
    def algebra(self):
        """Return the algebra associated with this Element."""
        return self._algebra

    @property
    def can_add(self):
        """Return True if this Element supports addition."""
        return True

    @property
    def can_subtract(self):
        """Return True if this Element supports subtraction."""
        return self._can_subtract

    @property
    def can_multiply(self):
        """Return True if this Element supports multiplication."""
        return self._can_multiply

    @property
    def can_divide(self):
        """Return True if this Element supports division."""
        return self._can_divide

    def __str__(self):
        return self._name

    def __repr__(self):
        return repr(self._name)

    def __add__(self, other):
        elem = self._algebra.op(self._name, other.name)
        return Element(elem, self._algebra)

    def __sub__(self, other):
        if self._can_subtract:
            elem = self._algebra.sub(self._name, other.name)
            return Element(elem, self._algebra)
        else:
            raise ValueError(f"{self._algebra.name} does not support subtraction")

    def __neg__(self):
        if self._can_subtract:
            elem = self._algebra.inv(self._name)
            return Element(elem, self._algebra)
        return None

    def __mul__(self, other):
        if self._can_multiply:
            elem = self._algebra.mult(self._name, other.name)
            return Element(elem, self._algebra)
        else:
            raise ValueError(f"{self._algebra.name} does not support multiplication")

    def __truediv__(self, other):
        if self._can_divide:
            elem = self._algebra.div(self._name, other.name)
            return Element(elem, self._algebra)
        else:
            raise ValueError(f"{self._algebra.name} does not support division")

    def __pow__(self, n):
        """See the documentation for the element_to_power method for either
        the Magma, Ring, or Field. This method calls one of those methods."""
        elem_to_pow_name = self._algebra.element_to_power(self._name, n)
        return Element(elem_to_pow_name, self._algebra)

    def __key(self):
        return tuple([self._name, self._algebra.__hash__()])

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.__key() == other.__key() and self._algebra == other.algebra
        else:
            return NotImplemented


# def element_map(algebra):
#     """Returns a dictionary where element names (str) are keys and the corresponding Elements
#     are the values."""
#     return {elem: Element(elem, algebra) for elem in algebra.elements}


class InfixNotation:
    """Creates a context manager for doing finite algebra calculations using infix notation.

    >>> s3 = generate_symmetric_group(3)
    >>> with InfixNotation(s3) as f:
    >>>     print(f['(2, 1, 3)'] + f['(3, 2, 1)'])
    (3, 1, 2)

    """

    def __init__(self, algebra):
        # self.element_map = element_map(algebra)
        self.element_map = algebra.element_map()

    def __enter__(self):
        return self.element_map

    def __exit__(self, _type, value, traceback):
        pass


# ==========================
# Modules and Vector Spaces
# ==========================

def module_sv_mult(ring):
    """Returns a function that scales a vector.  That is, a function that takes
    a scalar and a vector, and returns their product, also a vector."""
    delimiter = ring.direct_product_delimiter()

    # sv_mult(s, v) takes an element created from a direct product (e.g., v = "a:b:c"),
    # splits it into a list (e.g., ["a", "b", "c"]), then maps the multiplication of
    # another element, say "s", over the list (e.g., ["s" * "a", "s" * "b", "s" * "c"])
    # and then joins the list back together into a single string (e.g., "sa:sb:sc"),
    # where sa, sb, & sc represent the results of the multiplications.
    def sv_mult(s, v):
        """Scalar-Vector product function"""
        return delimiter.join([ring.mult(s, x) for x in v.split(delimiter)])

    return sv_mult


def module_dot_product(ring, vec1, vec2):
    """Returns a scalar (ring element) that represents the dot-product of the
    two input vectors."""
    delim = ring.scalar.direct_product_delimiter()
    return reduce(lambda a, b: ring.scalar.add(a, b),
                  map(lambda pair: ring.scalar.mult(*pair),
                      zip(vec1.split(delim), vec2.split(delim))))


class MultipleElementSetAlgebra(FiniteAlgebra):
    """This class represents Finite Algebras that do not have single element lists,
    such as VectorSpaces and Modules."""
    pass


class Module(MultipleElementSetAlgebra):
    """See https://abstract-algebra.readthedocs.io for the definition of a Module"""

    def __init__(self, name, description, ring, group, operator):
        super().__init__(name, description)
        if not isinstance(ring, Ring):
            raise ValueError(f"{ring} is not a Ring.")
        if not isinstance(group, Group) and group.is_abelian():
            raise ValueError(f"{group} is not an abelian Group.")
        if not check_module_conditions(ring, group, operator):
            raise ValueError("Inputs don't meet requirements for a Module.")
        self.scalar = ring
        self.vector = group
        self.sv_mult = operator  # scalar-vector operator

    def __repr__(self):
        sname = self.scalar.name
        vname = self.vector.name
        cname = self.__class__.__name__
        return f"<{cname}:{self.name}, ID:{id(self)}, Scalars:{sname}, Vectors:{vname}>"

    def vector_add(self, v1, v2):
        """Return the sum of two vectors using the Group operation, op."""
        return self.vector.op(v1, v2)

    def about(self, max_size=12, max_gens=2, use_table_names=False, show_tables=True, show_elements=True,
              show_generators=False):
        """Print information about the Module or Vector Space."""
        print(f"\n{self.__class__.__name__}: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"\nSCALARS:")
        self.scalar.about(max_size, max_gens, use_table_names, show_tables, show_elements, show_generators)
        print(f"\nVECTORS:")
        self.vector.about(max_size, max_gens, use_table_names, show_tables, show_elements, show_generators)
        return None


class VectorSpace(Module):
    """See https://abstract-algebra.readthedocs.io for the definition of a VectorSpace."""

    def __init__(self, name, description, field, group, operator):
        super().__init__(name, description, field, group, operator)
        if not isinstance(field, Field):
            raise ValueError(f"{field} must be a Field.")


class NDimensionalModule(Module):

    def __init__(self, ring, n, check_input_conditions=True):
        name = f"{n}D-{ring.name}"
        desc = f"{n}-dimensional Module over {ring.name}"
        self._dimensions = n

        # Group from the n-fold direct product of the Field with itself
        # group = ring.power(n)
        group = ring ** n

        super().__init__(name, desc, ring, group, module_sv_mult(ring))

        # Check input conditions, maybe
        if check_input_conditions:
            if not check_module_conditions(ring, group, self.sv_mult):
                raise ValueError("Inputs don't meet required conditions.")

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def origin(self):
        return self.vector.identity

    def dot_product(self, u, v):
        return module_dot_product(self, u, v)


class NDimensionalVectorSpace(VectorSpace):

    def __init__(self, field, n, check_input_conditions=True):
        name = f"{n}D-{field.name}"
        desc = f"{n}-dimensional Vector Space over {field.name}"
        self._dimensions = n

        # Group from the n-fold direct product of the Field with itself
        # group = field.power(n)
        group = field ** n

        super().__init__(name, desc, field, group, module_sv_mult(field))

        # Check input conditions, maybe
        if check_input_conditions:
            if not check_module_conditions(field, group, self.sv_mult):
                raise ValueError("Inputs don't meet required conditions.")

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def origin(self):
        return self.vector.identity

    def dot_product(self, u, v):
        return module_dot_product(self, u, v)


def check_module_conditions(ring: Ring, group: Group, sv_mult, verbose=False):
    """Returns True if all four conditions required of a Module hold true,
    otherwise this function returns False."""

    check1 = check_scaling_by_one(ring, group, sv_mult, verbose)
    if verbose:
        print(f"* Scaling by 1 OK? {yes_or_no(check1)}")

    check2 = check_dist_of_scalars_over_vec_add(ring, group, sv_mult, verbose)
    if verbose:
        print(f"* Distributivity of scalars over vector addition OK? {yes_or_no(check2)}")

    check3 = check_dist_of_vec_over_scalar_add(ring, group, sv_mult, verbose)
    if verbose:
        print(f"* Distributivity of vectors over scalar addition OK? {yes_or_no(check3)}")

    check4 = check_associativity(ring, group, sv_mult, verbose)
    if verbose:
        print(f"* Scaling by 1 OK? {yes_or_no(check4)}")

    return check1 & check2 & check3 & check4


def check_scaling_by_one(ring, group, sv_mult, verbose=False):
    """Returns True if scaling by one holds true in all cases, otherwise False is Returned."""
    is_ok = True
    one = ring.one
    for v in group.elements:
        if v != sv_mult(one, v):
            is_ok = False
            if verbose:
                print(f"{one} x {v} = {sv_mult(one, v)}")
    return is_ok


def check_dist_of_scalars_over_vec_add(ring, group, sv_mult, verbose=False):
    """Returns True if distributivity of scalars over vector addition holds true in all cases,
    otherwise False is Returned."""
    is_ok = True
    for s in ring.elements:
        for v1 in group.elements:
            for v2 in group.elements:
                a = sv_mult(s, group.op(v1, v2))
                b = group.op(sv_mult(s, v1), sv_mult(s, v2))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok


def check_dist_of_vec_over_scalar_add(ring, group, sv_mult, verbose=False):
    """Returns True if distributivity of vectors over scalar addition holds true in all cases,
    otherwise False is Returned."""
    is_ok = True
    for s1 in ring.elements:
        for s2 in ring.elements:
            for v in group.elements:
                a = sv_mult(ring.add(s1, s2), v)
                b = group.op(sv_mult(s1, v), sv_mult(s2, v))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok


def check_associativity(ring, group, sv_mult, verbose=False):
    """Return True if the special associativity condition on scalars and vectors holds true,
    otherwise return False."""
    is_ok = True
    for s1 in ring.elements:
        for s2 in ring.elements:
            for v in group.elements:
                a = sv_mult(ring.add(s1, s2), v)
                b = group.op(sv_mult(s1, v), sv_mult(s2, v))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok


# =====================
# Make Finite Algebra
# =====================

def make_finite_algebra(*args):
    """This is the recommended function to use to create any finite algebra.
    It analyzes the input and returns the appropriate finite algebra:
    Group, Ring, Field, VectorSpace, Module, Monoid, Semigroup, or Magma.

    If only 1 input argument, then it must either be a string or a Python
    dictionary.  If it's a string, then it must be a path to a JSON file
    that defines a SingleElementSetAlgebra (i.e., Magma, Semigroup, Monoid,
    Group, Ring, or Field), as described below for the first five arguments.
    If it's a Python dictionary, then it must be the dictionary version of
    such a JSON file. (No JSON or dictionary formats are defined for
    MultipleElementSetAlgebras.)

    Otherwise, the first argument should always be the name (str) of the
    algebra and the second argument should be a description (str) of the
    algebra.

    The remaining arguments depend on whether the algebra being constructed
    is a SingleElementSetAlgebra (i.e, Magma, Semigroup, Monoid, Group,
    Ring, or Field) or a MultipleElementSetAlgebra (i.e., Module or Vector
    Space).

    If constructing a SingleElementSetAlgebra:

    The third argument should be a list of element names (str).

    The fourth argument should be a list of lists of either all integers
    or all strings that represent a finite binary operation.  That is, a
    2-dimensional, square "table" (Cayley table).  The meaning of a table
    entry C corresponding to row A and column B, is that A * B = C, where
    * is the binary operator. If the items in the table are all integers,
    then they must all represent the positions of elements in the element
    list given by the third argument, above. If they are all strings, then
    they must all be members of the list of strings given by the third
    argument.

    A fifth argument is required only if a Ring or Field is being
    constructed, and it should also be a table with structure similar to
    the fourth argument.

    If constructing a MultipleElementSetAlgebra:

    The third argument should be a Ring or Field (the "scalars").

    The fourth argument should be a Group (the "vectors").

    And the fifth argument should be a function that implements the binary
    operation for "scaling vectors".

    See the definitions and examples at https://abstract-algebra.readthedocs.io
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

        # The inputs define a Group, Monoid, Semigroup, or Magma.
        # More checks to come farther below.
        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'elements': args[2],
                       'table': args[3]
                       }

    elif len(args) == 5:

        # The inputs define a VectorSpace or Module.
        # It gets created & returned immediately, right here.
        if isinstance(args[3], Group):
            if isinstance(args[2], Field):
                return VectorSpace(args[0], args[1], args[2], args[3], args[4])
            elif isinstance(args[2], Ring):
                return Module(args[0], args[1], args[2], args[3], args[4])
            else:
                raise ValueError(f"{args[2]} must be a Ring or a Field")

        # The inputs define a Field or Ring.
        # More checks to come farther below.
        else:
            finalg_dict = {'name': args[0],
                           'description': args[1],
                           'elements': args[2],
                           'table': args[3],
                           'table2': args[4]
                           }

    elif len(args) == 6:  # Only happens when we're constructing a Cayley-Dickson ring or field

        finalg_dict = {'name': args[0],
                       'description': args[1],
                       'elements': args[2],
                       'table': args[3],
                       'table2': args[4],
                       'conj_map': args[5]  # Lookup table for conjugates
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

    # If a second table was input, turn it into a CayleyTable
    # and determine if it supports associativity
    table2 = None
    is_assoc2 = False
    if 'table2' in finalg_dict:
        table2 = make_cayley_table(finalg_dict['table2'], elems)
        is_assoc2 = table2.is_associative()

    # Conjugate Mapping: A lookup table for conjugates in rings or fields that are Cayley-Dickson algebras
    if 'conj_map' in finalg_dict:
        conj_map = finalg_dict['conj_map']
    else:
        conj_map = None

    is_assoc = table.is_associative()
    identity = table.identity()  # this is the integer index of the identity, not the name str
    if identity is not None:
        inverses = table.has_inverses()
    else:
        inverses = None

    # Based on the properties of the inputs, create & return the appropriate algebraic structure
    if is_assoc:
        if identity is not None:
            if inverses:
                if table2 is not None and is_assoc2:
                    # is_field will either build the abelian Group, mentioned in the Field definition,
                    # or it will return False.  In the latter case, this becomes a Ring, instead of a Field.
                    # NOTE: Additional, required checks for multiplicative associativity and distributivity
                    # of multiplication over addition are done within the Field & Ring constructors themselves.
                    abelian_group = is_field(elems[identity], elems, table2.table)
                    if abelian_group:
                        return Field(name, desc, elems, table, table2, check_inputs=False,
                                     mult_sub_grp=abelian_group, conjugate_mapping=conj_map)
                    else:
                        return Ring(name, desc, elems, table, table2, check_inputs=False, conjugate_mapping=conj_map)
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


def delete_row_col(np_arr, row, col):
    """Removes the specified row and col from a Numpy array.
    A new np array is returned, so this does not affect the input array."""
    return np.delete(np.delete(np_arr, row, 0), col, 1)


def unpack_components(finalg):
    """A convenience function. It unpacks a SingleElementSetAlgebra
    and returns its components: name, description, elements, and
    table(s) (in list form).
    """
    if isinstance(finalg, SingleElementSetAlgebra):
        name = finalg.name
        description = finalg.description
        elements = finalg.elements
        table_as_list = finalg.table.tolist()
        if isinstance(finalg, Ring):
            table2_as_list = finalg.mult_table.tolist()
            conj_dict = finalg.conjugates()  # NOTE: This could be None
            return name, description, elements, table_as_list, table2_as_list, conj_dict
        else:
            return name, description, elements, table_as_list
    else:
        raise ValueError(f"{finalg} is not a SingleElementSetAlgebra.")


def make_cayley_table(table, elements):
    """Return a CayleyTable from a table of indices or a table of strings."""
    if isinstance(table[0][0], str):
        index_table = index_table_from_name_table(elements, table)
        ct = CayleyTable(index_table)
    else:
        ct = CayleyTable(table)
    return ct


# def make_cayley_table(table, elements):
#     table00 = table[0][0]
#     if isinstance(table00, str):
#         index_table = index_table_from_name_table(elements, table)
#         return CayleyTable(index_table)
#     elif isinstance(table00, int):
#         return CayleyTable(table)
#     else:
#         raise ValueError(f"Table must be all str or all int")


def index_table_from_name_table(elements, name_table):
    """Converts a table (list of lists) of strings into a table (list of lists) of ints."""
    return [[elements.index(elem_name) for elem_name in row] for row in name_table]


def get_duplicates(lst):
    """Return a list of the duplicate items in the input list."""
    return [item for item, count in collections.Counter(lst).items() if count > 1]


def yes_or_no(true_or_false):
    """A convenience function for turning True or False into Yes or No, respectively."""
    if true_or_false:
        return "Yes"
    else:
        return "No"


def symm_diff_of_two_lists_of_lists (list1, list2):
    """Return the symmetric difference between two lists of lists"""
    # Turn the inner lists into tuples, because tuples
    # are hashable and lists are not. Then turn the outer
    # lists into sets, before applying the symm diff operator.
    return set(map(tuple, list1)) ^ set(map(tuple, list2))


def same_lists_of_lists(list_of_lists1, list_of_lists2):
    """Handy for determining, for example, whether a list of left cosets
    is the same as a list of right cosets."""
    return not symm_diff_of_two_lists_of_lists(list_of_lists1, list_of_lists2)


# See https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    """Returns the powerset of the input iterable.
    e.g., powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))


def make_table_from_xml(table_string):
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
    """A convenience class for retrieving some example algebras in the "algebras"
    directory.  To add or subtract algebras to its default list, see the file,
    'examples.json', in the "algebras" directory."""

    def __init__(self, algebras_dir, filenames_json='examples.json'):
        examples_path = os.path.join(algebras_dir, filenames_json)
        with open(examples_path, 'r') as fin:
            self.filenames_list = json.load(fin)
        self.algebras = [make_finite_algebra(os.path.join(algebras_dir, filename))
                         for filename in self.filenames_list]
        self.about()

    def __len__(self):
        return len(self.algebras)

    def __getitem__(self, index):
        return self.algebras[index]

    def about(self):
        """Returns a list of example algebras with instructions on how to retrieve them."""
        n = 70
        print("=" * n)
        print(" " * (int(n / 2) - 8) + "Example Algebras")  # centered text
        print("-" * n)
        print(f"  {len(self.algebras)} example algebras are available.")
        print("  Use \"Examples[INDEX]\" to retrieve a specific example,")
        print("  where INDEX is the first number on each line below:")
        print("-" * n)
        index = 0
        for alg in self.algebras:
            print(f"{index}: {alg.name} -- {alg.description}")
            index += 1
        print("=" * n)


# End of File
