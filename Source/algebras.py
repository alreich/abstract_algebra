import itertools as it
import numpy as np
import json
import os
from collections import Counter


class Group:
    """This is a finite group (abstract algebra)

    The group definition here is assumed to have a finite number of elements, along
    with an addition table (Cayley table).

    The arguments can consist of a single string, representing the path to a JSON
    file that defines the group, or a single Python dictionary, that defines the
    group, or the four quantities listed below:
        name: A string name for the group;
        description: A string describing the group;
        element_names: A list of strings that represent the names of group elements;
        addition_table: a list of lists (2D array) of numbers that represent positions
            of elements in the elements list. The following requirements on the array
            must be adhered to:
            (1) The elements of the array must be integers that reference the groups
                elements according to their index (position) in the list, element_names.
            (2) 0 must always refer to the identity element for the group operation (addition)
            (3) The first row and first column must be the integers in order, 0, 1, 2,..., n-1,
                where n is the number of elements.

    Regarding the interpretation of the addition table, the row element is added on
    the left and the column element on the right, e.g., row + col.  Or, assuming
    functions written on the left, such as permutations, this means that the column
    element is applied first and the row element is applied next, e.g., row(col(x)).
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
            else:
                # TODO: Allow for just a table to be input (list of lists of element name strings)
                # No other options for single input arguments
                raise Exception("Single argument must be a string or a dictionary.")

        # The following assumes that no element_names list is input, and the table is
        # input using element names instead of indices of the elements.  So, the first
        # row of the table acts as the element_names list.
        elif len(args) == 3:
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2][0],  # top row of table input
                        'addition_table': index_table_from_name_table(args[2])
                        }
        else:
            # Assumes all four possible fields were input
            grp_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2],
                        'addition_table': args[3]
                        }
        self.name = grp_dict['name']
        self.description = grp_dict['description']

        if grp_dict.get('element_names'):
            self.element_names = grp_dict['element_names']
        else:
            self.element_names = grp_dict['addition_table'][0]  # First row of table

        tbl = grp_dict['addition_table']
        if isinstance(tbl[0][0], str):
            table = index_table_from_name_table(tbl)
        else:
            table = tbl
        self.addition_table = np.array(table, dtype=np.int64)

        self.dp_delimiter = ':'  # name delimiter used when creating direct products

        if check_inputs(self.element_names, self.addition_table):
            self.inverse_lookup_dict = self._make_inverse_lookup_dict()

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.description}>"

    def __repr__(self):
        nm = self.name
        desc = self.description
        elems = self.element_names
        tbl = self.addition_table
        return f"{self.__class__.__name__}('{nm}', '{desc}', {elems}, {tbl}) "

    def set_direct_product_delimiter(self, delimiter=':'):
        """Change or reset the delimiter used to construct new element names of direct products.
        The default delimiter is a colon."""
        self.dp_delimiter = delimiter
        return None

    def _make_inverse_lookup_dict(self):
        """Return a dictionary of element names and their inverse names."""
        row_indices, col_indices = np.where(self.addition_table == 0)
        return {self.element_names[elem_index]: self.element_names[elem_inv_index]
                for (elem_index, elem_inv_index)
                in zip(row_indices, col_indices)}

    def to_dict(self):
        """Return a dictionary that represents this group."""
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'element_names': self.element_names,
                'addition_table': self.addition_table.tolist()}

    def dumps(self):
        """Write the group to a JSON string."""
        return json.dumps(self.to_dict())

    def dump(self, json_filename):
        """Write the group to a JSON file."""
        with open(json_filename, 'w') as fout:
            json.dump(self.to_dict(), fout)

    def inverse(self, element_name):
        """Return the inverse name of the input element name."""
        return self.inverse_lookup_dict[element_name]

    def addition_table_with_names(self):
        """Return the addition table with element names rather than element positions."""
        return [[self.element_names[elem_pos] for elem_pos in row] for row in self.addition_table]

    def add(self, a, b):
        """Given element names, a & b, return the sum, a + b, according the the addition table."""
        a_pos = self.element_names.index(a)
        b_pos = self.element_names.index(b)
        product_index = self.addition_table[a_pos, b_pos]
        return self.element_names[product_index]

    def pretty_print_addition_table(self, delimiter=' ', prefix=''):
        """Print the Cayley table for addition using element names."""
        field_size = 1 + len(max(self.element_names, key=len))  # 1 + Longest Name Length
        for row_index in self.addition_table[:, 0]:  # row index from first column
            row_string = f"{prefix}"
            for col_index in self.addition_table[0]:  # column index from first row
                prod_index = self.addition_table[row_index, col_index]
                prod_name = self.element_names[prod_index]
                row_string += delimiter + f"{prod_name :>{field_size}}"
            print(row_string)

    def associative(self):
        "A brute force test of associativity.  Returns True if the group is associative."
        result = True
        for a in self.element_names:
            for b in self.element_names:
                for c in self.element_names:
                    if not (self.add(self.add(a, b), c) == self.add(a, self.add(b, c))):
                        result = False
                        break
        return result

    # Direct Product Definition
    def __mul__(self, other):
        """Return the direct product of this group with an 'other' group."""
        dp_name = self.name + "_x_" + other.name
        dp_description = "Direct product of " + self.name + " & " + other.name
        dp_element_names = list(it.product(self.element_names, other.element_names))  # Cross product
        dp_addition_table = list()
        for a in dp_element_names:
            addition_table_row = list()  # Start a new row
            for b in dp_element_names:
                addition_table_row.append(dp_element_names.index((self.add(a[0], b[0]), other.add(a[1], b[1]))))
            dp_addition_table.append(addition_table_row)  # Add the new row to the table
        return self.__class__(dp_name,
                              dp_description,
                              list([f"{elem[0]}{self.dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                              dp_addition_table)

    def print_info(self, max_size=12, prefix='  '):
        print(f"\n{self.__class__.__name__} : {self.name} : {self.description}")
        print(f"{prefix}Element Names: {self.element_names}")
        print(f"{prefix}Is Abelian? {self.abelian()}")
        # Don't calculate/print the following info if the Group is greater than max_size
        print(f"{prefix}Inverses:  (** - indicates that it is its own inverse)")
        for elem in self.element_names:
            footnote = ''
            inv_elem = self.inverse(elem)
            if elem == inv_elem:
                footnote = '  **'
            print(f"{prefix}  inv({elem}) = {self.inverse(elem)} {footnote}")
        size = len(self.element_names)
        if size <= max_size:
            print(f"{prefix}Is associative? {self.associative()}")
            print(f"{prefix}Cayley Table:")
            self.pretty_print_addition_table(prefix=prefix)
        else:
            print(f"{self.__class__.__name__} order is {size} > {max_size}, so no further info calculated/printed.")

    def abelian(self):
        """Returns True if this is a commutative group."""
        result = True
        for e1 in self.element_names:
            for e2 in self.element_names:
                if not (self.add(e1, e2) == self.add(e2, e1)):
                    result = False
                    break
        return result

    def commutative(self):
        return self.abelian()

    # Written and tested, but not sure whether this is needed yet.
    def swap(self, a, b):
        """Change the struture of the group's definition by swapping the order of two elements, a & b."""
        elem = self.element_names
        i, j = elem.index(a), elem.index(b)
        # Swap the two elements in the element_names list
        elem[j], elem[i] = elem[i], elem[j]
        # Swap the corresponding rows
        for row in self.addition_table:
            k, m = row.index(i), row.index(j)
            row[k], row[m] = row[m], row[k]
        # Swap the corresponding columns
        # TODO: Actually swap the two columns here
        return None


