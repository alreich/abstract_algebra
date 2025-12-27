class Perm:
    """A permutation is of size n is, essentially, a list or tuple containing
    the first n-1 non-negative integers. For example, (2, 0, 1, 3) or [0, 1, 2, 3],
    are permutations of size 4. All n-1 non-negative integers must be present,
    and no integers can be duplicated.
    """

    def __init__(self, mapping):
        self._mapping = tuple(mapping)
        self._size = len(mapping)
        self._is_even = None  # memoized at first call to 'is_even' method

    @property
    def mapping(self):
        return self._mapping

    @property
    def size(self):
        return self._size

    @property
    def is_even(self):
        if self._is_even is None:
            self._is_even = self._is_even_fnc()
            return self._is_even
        else:
            return self._is_even

    def __eq__(self, other):
        return self._mapping == other.mapping

    def __hash__(self):
        return hash(self._mapping)

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        return self._mapping[index]

    def __mul__(self, other):
        """self * other (apply 'other' first, then 'self')
        Example: p * q = p[q[i]]"""
        new_mapping = [0] * self._size
        for i in range(self._size):
            new_mapping[i] = self[other[i]]
        return Perm(new_mapping)

    def __repr__(self):
        return f"Perm({self._mapping})"

    def __str__(self):
        return str(self._mapping)

    def _is_even_fnc(self):
        inversions = 0
        # Iterate through all possible pairs of elements
        for i in range(self._size):
            for j in range(i + 1, self._size):
                # If a pair is out of natural order, it's an inversion
                if self._mapping[i] > self._mapping[j]:
                    inversions += 1
        # If the total inversions are even, the permutation is even
        return inversions % 2 == 0

    def show(self):  # Just for testing
        return f"<{self._mapping}, {self._size}, {self._is_even}>"

    @property
    def parity(self):
        return "Even" if self.is_even else "Odd"