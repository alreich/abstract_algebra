import itertools as it
import json


class Algebra:
    """An abstract algebra with a finite number of elements and an addition table.

    Regarding the format of the addition table, the row element is added on the
    left and the column element on the right. Assuming functions written on the
    left, this means that the column element is applied first and the row element
    is applied next.
    """

    def __init__(self, name, description, element_names, addition_table):
        self.name = name
        self.desc = description
        self.elements = element_names
        self.addition_table = addition_table
        # For efficiency, calculate the headers up front
        self.col_header = self.addition_table[0]
        self.row_header = [row[0] for row in self.addition_table]

    @classmethod
    def make(cls, *args):
        """Create an algebra from a JSON file or a Python dictionary."""

        if str(args[0]):
            print(args[0])
            with open(args[0], 'r') as fin:
                alg_dict = json.load(fin)
        else:
            alg_dict = args[0]

        alg = cls(alg_dict['name'],
                  alg_dict['desc'],
                  alg_dict['elements'],
                  alg_dict['addition_table'])

        return alg

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.desc}>"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.desc}', {self.elements}, {self.addition_table})"

    def to_dict(self):
        return {'type': self.__class__.__name__,
                'name': self.name,
                'desc': self.desc,
                'elements': self.elements,
                'addition_table': self.addition_table}

    def inverse(self, element):
        elem_index = self.elements.index(element)
        row_index = self.row_header.index(elem_index)
        col_index = self.addition_table[row_index].index(0)
        return self.elements[self.col_header[col_index]]

    def addition_table_with_names(self):
        return [[self.elements[x] for x in row] for row in self.addition_table]

    def add(self, r, c):
        """Return the sum of elements, r & c.
        The inputs, r & c, can be numbers or strings, but if either
        input is a number, then a number will be returned, otherwise
        the sum's element name (a string) will be returned."""

        # Table lookup requires numbers
        r_ = r
        c_ = c
        str_result = False
        if type(r) == str:
            r_ = self.elements.index(r)
            str_result = True
        if type(c) == str:
            c_ = self.elements.index(c)
            str_result = True

        # Lookup the product based on the row & column indices
        row_index = self.row_header.index(r_)
        col_index = self.col_header.index(c_)
        product = self.addition_table[row_index][col_index]

        # If either input value was a string, then return a string,
        # otherwise return a number
        if str_result:
            return self.elements[product]
        else:
            return product

    def __mul__(self, other):
        """Return the direct product of this algebra with the input algebra, other."""
        new_name = self.name + "_x_" + other.name
        new_desc = "Direct product of " + self.name + " & " + other.name
        new_elements = list(it.product(self.elements, other.elements))
        new_table = list()
        for e in new_elements:
            new_row = list()
            for f in new_elements:
                new_row.append(new_elements.index((self.add(e[0], f[0]), other.add(e[1], f[1]))))
            new_table.append(new_row)
        return self.__class__(new_name,
                              new_desc,
                              list([f"{c[0]},{c[1]}" for c in new_elements]),
                              new_table)

    def swap(self, a, b):
        """Change the algebra's definition by swapping the order of two elements, a & b."""
        elem = self.elements
        i, j = elem.index(a), elem.index(b)
        elem[j], elem[i] = elem[i], elem[j]
        for row in self.addition_table:
            k, m = row.index(i), row.index(j)
            row[k], row[m] = row[m], row[k]
        return None

    def elements(self):
        return self.addition_table[0]


class Group(Algebra):
    pass


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


# For testing (delete later)
def direct_product(g1, g2):
    new_elements = list(it.product(g1.elements, g2.elements))
    new_table = list()
    for e1 in new_elements:
        new_row = list()
        for e2 in new_elements:
            new_row.append(new_elements.index((g1.add(e1[0], e2[0]), g2.add(e1[1], e2[1]))))
        new_table.append(new_row)
