from unittest import TestCase

from cayley_table import CayleyTable
from finite_algebras import Magma
from copy import deepcopy


class TestMagma(TestCase):

    def setUp(self) -> None:
        self.rps = Magma(['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])

    def test_elements(self):
        self.assertEqual(self.rps.elements, ['r', 'p', 's'])

    def test_table(self):
        self.assertEqual(self.rps.table, CayleyTable([[0, 1, 0], [1, 1, 2], [0, 2, 2]]))

    def test_op_1(self):
        ps = self.rps.op('p', 's')
        r_ps = self.rps.op('r', ps)
        self.assertEqual(r_ps, 'r')

    def test_op_2(self):
        rp = self.rps.op('r', 'p')
        rp_s = self.rps.op(rp, 's')
        self.assertEqual(rp_s, 's')

    def test_table_with_names(self):
        self.assertEqual(self.rps.table_with_names(), [['r', 'p', 'r'], ['p', 'p', 's'], ['r', 's', 's']])

    def test_is_associative(self):
        self.assertEqual(self.rps.is_associative(), False)

    def test_is_commutative(self):
        self.assertEqual(self.rps.is_commutative(), True)

    def test_identity(self):
        self.assertIsNone(self.rps.identity())

    # def test_set_elements(self):
    #     full_names = ['rock', 'paper', 'scissors']
    #     self.rps.set_elements(full_names)
    #     self.assertEqual(self.rps, Magma(full_names, deepcopy(self.rps.table)))

# class Test(TestCase):
#     def test_get_cached_value(self):
#         self.fail()