# Utilities

def duplicates(lst):
    """Return a list of the duplicate items in the input list."""
    return [item for item, count in Counter(lst).items() if count > 1]


def check_inputs(element_names, addition_table):
    """Check that the element_list and addition_table have sizes and contents
    that don't violate the attributes of a group."""

    # Check for duplicate element names
    # element_set = set(element_names)
    dups = duplicates(element_names)
    if len(dups) == 0:
        pass
    else:
        raise ValueError(f"Duplicate element names: {dups}")

    # Check that table is square
    rows, cols = addition_table.shape
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
    for row in addition_table:
        row_number += 1
        if set(row) == correct_indices:
            pass
        else:
            raise ValueError(f"A row {row_number} does not contain the correct values")

    # Check that each table col contains the correct values for a Cayley table
    for col_number in range(num_elements):
        if set(addition_table[:, col_number]) == correct_indices:
            pass
        else:
            raise ValueError(f"Column {col_number} does not contain the correct values")

    return True


def index_table_from_name_table(name_table):
    """Given a Cayley table using element names, return a table that uses position indices.
    Assumes that the first element in the first row of the table is the identity for the
    table's algebra."""
    top_row = name_table[0]
    return [[top_row.index(elem_name) for elem_name in row] for row in name_table]


def values_in_order(seq):
    starts_with_zero = (seq[0] == 0)
    print(f"Starts with zero? {starts_with_zero}")
    increasing_by_one = all([((seq[i + 1] - seq[i]) == 1) for i in range(len(seq) - 1)])
    print(f"Increasing by one? {increasing_by_one}")
    return starts_with_zero and increasing_by_one


def make_table(table_string):
    """This function helps turn the XML-based tables at Groupprops into a
    list of lists for use here.

    Instructions for use:
    1. Copy the table from there and paste it here;
    2. Find & Replace the strings, "<row>" and "</row>", with nothing;
    3. Place triple quotes around the result and give it a variable name;
    4. Then run make_table on the variable.
    """
    return [[int(n) for n in row.strip().split(" ")]
            for row in table_string.splitlines()]


def swap_list_items(lst, item1, item2):
    a, b = lst.index(item1), lst.index(item2)
    lst[b], lst[a] = lst[a], lst[b]
    return None

if __name__ == '__main__':

    print("\n=======================================================================")

    print("\n--------------")
    print("START OF TESTS")
    print("--------------")

    path = os.path.join(os.getenv('PYPROJ'), 'abstract_algebra')

    algebras = [Group(os.path.join(path, 'Algebras/v4_klein_4_group.json')),
                Group(os.path.join(path, 'Algebras/z4_cyclic_group_of_order_4.json')),
                Group(os.path.join(path, 'Algebras/s3_symmetric_group_on_3_letters.json')),
                Group(os.path.join(path, 'Algebras/s3x_symmetric_group_OTHER.json')),
                Group(os.path.join(path, 'Algebras/Z2xZ2xZ2.json')),
                Group(os.path.join(path, "Algebras/Pinter_page_29.json")),
                Group(os.path.join(path, "Algebras/Pinter_page_29_VERS2.json"))
                ]

    # Create some direct products
    v4_x_z4 = algebras[0] * algebras[1]
    z4_x_s3 = algebras[1] * algebras[2]

    algebras.extend([v4_x_z4, z4_x_s3])

    # Add some algebras that are direct products of the algebras, above:

    for grp in algebras:
        grp.print_info()

    print("\n------------")
    print("END OF TESTS")
    print("------------")

