"""
@author: Alfred J. Reich

"""

# Standard Library Imports
import itertools as it
import json
import os
import collections as co
import functools as fnc
import pprint as pp
import copy

# Non-Standard Library Imports
import numpy as np


class Group:
    """A finite group (abstract algebra)

    Internally, the Group object consists of four quantities:

    - `name`: (string) A short name for the Group;
    - `description`: (string) Any additional, useful information about the Group;
    - `element_names`: (list of strings) The Group's element names, where the first element in the list is the Group's
      identity element (usually denoted by 'e');
    - `mult_table`: (list of lists of integers) The Group's multiplication table, where each list in the list
      represents a row of the table, and each integer represents the position of an element in 'element_names'.
      The table must be square, where the row or column length is the same as the number of elements (say, n).
      The first row and column should be the [0, 1, 2, ..., n], in that exact order.  Every row and column should
      contain the same integers, in a different order, as long as no row or column contains the same integer twice.

    The group constructor will enforce the `mult_table` conditions, described above.  It will also check the table to
    see if it supports associativity.  If any of the conditions are violated, or if associativity is not supported,
    then the group will not be instantiated.

    A Group object can be instantiated in several ways:

    1. Enter four values corresponding to the quantities described above, in the order shown above.

    2. Enter three values corresponding to `name`, `description`, and `mult_table`, where `mult_table` uses element
       names (strings) instead of integer positions.  The string-based mult_table must follow rules, similar to those
       described above: 1. identity element comes first in the first row and first column, 2. The names in the first
       row and column should be in the same order, and 3. No row or column contains the same element name twice.

    3. Enter a Python dictionary, with keys and values corresponding to either the four value or three value input
       schemes, described above.

    4. Enter a string representing the path to a JSON file that corresponds to the dictionary described above in 3.

    Examples:

    .. code-block:: python

       Group('v_4',
             'Klein-4 group',
             ['e',  'h',  'v', 'hv'],
             [[0, 1, 2, 3],
              [1, 0, 3, 2],
              [2, 3, 0, 1],
              [3, 2, 1, 0]])

       Group('v_4_VERSION2',
             'Klein-4 group again -- defined using element names in the mult_table',
             [[ 'e', 'h' ,  'v', 'hv'],
              [ 'h', 'e' , 'hv', 'v' ],
              [ 'v', 'hv',  'e', 'h' ],
              ['hv', 'v' ,  'h', 'e' ]])

    For more examples of Group instantiation, see the Jupyter Notebook: `ways_to_create_a_group`.

    A final note regarding the interpretation of the multiplication table, the row element is multiplied on the left
    and the column element on the right, e.g., row * col.  Or, assuming functions written on the left, such as
    permutations, this means that the column element is applied first and the row element is applied next,
    e.g., row(col(x)).

    """

    def __init__(self, *args):

        if len(args) == 1:
            if isinstance(args[0], str):
                with open(args[0], 'r') as fin:
                    # Assumes the single argument is a JSON file name string
                    grp_dict = json.load(fin)
            elif isinstance(args[0], dict):
                # Assumes the single argument is a dictionary
                grp_dict = args[0]
            elif isinstance(args[0], list):
                # Assumes input is a mult table (list of lists of element name strings)
                grp_dict = {'name': "no name",
                            'description': "Constructed from multiplication table",
                            'element_names': args[0][0],
                            'mult_table': args[0]}
            else:
                # No other options for single input arguments
                raise Exception("Single argument must be a string or a dictionary.")

        # The following assumes that no element_names list is input, and the table is
        # input using element names instead of indices of the elements.  So, the first
        # row of the table acts as the element_names list.
        elif len(args) == 3:
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2][0],  # top row of table input
                        'mult_table': index_table_from_name_table(args[2])
                        }
        else:
            # Assumes all four possible fields were input
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2],
                        'mult_table': args[3]
                        }
        self.name = grp_dict['name']
        self.description = grp_dict['description']

        if grp_dict.get('element_names'):
            self.element_names = grp_dict['element_names']
        else:
            self.element_names = grp_dict['mult_table'][0]  # First row of table

        # Setup the group's multiplication table
        tbl = grp_dict['mult_table']
        if isinstance(tbl[0][0], str):
            table = index_table_from_name_table(tbl)
        else:
            table = tbl
        self.mult_table = np.array(table, dtype=np.int64)

        self.__dp_delimiter = ':'  # name delimiter used when creating direct products

        # The following private members are for caching.
        self.__is_abelian = None
        self.__is_associative = None
        self.__element_orders = {elem: None for elem in self.element_names}

        # Finally, check that the inputs represent a valid group
        if check_inputs(self.element_names, self.mult_table):
            self.__inverse_lookup_dict = self.__make_inverse_lookup_dict()

    def __str__(self):
        """Return a string that identifies the object's class, name, and description."""
        return f"<{self.__class__.__name__}: {self.name}, {self.description}>"

    def __repr__(self):
        """Return a readable representation of the Group.

        NOTE: The method, `pprint`, also does this, but Pretty Prints the Group.
        """
        nm = self.name
        desc = self.description
        elems = self.element_names
        tbl = self.mult_table
        return f"{self.__class__.__name__}('{nm}',\n'{desc}',\n{elems},\n{tbl.tolist()}) "

    def __len__(self):
        """Return the order of the Group, i.e., the number of elements in it."""
        return len(self.element_names)

    def __contains__(self, element_name):
        """Return True if the element_name is in the group's list of element names."""
        return element_name in self.element_names

    def __getitem__(self, index):
        """Allows for iteration over elements of the group"""
        return self.element_names[index]

    @property
    def order(self):
        """Return the order of the group, ie., the number of elements in it."""
        return len(self.element_names)

    def element_order(self, element):
        """Return the order of the element.
        (Developer Note: The value returned is cached for future calls to this method.)

        Parameters
        ----------
        element : str
          An element of this group

        Returns
        -------
        int
          The element's order
        """
        def order_aux(elem, prod, order):
            if prod == self.identity:
                return order
            else:
                return order_aux(elem, self.mult(prod, elem), order + 1)
        # Memoize element orders:
        if self.__element_orders[element] is None:  # Check for no cached value
            self.__element_orders[element] = order_aux(element, element, 1)
        return self.__element_orders[element]

    def __eq__(self, other):
        """Return True if this Group is identical to the `other` Group.

        Parameters
        ----------
        other : Group
          Another group to check equality with

        Returns
        -------
        bool
          True if the element names and multiplication tables of the two groups are identical.
        """
        return (self.element_names == other.element_names) and np.array_equal(self.mult_table, other.mult_table)

    @property
    def identity(self):
        """Return the identity element of the Group.  Also known as the 'natural' element."""
        return self.element_names[0]

    def deepcopy(self):
        """Returns a deep copy of this group."""
        return Group(copy.deepcopy(self.name),
                     copy.deepcopy(self.description),
                     copy.deepcopy(self.element_names),
                     copy.deepcopy(self.mult_table))

    def direct_product_delimiter(self, delimiter=None):
        """If no input, then the current direct product element name delimiter will be returned (default is ':').
        Otherwise, if a string is input (e.g., "-") it will become the new delimiter for direct product element
        names, and then it will be returned.

        Parameters
        ----------
        delimiter : str or None
          A string that will be used to join group element names into new names when computing a direct product.

        Returns
        -------
        str
          The current delimiter.
        """
        if delimiter:
            self.__dp_delimiter = delimiter
            return self.__dp_delimiter
        else:
            return self.__dp_delimiter

    def __make_inverse_lookup_dict(self):
        """(Private Method) Return a dictionary of element names and their inverse names."""
        # A 0 index in the mult_table means that the row and col. are inverses
        row_indices, col_indices = np.where(self.mult_table == 0)
        return {self.element_names[elem_index]: self.element_names[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def to_dict(self):
        """Return a dictionary that represents this Group."""
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'element_names': self.element_names,
                'mult_table': self.mult_table.tolist()}

    def dumps(self):
        """Write the Group to a JSON string."""
        return json.dumps(self.to_dict())

    def dump(self, json_filename):
        """Write the Group to a JSON file.

        Parameters
        ----------
        json_filename : str
          Complete path to a JSON file

        """
        with open(json_filename, 'w') as fout:
            json.dump(self.to_dict(), fout)

    def inv(self, element_name):
        """Return the name of the inverse element for the input `element_name`.

        Parameters
        ----------
        element_name : str
          An element name

        Returns
        -------
        str
          The name of the element's inverse
        """
        return self.__inverse_lookup_dict[element_name]

    def conj(self, a, g):
        """Return g * a * inv(g), the conjugate of a with respect to g.

        Parameters
        ----------
        a : str
          An element name, e.g., a member of a subgroup when checking for normality w.r.t. a parent group
        g : str
          An element name, e.g., a member of the parent group when checking whether a subgroup is normal

        Returns
        -------
        str
          Returns g * a * inv(g), the conjugate of a with respect to g.
        """
        return self.mult(g, self.mult(a, self.inv(g)))

    def mult_table_with_names(self):
        """Return the multiplication table with element names rather than element positions."""
        return [[self.element_names[elem_pos] for elem_pos in row] for row in self.mult_table]

    def mult(self, *args):
        """Multiply zero or more elements using the group's multiplication table.

        Parameters
        ----------
        args : Zero or more element names separated by commas
          Elements of the group to be multiplied to each other, in the order given.
          If no arg are input, then the identity/natural element for the group is returned.
          If only one element name is input, then it is simply returned.
          If two or more element names are input, then they are multiplied together in the order given.

        Returns
        -------
        str
          The element that represents the product of the input elements
        """
        # If no args, return the identity
        if len(args) == 0:
            return self.element_names[0]
        # If one arg, and it's a valid element name, then just return it
        elif len(args) == 1:
            if args[0] in self.element_names:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid Group element name")
        # If two args, then look up their sum in the multiplication table
        elif len(args) == 2:
            row = self.element_names.index(args[0])
            col = self.element_names.index(args[1])
            index = self.mult_table[row, col]
            return self.element_names[index]
        # If more than two args, then multiply them all together
        else:
            return fnc.reduce(lambda a, b: self.mult(a, b), args)

    def pprint(self, use_element_names=False):
        """Pretty print the Group.  This method produces a readable representation of
        the Group.  That is, the output (strings) created by this method can be read back in
        to create a copy of the Group.  By default, the four basic components of the Group
        are printed: Name, Description, Element Names List, and Multiplication Table,
        where the table contains the indices (integers) of elements according to the
        element_names list.  If use_element_names is set to True, then the element names
        list is omitted in the printout and the table is printed using element names.

        Parameters
        ----------
        use_element_names : bool
          If true the table output shows element names rather than element indices.
          Default is False.

        Returns
        -------
        None
        """
        print(f"{self.__class__.__name__}('{self.name}',")
        print(f"'{self.description}',")
        if use_element_names:
            pp.pprint(self.mult_table_with_names())
        else:
            print(f"{self.element_names},")
            pp.pprint(self.mult_table.tolist())
        print(")")
        return None

    def is_associative(self):
        """Returns True if the Group is is_associative.
        (Developer Note: The value returned is cached for future calls to this method.)
        """
        if self.__is_associative is None:  # Check for no cached value
            self.__is_associative = is_table_associative(self.mult_table)
        return self.__is_associative

    # Direct Product Definition
    def __mul__(self, other):
        """Return the direct product of this Group with the `other` Group."""
        dp_name = f"{self.name}_x_{other.name}"
        dp_description = "Direct product of " + self.name + " & " + other.name
        dp_element_names = list(it.product(self.element_names, other.element_names))  # Cross product
        dp_mult_table = list()
        for a in dp_element_names:
            dp_mult_table_row = list()  # Start a new row
            for b in dp_element_names:
                dp_mult_table_row.append(dp_element_names.index((self.mult(a[0], b[0]), other.mult(a[1], b[1]))))
            dp_mult_table.append(dp_mult_table_row)  # Append the new row to the table
        return self.__class__(dp_name,
                              dp_description,
                              list([f"{elem[0]}{self.__dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                              dp_mult_table)

    def about(self, max_size=12, use_table_names=False):
        """Print information about the Group.

        Parameters
        ----------
        max_size : int
          Don't output table info for tables larger than this
        use_table_names : bool
          Set to True to see element names in table printout, instead of integer indices.
          Default is False.

        Returns
        -------
        None
        """
        print(f"\n{self.__class__.__name__}: {self.name}\n{self.description}")
        print(f"Abelian? {self.is_abelian()}")
        spc = 7
        print("Elements:")
        print("   Index   Name   Inverse  Order")
        for elem in self:
            idx_elem = self.element_names.index(elem)
            inv_elem = self.inv(elem)
            ord_elem = self.element_order(elem)
            print(f"{idx_elem :>{spc}} {elem :>{spc}} {inv_elem :>{spc}} {ord_elem :>{spc}}")
        size = len(self.element_names)
        if size <= max_size:
            if use_table_names:
                print(f"Cayley Table (showing names):")
                pp.pprint(self.mult_table_with_names())
            else:
                print(f"Cayley Table (showing indices):")
                pp.pprint(self.mult_table.tolist())
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so no further info calculated/printed.")
        return None

    def about_proper_subgroups(self, unique=False, show_elements=True):
        if unique:
            subgrps = self.unique_proper_subgroups()
        else:
            subgrps = self.proper_subgroups()
        print(f"\nSubgroups of {self.name}:")
        for subgrp in subgrps:
            print(f"\n  {subgrp.name}:")
            print(f"       order: {subgrp.order}")
            if show_elements:
                print(f"    elements: {subgrp.element_names}")
            print(f"    abelian?: {subgrp.is_abelian()}")
            print(f"     normal?: {self.is_normal(subgrp)}")
        return None

    def is_abelian(self):
        """Returns True if the group is abelian (commutative)."""
        if self.__is_abelian is None:  # Check for no cached value
            result = True
            for e1 in self.element_names:
                for e2 in self.element_names:
                    if not (self.mult(e1, e2) == self.mult(e2, e1)):
                        result = False
                        break
            self.__is_abelian = result  # Cache this result
        return self.__is_abelian

    def commutative(self):
        """Returns True if the group is commutative (abelian)."""
        return self.is_abelian()

    def is_normal(self, subgrp):
        """Return True if the subgroup is normal."""
        result = True
        for x in self:
            for a in subgrp:
                if not self.conj(a, x) in subgrp:
                    result = False
                    break
        return result

    def closure(self, subset_of_elements):
        """Given a subset (in list form) of the group's elements (name strings),
        return the smallest possible set of elements, containing the subset,
        that is closed under group multiplication, with inverses.

        Parameters
        ----------
        subset_of_elements : list
          A list of elements in the group

        Returns
        -------
        list
          The closure of the input list.  The elements of the closure can be used to form
          a subgroup of the group.
        """

        # Make sure inverses are considered
        result = set(subset_of_elements)
        for elem in subset_of_elements:
            result.add(self.inv(elem))

        # Add the products of all possible pairs
        for pair in it.product(result, result):
            result.add(self.mult(*pair))

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
        all_elements = self.element_names
        n = len(all_elements)
        for i in range(2, n - 1):  # avoids trivial closures, {'e'} & set of all elements
            # Look at all combinations of elements: pairs, triples, quadruples, etc.
            for combo in it.combinations(all_elements, i):
                clo = frozenset(self.closure(list(combo)))  # freezing required to add a set to a set
                if len(clo) < n:  # Don't include closures consisting of all elements
                    closed.add(clo)
        return list(map(lambda x: list(x), closed))

    def subgroup_from_elements(self, closed_subset_of_elements, name="No name", desc="No description"):
        """Return the Group constructed from the given closed subset of elements.

        Parameters
        ----------
        closed_subset_of_elements : list
          A list of elements in the group
        name : str
          The name of the subgroup to be generated
        desc : str
          A description of the subgroup to be generated

        Returns
        -------
        Group
          The subgroup defined by the input closed subset of elements
        """
        # Make sure the elements are sorted according to their order in the parent Group (self)
        # TODO: Check whether the input elements are indeed closed (make this check optional)
        #       Use the is_closed method (To Be Written) defined, above.
        elements_sorted = sorted(closed_subset_of_elements, key=lambda x: self.element_names.index(x))
        table = []
        for a in elements_sorted:
            row = []
            for b in elements_sorted:
                # The table entry is the index of the product in the sorted elements list
                row.append(elements_sorted.index(self.mult(a, b)))
            table.append(row)
        return Group(name, desc, elements_sorted, table)

    def proper_subgroups(self):
        """Return a list of proper subgroups of the group

        Returns
        -------
        list
          The list of proper subgroups of the group
        """
        desc = f"Subgroup of: {self.description}"
        count = 0
        list_of_subgroups = []
        for closed_element_set in self.closed_proper_subsets_of_elements():
            name = f"{self.name}_subgroup_{count}"
            count += 1
            list_of_subgroups.append(self.subgroup_from_elements(closed_element_set, name, desc))
        return list_of_subgroups

    def trivial_subgroups(self):
        """Return the group's two trivial subgroups.

        Returns
        -------
        list
          A list containing the two trivial subgroups of the group
        """
        name = f"Subgroup of {self.name}"
        desc = f"Trivial subgroup: {self.description}"
        trivial = Group(name, desc, [self.identity], [[0]])
        return [trivial, self]

    def subgroups(self):
        """Return a list of all subgroups, including trivial subgroups.

        Returns
        -------
        list
          A list of all subgroups of the group
        """
        return self.proper_subgroups() + self.trivial_subgroups()

    def unique_proper_subgroups(self, subgroups=None):
        """Return a list of proper subgroups that are unique, up to isomorphism.
        If no subgroups are provided, then they will be derived.

        Parameters
        ----------
        subgroups : list
          A list of subgroups that have already been computed

        Returns
        -------
        list
          Returns a list of proper subgroups that are unique, up to isomorphism
        """
        if subgroups:
            iso_sets_of_subs = divide_groups_into_isomorphic_sets(subgroups)
        else:
            iso_sets_of_subs = divide_groups_into_isomorphic_sets(self.proper_subgroups())
        # Return a list of the first subgroups from each sublist of proper subgroups
        return [iso_set[0] for iso_set in iso_sets_of_subs]

    def reorder_elements(self, reordered_elements):
        """Return a new group made from this one with the elements reordered.

        Parameters
        ----------
        reordered_elements : list
          A reordered list of the group's element names (str)

        Returns
        -------
        Group
          A new group using the new element order, but with the same multiplication operation.
        """
        n = self.order
        if n == len(reordered_elements):
            new_table = np.full((n, n), 0)
            for row in range(n):
                for col in range(n):
                    prod = self.mult(reordered_elements[row], reordered_elements[col])
                    new_table[row, col] = reordered_elements.index(prod)
            new_name = str(self.name) + '_REORDERED'
            new_desc = str(self.description) + ' (elements reordered)'
            return Group(new_name, new_desc, reordered_elements, new_table)
        else:
            raise Exception(f"There are {len(reordered_elements)} reordered elements.  There should be {n}.")

    def element_mappings(self, other):
        """Returns a list of mappings (dictionaries) of this group's elements to all possible permutations
        of other's elements, where the identity of this group is always mapped to the identity of other.

        Parameters
        ----------
        other : Group
          Another group to compare this group with, e.g., are they isomorphic?

        Returns
        -------
        list
          A list of dictionaries mapping this group's elements to the other group's elements.
        """
        if self.order == other.order:
            elems0 = self.element_names
            elems1 = other.element_names
            mappings = [dict(zip(elems0[1:], perm)) for perm in it.permutations(elems1[1:])]
            for mapping in mappings:
                mapping[elems0[0]] = elems1[0]
            return mappings
        else:
            raise Exception(f"Groups must be of the same order: {self.order} != {other.order}")

    def isomorphic_mapping(self, other, mapping):
        """Returns True if the input mapping from this group to the other group is isomorphic.

        Parameters
        ----------
        other : Group
          The other group this group is being compared with.
        mapping: dict
          A mapping between the elements of this group and the 'other' group.

        Returns
        -------
        bool
          Returns True if the mapping represents an isomorphism between the two groups; False, otherwise.
        """
        elems = self.element_names
        return all([mapping[self.mult(x, y)] == other.mult(mapping[x], mapping[y]) for x in elems for y in elems])

    def isomorphic(self, other):
        """If there is a mapping from elements of this group to the other group's elements,
        return it; otherwise return False.

        Parameters
        ----------
        other : Group
          Another group to compare this group with

        Returns
        -------
        dict or bool
          Returns the mapping if the two groups are isomorphic, otherwise, False is returned.
        """
        if self.order == other.order:
            maps = self.element_mappings(other)
            for mp in maps:
                if self.isomorphic_mapping(other, mp):
                    return mp
            return False
        else:
            return False


# Group Generators

def generate_cyclic_group(order, identity_name="e", elem_name="a", name=None, description=None):
    """Generates a cyclic group with the given order.

    Parameters
    ----------
    order : int
      A positive integer
    identity_name : str
      The name of the group's identity element
      Defaults to 'e'
    elem_name : str
      Prefix for all non-identity elements
      Default is a1, a2, a3, ...
    name : str
      The group's name.  Defaults to 'Zn',
      where n is the order.
    description : str
      A description of the group. Defaults to
      'Autogenerated cyclic group of order n',
      where n is the group's order.

    Returns
    -------
    Group
      A cyclic group of the given order
    """

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


# Utilities

# From: https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))


def get_duplicates(lst):
    """Return a list of the duplicate items in the input list.

    This function is used by `check_inputs`."""
    return [item for item, count in co.Counter(lst).items() if count > 1]


def check_inputs(element_names, mult_table):
    """Check that the element_list and mult_table have sizes and contents
    that don't violate the attributes of a group.

    This function is used by the Group constructor."""

    # Check for duplicate element names
    dups = get_duplicates(element_names)
    if len(dups) == 0:
        pass
    else:
        raise ValueError(f"Duplicate element names: {dups}")

    # Check that table is square
    rows, cols = mult_table.shape
    if rows == cols:
        pass
    else:
        raise ValueError(f"The table is not square: {rows}x{cols}")

    # Check that the row-col dimensions are the same as the number of elements
    num_elements = len(element_names)
    if rows == num_elements:
        pass
    else:
        raise ValueError(f"Number of elements is {num_elements}, but table size is {rows}x{cols}")

    # Check that each table row contains the correct values for a Cayley table
    correct_indices = set(range(num_elements))  # {0, 1, 2, ..., n-1}
    row_number = -1
    for row in mult_table:
        row_number += 1
        if set(row) == correct_indices:
            pass
        else:
            raise ValueError(f"A row {row_number} does not contain the correct values")

    # Check that each table col contains the correct values for a Cayley table
    for col_number in range(num_elements):
        if set(mult_table[:, col_number]) == correct_indices:
            pass
        else:
            raise ValueError(f"Column {col_number} does not contain the correct values")

    # Check that the table supports associativity for multiplication
    if is_table_associative(mult_table):
        pass
    else:
        raise ValueError("Multiplication table is not is_associative.")

    return True


def divide_groups_into_isomorphic_sets(list_of_groups):
    """Divide the list of groups into sub-lists of groups that are isomorphic to each other.
    The purpose of this function is operate on the proper subgroups of a group to determine
    the unique subgroups, up to isomorphism.

    Parameters
    ----------
    list_of_groups : list
      A list of groups, e.g., the list of subgroups of a group.

    Returns
    -------
    list
      A list of lists of groups, where each sublist represents groups that are isomorphic to each other.
    """

    def iso_and_not_iso(gp, gps):
        """Divide the list of groups, gps, into two lists, those that are isomorphic to gp
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
        """Recursively subdivide 'remainder' into lists that are isomorphic to its first member of the
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


def index_table_from_name_table(name_table):
    """Given a Cayley table using element names, return a table that uses position indices.
    Assumes that the first element in the first row of the table is the identity for the
    table's algebra.

    This function is used by the Group constructor.

    Parameters
    ----------
    name_table : list
      A square array (list of lists) that contains strings (names of group elements)
      that represent a group's multiplication table.

    Returns
    -------
    list
      The same table using element position indices (int)
    """
    top_row = name_table[0]
    return [[top_row.index(elem_name) for elem_name in row] for row in name_table]


def make_table(table_string):
    """This function helps turn the XML-based tables at Groupprops into a
    list of lists for use here.

    Instructions for use:
    1. Copy the table from there and paste it here;
    2. Find & Replace the strings, "<row>" and "</row>", with nothing;
    3. Place triple quotes around the result and give it a variable name;
    4. Then run make_table on the variable.

    Parameters
    ----------
    table_string : str
      XML-based table at Groupprops

    Returns
    -------
    list
      A list of lists of ints, representing a group's multiplication table.
    """
    return [[int(n) for n in row.strip().split(" ")]
            for row in table_string.splitlines()]


def __no_conflict(p1, p2):
    """Returns True only if no element of p1 equals the corresponding element of p2."""
    return all([p1[i] != p2[i] for i in range(len(p1))])


def __no_conflicts(items):
    """Return True if each possible pair, from a list of items, has no conflicts."""
    return all(__no_conflict(combo[0], combo[1]) for combo in it.combinations(items, 2))


def __filter_out_conflicts(perms, perm, n):
    """Filter out all permutations in perms that confict with perm,
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


def tables_to_groups(tables, identity_name="e", elem_name="a"):
    """Given a list of multiplication tables, all of the same size, turn them into a list of groups.

    Parameters
    ----------
    tables : list
      A list of tables (list of lists of ints) that represent group multiplication tables
    identity_name : str
      Root name to use for the identity element in all the groups
    elem_name : str
      Root name to use for the groups' elements

    Returns
    -------
    list
      A list of Groups based on the input tables.
    """
    order = len(tables[0])
    groups = []
    for j in range(len(tables)):
        gname = f"G{j}"
        desc = f"Group {j} of order {order}"
        ename = elem_name + str(j) + "_"
        elements = [identity_name + str(j)] + [f"{ename}" + str(i) for i in range(1, order)]
        groups.append(Group(gname, desc, elements, tables[j]))
    return groups


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


# EXPERIMENTAL STUFF

def get_integer_form(elem_list):
    """For an element list like ['e1', 'a1_2', 'a1_1', 'a1_3'],
    return the integer 213, i.e., the 'subscripts' of the elements that
    follow the identity element."""
    return int(''.join(map(lambda x: x.split("_")[1], elem_list[1:])))


def get_int_forms(ref_group, isomorphisms):
    """Return a list of integer forms ('permutations') for a list of isomorphisms,
    i.e., mappings, based on a reference group."""
    return [get_integer_form([iso[elem] for elem in ref_group.element_names])
            for iso in isomorphisms]


# PERMUTATIONS

class Perm:  # Permutation

    def __init__(self, permutation):
        self.perm = permutation
        self.base = min(self.perm)  # lowest value in perm
        self.size = len(self.perm) + self.base
        #
        # MAPPING: A mapping of the consecutive integers, starting at the base value,
        # to the integers in the permutation.
        #   Examples:
        #     0-based mapping: (0, 1, 2, 3) ==> {0: 0, 1: 1, 2: 2, 3: 3}
        #     1-based mapping: (3,1,2) ==> {1: 3, 2: 1, 3: 2}
        self.mapping = {i: self.perm[i - self.base] for i in range(self.base, self.size)}

    def __eq__(self, other):
        """Return True if the other's enclosee permutation (`tuple`) is the same as this one's."""
        return self.perm == other.perm

    def __hash__(self):
        """Use the enclosed permutation `tuple` for hashing this object"""
        return hash(self.perm)

    def __repr__(self):
        """A readable print representation of this permutation."""
        return f'Perm({self.perm})'

    def __len__(self):
        """Return the number of elements in the permutation."""
        return len(self.perm)

    def __mul__(self, other):
        """Compose this permutation with another, that is, self(other(id)),
        where *id* is the identity permutation, (0,1,...,n-1) or (1,2,...,n).
        Both permutations must use the same base and be of the same size,
        otherwise an exception will be raised."""
        if self.base == other.base:
            if len(self) == len(other):
                return Perm(tuple([self.mapping[other.mapping[i]] for i in range(self.base, self.size)]))
            else:
                raise Exception(f"Mixed lengths: {len(self)} != {len(other)}")
        else:
            raise Exception(f"Mixed bases: {self.base} != {other.base}")


def generate_symmetric_group(n, name=None, description=None, base=1):
    """Generates a symmetric group on n elements.

    Parameters
    ----------
    n : int
      A positive integer. The number of elements, (1, 2, 3, ..., n).
      Or, if the base is 0, then, the elements are (0, 1, 2, ..., n-1).
    name : str
      The group's name.  Defaults to 'Sn',
      where n is the order.
    description : str
      A description of the group. Defaults to
      'Autogenerated symmetric group on n elements',
      where n is the group's order.
    base : int
      A non-negative integer (typically, 0 or 1).
      The default is 1, so permutations will be
      on the tuple (1, 2, 3, ..., n), where n is
      the order.  Base 0, on the other hand, would
      produce permutations of (0, 1, 2, ..., n-1).

    Returns
    -------
    Group
      A symmetric group on n elements.
    """
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
    return Group(nm, desc, mul_tbl)


def generate_powerset_group(n, name=None, description=None):
    """Generates a group on the powerset of {0, 1, 2, ..., n-1},
    where symmetric difference is the operator.

    Parameters
    ----------
    n : int
      A positive integer. The number of elements in the set, {0, 1, 2, ..., n-1},
      from which the powerset will be created. The sets in the powerset will be
      the group's elements.
    name : str
      The group's name.  Defaults to 'PSn',
      where n is the order.
    description : str
      A description of the group. Defaults to
      'Autogenerated powerset group on a set of n elements'.
      The group's order will be 2^n.

    Returns
    -------
    Group
      A group on the powerset of {0, 1, 2, ..., n-1},
      where symmetric difference is the group's operator.
    """
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


def powerset_mult_table(n):
    """Return the multiplication table for the powerset of {0, 1, 2, ..., n-1},
    where intersection is the multiplication operation.

    Parameters
    ----------
    n : int
      Size of the set used to compute a powerset

    Returns
    -------
    list
      A list of lists of strings, representing the multiplication table for a group,
      where intersection is the 'multiplication' operation of a ring based on sets
      from a powerset.
    """
    set_of_n = set(list(range(n)))
    pset = [set(x) for x in list(powerset(set_of_n))]
    return [[pset.index(a & b) for b in pset] for a in pset]


class Ring(Group):

    def __init__(self, *args):

        if len(args) == 5:
            super().__init__(*args[:4])

        self.rmult_table = np.array(args[4], dtype=np.int64)

        # TODO: Check that this is an abelian group
        # TODO: Check that distributivity holds true

    def add(self, *args):
        """Use the parent's (group) mult. operation as the ring's addition operator."""
        return super().mult(*args)

    def rmult(self, *args):
        """The ring's multiplication operation."""
        # If no args, return the identity
        if len(args) == 0:
            return self.element_names[0]
        # If one arg, and it's a valid element name, then just return it
        elif len(args) == 1:
            if args[0] in self.element_names:
                return args[0]
            else:
                raise ValueError(f"{args[0]} is not a valid Group element name")
        # If two args, then look up their sum in the multiplication table
        elif len(args) == 2:
            row = self.element_names.index(args[0])
            col = self.element_names.index(args[1])
            index = self.rmult_table[row, col]
            return self.element_names[index]
        # If more than two args, then multiply them all together
        else:
            return fnc.reduce(lambda a, b: self.rmult(a, b), args)

    def identity_element(self):
        """If it exists, find the identity element for the given operation, op."""
        result = None
        for x in self:
            xy = [self.rmult(x, y) for y in self]
            if xy == self.element_names:
                result = x
        return result

    def is_distributive(self, verbose=False):
        """Check that a(b + c) = ab + ac for all elements, a, b, and c, in the Ring, rng."""
        result = True
        for a in self:
            for b in self:
                for c in self:
                    b_plus_c = self.add(b, c)
                    ab = self.rmult(a, b)
                    ac = self.rmult(a, c)
                    if self.rmult(a, b_plus_c) != self.add(ab, ac):
                        if verbose:
                            print(f"a = {a}; b = {b}; c = {c}")
                            print(f"{a} x {b_plus_c} != {ab} + {ac}")
                        result = False
                        break
        return result

    def rmult_table_with_names(self):
        return [[self.element_names[elem_pos]
                 for elem_pos in row]
                for row in self.rmult_table]

    def pprint(self, use_element_names=False):
        print(f"{self.__class__.__name__}('{self.name}',")
        print(f"'{self.description}',")
        if use_element_names:
            pp.pprint(self.mult_table_with_names())
            pp.pprint(self.rmult_table_with_names())
        else:
            print(f"{self.element_names},")
            print("")
            pp.pprint(self.mult_table.tolist())
            print("")
            pp.pprint(self.rmult_table.tolist())
        print(")")
        return None


# TODO: Implement fields

class Field(Ring):
    """Not implemented yet"""
    pass


if __name__ == '__main__':

    print("\n=======================================================================")

    print("\n--------------")
    print("START OF TESTS")
    print("--------------")

    # import pprint as pp

    project_path = os.path.join(os.getenv('PYPROJ'), 'abstract_algebra')

    algebras = [Group(os.path.join(project_path, 'Algebras/v4_klein_4_group.json')),
                Group(os.path.join(project_path, 'Algebras/z4_cyclic_group_of_order_4.json')),
                Group(os.path.join(project_path, 'Algebras/s3_symmetric_group_on_3_letters.json')),
                Group(os.path.join(project_path, 'Algebras/s3x_symmetric_group_OTHER.json')),
                Group(os.path.join(project_path, 'Algebras/Z2xZ2xZ2.json')),
                Group(os.path.join(project_path, "Algebras/Pinter_page_29.json")),
                Group(os.path.join(project_path, "Algebras/Pinter_page_29_VERS2.json")),
                Group(os.path.join(project_path, "Algebras/a4_alternating_group_on_4_letters.json")),
                Group(os.path.join(project_path, "Algebras/d3_dihedral_group_of_order_6.json")),
                Group(os.path.join(project_path, "Algebras/d4_dihedral_group_on_4_vertices.json"))
                ]

    # Create some direct products
    z2 = generate_cyclic_group(2)
    v4 = algebras[0]
    z4 = algebras[1]
    s3 = algebras[2]
    v4_x_z4 = v4 * z4
    z4_x_s3 = z4 * s3
    z2_x_z2_x_z2 = z2 * z2 * z2

    # Autogenerate some groups
    z5 = generate_cyclic_group(5, 'E', 'A', 'Z5', 'Cyclic group')
    s3_1 = generate_symmetric_group(3, 'S3_1', 'Symmetric group')
    s3_0 = generate_symmetric_group(3, 'S3_0', 'Symmetric group', base=0)
    p3 = generate_powerset_group(3, 'P3', 'Powerset group')

    # Extend the list, above, with the direct products, just created:
    algebras.extend([v4_x_z4, z4_x_s3, z2_x_z2_x_z2, z5, s3_0, s3_1, p3])

    # Show info for each algebra in the list
    for grp in algebras:
        grp.about()

    print("\n")
    v4 = algebras[0]
    subs = v4.proper_subgroups()
    for sub in subs:
        sub.pprint()

    print(f"\nOrder of subgroups of {z2_x_z2_x_z2.name}:")
    print([g.order for g in z2_x_z2_x_z2.proper_subgroups()])

    print(f"\nTurning a group into dictionary:")
    # pp.pprint(z4.to_dict())
    print(z4.to_dict())

    print("\n------------")
    print("END OF TESTS")
    print("------------")
