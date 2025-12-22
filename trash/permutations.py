"""
@author: Alfred J. Reich

"""

# Permutations


class Perm:
    """A Perm (permutation) is a mapping of the consecutive integers, starting at
    the base value, to the integers in the permutation:

    Examples:

    0-based mapping: (0, 1, 2, 3) ==> {0: 0, 1: 1, 2: 2, 3: 3}

    1-based mapping: (3,1,2) ==> {1: 3, 2: 1, 3: 2}

    Permutations can be composed using Python's multiplication operator, '*'.
    Both permutations must use the same base and be of the same size,
    otherwise an exception will be raised.   For example, the permutation,
    (A, B, C) means 1 -> A, 2 -> B, & 3 -> C.
    """

    def __init__(self, permutation):
        self.perm = permutation
        self.base = min(self.perm)  # lowest value in perm
        self.size = len(self.perm) + self.base
        self.mapping = {i: self.perm[i - self.base] for i in range(self.base, self.size)}

    def __eq__(self, other):
        """Return True if the other's enclosed permutation (`tuple`) is the same as this one's."""
        return self.perm == other.perm

    def __hash__(self):
        """Use the enclosed permutation `tuple` for hashing this object"""
        return hash(tuple(self.perm))

    def __repr__(self):
        """A readable print representation of this permutation."""
        return f'Perm({self.perm})'

    def __len__(self):
        """Return the number of elements in the permutation."""
        return len(self.perm)

    def __mul__(self, other):
        """Compose this permutation with another, that is, self(other(id)),
        where id is the identity permutation, (0,1,...,n-1) or (1,2,...,n).
        Both permutations must use the same base and be of the same size,
        otherwise an exception will be raised."""
        if self.base == other.base:
            if len(self) == len(other):
                return Perm(tuple([self.mapping[other.mapping[i]] for i in range(self.base, self.size)]))
            else:
                raise Exception(f"Mixed lengths: {len(self)} != {len(other)}")
        else:
            raise Exception(f"Mixed bases: {self.base} != {other.base}")
