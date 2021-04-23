import itertools as it
import json


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
        self.addition_table = alg_dict['addition_table']
        # For efficiency, calculate the headers up front
        self._col_header = self.addition_table[0]
        self._row_header = [row[0] for row in self.addition_table]
        self._dp_delimiter = ','  # name delimiter used when creating direct products

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.description}>"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.element_names}, {self.addition_table})"

    def set_direct_product_delimiter(self, delimiter=','):
        """Change or reset the delimiter used to construct new element names of direct products.
        The default delimiter is a comma."""
        self._dp_delimiter = delimiter
        return None

    def to_dict(self):
        """Return a dictionary that represents this group."""
        return {'type': self.__class__.__name__,
                'name': self.name,
                'description': self.description,
                'element_names': self.element_names,
                'addition_table': self.addition_table}

    def dumps(self):
        """Write the algebra to a JSON string."""
        return json.dumps(self.to_dict())

    def dump(self, path):
        """Write the algebra to a JSON file."""
        with open(path, 'w') as fout:
            json.dump(self.to_dict(), fout)

    def inverse(self, element_name):
        """Return the inverse of the input element name."""
        elem_index = self.element_names.index(element_name)
        row_index = self._row_header.index(elem_index)
        col_index = self.addition_table[row_index].index(0)
        return self.element_names[self._col_header[col_index]]

    def addition_table_with_names(self):
        """Return the addition table with element names rather than element positions."""
        return [[self.element_names[elem_pos] for elem_pos in row] for row in self.addition_table]

    def add(self, r, c):
        """Given element names, r & c, return the sum, r + c, according the the addition table."""
        # Find the positions of r & c in the list of element names.
        r_pos = self.element_names.index(r)
        c_pos = self.element_names.index(c)
        # Lookup the product based on the row & column indices
        row_index = self._row_header.index(r_pos)
        col_index = self._col_header.index(c_pos)
        product_index = self.addition_table[row_index][col_index]
        return self.element_names[product_index]

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
                              list([f"{elem[0]}{self._dp_delimiter}{elem[1]}" for elem in dp_element_names]),
                              dp_addition_table)

    def table_column(self, n):
        """Return the n_th column of the addition table."""
        return [row[n] for row in self.addition_table]

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
