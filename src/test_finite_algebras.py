"""
@author: Alfred J. Reich

"""

from unittest import TestCase

from finite_algebras import *


class TestMagma(TestCase):

    def setUp(self) -> None:
        self.rps = Magma('RPS', "Rock, Paper, Scissors", ['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])

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
        self.assertEqual(self.rps.table_as_list_with_names(), [['r', 'p', 'r'], ['p', 'p', 's'], ['r', 's', 's']])

    def test_is_associative(self):
        self.assertEqual(self.rps.is_associative(), False)

    def test_is_commutative(self):
        self.assertEqual(self.rps.is_commutative(), True)

    def test_identity(self):
        self.assertIsNone(self.rps.identity)

    def test_set_elements(self):
        full_names = ['rock', 'paper', 'scissors']
        self.rps.set_elements(full_names)  # Changes the names used in rps
        rps_copy_with_full_names = Magma('RPS', "Rock, Paper, Scissors",
                                         full_names, [[0, 1, 0], [1, 1, 2], [0, 2, 2]])
        self.assertEqual(self.rps, rps_copy_with_full_names)

    def test_make_finite_algebra_1(self):
        rps2 = make_finite_algebra('RPS', "Rock, Paper, Scissors",
                                   ['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])
        self.assertEqual(rps2, self.rps)


class TestSemigroup(TestCase):

    def setUp(self) -> None:
        self.ex141_tbl = [[0, 3, 0, 3, 0, 3],
                          [1, 4, 1, 4, 1, 4],
                          [2, 5, 2, 5, 2, 5],
                          [3, 0, 3, 0, 3, 0],
                          [4, 1, 4, 1, 4, 1],
                          [5, 2, 5, 2, 5, 2]]

        self.ex141_sg = Semigroup('ex141', 'foobar', ['a', 'b', 'c', 'd', 'e', 'f'], self.ex141_tbl)

    def testIsAssocSG(self):
        self.assertEqual(self.ex141_sg.is_associative(), True)

    def testIsCommSG(self):
        self.assertEqual(self.ex141_sg.is_commutative(), False)

    def test_identitySG(self):
        self.assertIsNone(self.ex141_sg.identity)

    def test_createSG(self):
        """The RPS magma can't also be made into a semigroup."""
        with self.assertRaises(ValueError):
            Semigroup('ex141', 'foobar', ['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])


class TestGroup(TestCase):

    def setUp(self) -> None:
        self.z4 = generate_cyclic_group(4, name="Z4", description="Cyclic group")

    def test_elements_z4(self):
        self.assertEqual(self.z4.elements, ['e', 'a', 'a^2', 'a^3'])

    def test_table_z4(self):
        self.assertEqual(self.z4.table, CayleyTable([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]))

    def testIsAssociative_z4(self):
        self.assertEqual(self.z4.is_associative(), True)

    def testIsCommutative_z4(self):
        self.assertEqual(self.z4.is_commutative(), True)

    def test_identity_z4(self):
        print(self.z4)
        self.assertEqual(self.z4.identity, 'e')