import itertools as it
import numpy as np
import json
import os


class Algebra:
    """An abstract algebra with a finite number of elements and an addition (Cayley) table.

    The arguments can consist of a single string, representing the path to a JSON
    file that defines the algebra, or a single Python dictionary, that defines the
    algebra, or the four quantities listed below:
        name: A string name for the algebra;
        description: A string describing the algebra;
        element_names: A list of strings that represent the names of algebra elements;
        addition_table: a list of lists of numbers that represent positions of elements
            in the elements list.

    Regarding the format of the addition table, the row element is added on the
    left and the column element on the right, e.g., row + col.  Or, assuming
    functions written on the left (such as permutations), this means that the
    column element is applied first and the row element is applied next, e.g.,
    row(col(x)).
    """
    def __init__(self, *args):

        if len(args) == 1:
            if isinstance(args[0], str):
                with open(args[0], 'r') as fin:
                    # Assumes the single arg is a JSON file name string
                    alg_dict = json.load(fin)
            else:
                # Assumes the single argument is a dictionary
                alg_dict = args[0]
        else:
            # Assumes all fields were input
            alg_dict = {'name': args[0],
                        'description': args[1],
                        'element_names': args[2],
                        'addition_table': args[3]
                        }
        self.name = alg_dict['name']
        self.description = alg_dict['description']
        self.element_names = alg_dict['element_names']
        self.addition_table = np.array(alg_dict['addition_table'], dtype=np.int64)
        self.inverse_lookup_dict = self._make_inverse_lookup_dict()
        self.dp_delimiter = ','  # name delimiter used when creating direct products

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.description}>"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.element_names}, {self.addition_table})"

    def set_direct_product_delimiter(self, delimiter=','):
        """Change or reset the delimiter used to construct new element names of direct products.
        The default delimiter is a comma."""
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
        """Write the algebra to a JSON string."""
        return json.dumps(self.to_dict())

    def dump(self, path):
        """Write the algebra to a JSON file."""
        with open(path, 'w') as fout:
            json.dump(self.to_dict(), fout)

    def inverse(self, element_name):
        """Return the inverse name of the input element name."""
        return self.inverse_lookup_dict[element_name]

    def addition_table_with_names(self):
        """Return the addition table with element names rather than element positions."""
        return [[self.element_names[elem_pos] for elem_pos in row] for row in self.addition_table]

    def add(self, a, b):
        """Given element names, r & c, return the sum, r + c, according the the addition table."""
        a_pos = self.element_names.index(a)
        b_pos = self.element_names.index(b)
        product_index = self.addition_table[a_pos, b_pos]
        return self.element_names[product_index]

    # def pretty_print_addition_table_OLDER(self, delimiter=' ', prefix=''):
    #     field_size = 1 + len(max(self.element_names, key=len))  # 1 + Longest Name Length
    #     for elem1 in self.element_names:
    #         row = f"{prefix}"
    #         for elem2 in self.element_names:
    #             row += delimiter + f"{self.add(elem1, elem2) :>{field_size}}"
    #         print(row)

    # def pretty_print_addition_table_OLD(self, delimiter=' ', prefix=''):
    #     """The method name says it all."""
    #     field_size = 1 + len(max(self.element_names, key=len))  # 1 + Longest Name Length
    #     for elem1 in self.element_names:
    #         idx1 = self.element_names.index(elem1)
    #         row = f"{prefix}"
    #         for elem2 in self.element_names:
    #             idx2 = self.element_names.index(elem2)
    #             prod = self.element_names[self.addition_table[idx1, idx2]]
    #             row += delimiter + f"{prod :>{field_size}}"
    #         print(row)

    def pretty_print_addition_table(self, delimiter=' ', prefix=''):
        field_size = 1 + len(max(self.element_names, key=len))  # 1 + Longest Name Length
        for row_index in self.addition_table[:, 0]:  # row index from first column
            row_string = f"{prefix}"
            for col_index in self.addition_table[0]:  # column index from first row
                prod_index = self.addition_table[row_index, col_index]
                prod_name = self.element_names[prod_index]
                row_string += delimiter + f"{prod_name :>{field_size}}"
            print(row_string)

    def associative(self):
        "A brute force test of associativity.  Returns True if the algebra is associative."
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
        """Return the direct product of this algebra with the input algebra, other."""
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

    # def addition_table_row(self, row_num):
    #     return self.addition_table[row_num]
    #
    # def addition_table_column(self, col_num):
    #     return self.addition_table[:, col_num]

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

    # Written and tested, but not sure whether this is needed yet.
    def swap(self, a, b):
        """Change the algebra's definition by swapping the order of two elements, a & b."""
        elem = self.element_names
        i, j = elem.index(a), elem.index(b)
        elem[j], elem[i] = elem[i], elem[j]
        for row in self.addition_table:
            k, m = row.index(i), row.index(j)
            row[k], row[m] = row[m], row[k]
        return None


class Group(Algebra):
    """This algebra is a group."""

    # TODO: Automatically check the addition table using check_addition_table, below.
    def check_addition_table(self):
        """Check that each row and column in the table has a unique number of elements equal to the
        expected number of elements.  Basically, each element should appear exactly once in each row
        and each column. Returns True if the table is OK."""
        num_elements = len(self.element_names)  # the expected number of elements
        result = True
        for row in self.addition_table:
            if not (num_elements == len(set(row))):
                result = False
                break
        for col_num in range(num_elements):
            if not (num_elements == len(set(self.table_column(col_num)))):
                result = False
                break
        return result

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


# Utilities

def values_in_order(seq):
    starts_with_zero = (seq[0] == 0)
    print(f"Starts with zero? {starts_with_zero}")
    increasing_by_one = all([((seq[i + 1] - seq[i]) == 1) for i in range(len(seq) - 1)])
    print(f"Increasing by one? {increasing_by_one}")
    return starts_with_zero and increasing_by_one


def first_column(table):
    return [row[0] for row in table]


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

