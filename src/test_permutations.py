"""
@author: Alfred J. Reich

"""

from unittest import TestCase
from permutations import Perm


class TestPermutations(TestCase):

    def setUp(self) -> None:

        # The example here is from [Pinter, 1990], pages 70-71.
        self.s3 = {'epsilon': Perm((1, 2, 3)),
                   'alpha': Perm((1, 3, 2)),
                   'beta': Perm((3, 1, 2)),
                   'gamma': Perm((2, 1, 3)),
                   'delta': Perm((2, 3, 1)),
                   'kappa': Perm((3, 2, 1))}

        # A reverse lookup dictionary, so that names can be looked up by permutation.
        # This is used when creating the multiplication table.
        self.s3_rev = {val: key for key, val in self.s3.items()}

        self.a = self.s3['alpha']
        self.b = self.s3['beta']
        self.g = self.s3['gamma']

    # Perm((1, 3, 2)) o Perm((3, 1, 2)) = Perm((2, 1, 3))
    # (i.e., alpha o beta = gamma)
    def test_multiplication(self):
        self.assertEqual(self.a * self.b, self.g)

    def test_mult_table_for_s3(self):
        expect = [['epsilon', 'alpha', 'beta', 'gamma', 'delta', 'kappa'],
                  ['alpha', 'epsilon', 'gamma', 'beta', 'kappa', 'delta'],
                  ['beta', 'kappa', 'delta', 'alpha', 'epsilon', 'gamma'],
                  ['gamma', 'delta', 'kappa', 'epsilon', 'alpha', 'beta'],
                  ['delta', 'gamma', 'epsilon', 'kappa', 'beta', 'alpha'],
                  ['kappa', 'beta', 'alpha', 'delta', 'gamma', 'epsilon']]
        s3_mul_tbl = [[self.s3_rev[self.s3[a] * self.s3[b]] for b in self.s3] for a in self.s3]
        self.assertEqual(s3_mul_tbl, expect)

