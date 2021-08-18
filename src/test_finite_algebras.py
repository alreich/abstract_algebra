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

    def test_rps_is_not_associative(self):
        rp = self.rps.op('r', 'p')
        ps = self.rps.op('p', 's')
        rp_s = self.rps.op(rp, 's')
        r_ps = self.rps.op('r', ps)
        self.assertNotEqual(rp_s, r_ps)

    def test_table_with_names(self):
        self.assertEqual(self.rps.table.to_list_with_names(self.rps.elements),
                         [['r', 'p', 'r'], ['p', 'p', 's'], ['r', 's', 's']])

    def test_is_associative(self):
        self.assertEqual(self.rps.is_associative(), False)

    def test_is_commutative(self):
        self.assertEqual(self.rps.is_commutative(), True)

    def test_identity(self):
        self.assertIsNone(self.rps.identity)

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

    def test_rps_is_associative(self):
        self.assertEqual(self.ex141_sg.is_associative(), True)

    def test_rps_is_not_commutative(self):
        self.assertEqual(self.ex141_sg.is_commutative(), False)

    def test_rps_has_no_identity(self):
        self.assertIsNone(self.ex141_sg.identity)

    def test_ex141_is_associative(self):
        ab = self.ex141_sg.op('a', 'b')
        bc = self.ex141_sg.op('b', 'c')
        ab_c = self.ex141_sg.op(ab, 'c')
        a_bc = self.ex141_sg.op('a', bc)
        self.assertEqual(ab_c, a_bc)

    def test_fail_to_create_semigroup_from_rps(self):
        """The RPS magma can't also be made into a semigroup."""
        with self.assertRaises(ValueError):
            Semigroup('rps', 'foobar', ['r', 'p', 's'], [[0, 1, 0], [1, 1, 2], [0, 2, 2]])


class TestGroup(TestCase):

    def setUp(self) -> None:
        self.z2 = generate_cyclic_group(2, name="Z2", description="Cyclic group of order 2")
        self.z4 = generate_cyclic_group(4, name="Z4", description="Cyclic group of order 4")
        self.s3 = generate_symmetric_group(3, name="S3", description="Symmetric group")
        self.ps3 = generate_powerset_group(3, "PS3", "Powerset group")
        self.v4 = make_finite_algebra('V4', 'Klein-4 group', ['e', 'h', 'v', 'r'],
                                      [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])

    def test_elements_accessor_ps3(self):
        self.assertEqual(self.ps3.elements, ['{}', '{0}', '{1}', '{2}', '{0, 1}',
                                             '{0, 2}', '{1, 2}', '{0, 1, 2}'])

    def test_table_accessor_ps3(self):
        self.assertEqual(self.ps3.table, CayleyTable([[0, 1, 2, 3, 4, 5, 6, 7],
                                                      [1, 0, 4, 5, 2, 3, 7, 6],
                                                      [2, 4, 0, 6, 1, 7, 3, 5],
                                                      [3, 5, 6, 0, 7, 1, 2, 4],
                                                      [4, 2, 1, 7, 0, 6, 5, 3],
                                                      [5, 3, 7, 1, 6, 0, 4, 2],
                                                      [6, 7, 3, 2, 5, 4, 0, 1],
                                                      [7, 6, 5, 4, 3, 2, 1, 0]]))

    def test_is_associative_ps3(self):
        self.assertEqual(self.ps3.is_associative(), True)

    def test_is_commutative_ps3(self):
        self.assertEqual(self.ps3.is_commutative(), True)

    def test_identity_accessor_ps3(self):
        self.assertEqual(self.ps3.identity, '{}')

    def test_elements_accessor_z4(self):
        self.assertEqual(self.z4.elements, ['e', 'a', 'a^2', 'a^3'])

    def test_table_accessor_z4(self):
        self.assertEqual(self.z4.table, CayleyTable([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]))

    def test_is_associative_z4(self):
        self.assertEqual(self.z4.is_associative(), True)

    def test_is_commutative_z4(self):
        self.assertEqual(self.z4.is_commutative(), True)

    def test_identity_accessor_z4(self):
        self.assertEqual(self.z4.identity, 'e')

    def test_elements_accessor_s3(self):
        self.assertEqual(self.s3.elements, ['(1, 2, 3)', '(1, 3, 2)', '(2, 1, 3)',
                                            '(2, 3, 1)', '(3, 1, 2)', '(3, 2, 1)'])

    def test_table_accessor_s3(self):
        self.assertEqual(self.s3.table, CayleyTable([[0, 1, 2, 3, 4, 5],
                                                     [1, 0, 4, 5, 2, 3],
                                                     [2, 3, 0, 1, 5, 4],
                                                     [3, 2, 5, 4, 0, 1],
                                                     [4, 5, 1, 0, 3, 2],
                                                     [5, 4, 3, 2, 1, 0]]
                                                    ))

    def test_is_associative_s3(self):
        self.assertEqual(self.s3.is_associative(), True)

    def test_is_commutative_s3(self):
        self.assertEqual(self.s3.is_commutative(), False)

    def test_identity_accessor_s3(self):
        self.assertEqual(self.s3.identity, '(1, 2, 3)')

    def test_direct_product_and_isomorphic(self):
        z2_sqr = self.z2 * self.z2
        self.assertEqual(self.v4.isomorphic(z2_sqr),
                         {'e': 'e:e', 'h': 'e:a', 'v': 'a:e', 'r': 'a:a'})

    def test_not_isomorphic(self):
        self.assertFalse(self.z4.isomorphic(self.v4))


class TestRing(TestCase):

    def setUp(self) -> None:

        self.rng = make_finite_algebra('Powerset Ring 2',
                                       'Ring on powerset of {0, 1}',
                                       ['{}', '{0}', '{1}', '{0, 1}'],
                                       [[0, 1, 2, 3],
                                        [1, 0, 3, 2],
                                        [2, 3, 0, 1],
                                        [3, 2, 1, 0]],
                                       [[0, 0, 0, 0],
                                        [0, 1, 0, 1],
                                        [0, 0, 2, 2],
                                        [0, 1, 2, 3]]
                                       )

    def test_ring_elements(self):
        self.assertEqual(self.rng.elements, ['{}', '{0}', '{1}', '{0, 1}'])

    def test_powerset_mult_table(self):
        self.assertEqual(self.rng.mult_table, CayleyTable([[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]))

    def test_add_identity(self):
        self.assertEqual(self.rng.add_identity, '{}')

    def test_add(self):
        self.assertEqual(self.rng.add('{1}', '{0, 1}'), '{0}')

    def test_mult(self):
        self.assertEqual(self.rng.mult('{1}', '{0, 1}'), '{1}')

    def test_mult_identity(self):
        self.assertEqual(self.rng.mult_identity, '{0, 1}')

    def test_has_mult_identity(self):
        self.assertTrue(self.rng.has_mult_identity())

    def test_ring_zero_divisors(self):
        self.assertEqual(self.rng.zero_divisors(), ['{0}', '{1}'])
