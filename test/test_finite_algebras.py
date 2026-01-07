"""
@author: Alfred J. Reich

"""

from unittest import TestCase

from finite_algebras import *


class TestMagma(TestCase):

    def setUp(self) -> None:
        self.rps = Magma('RPS', "Rock, Paper, Scissors",
                         ['r', 'p', 's'],
                         [[0, 1, 0], [1, 1, 2], [0, 2, 2]])

    def test_elements(self):
        self.assertEqual(self.rps.elements, ('r', 'p', 's'))

    def test_table1(self):
        self.assertEqual(self.rps.table.tolist(), [[0, 1, 0], [1, 1, 2], [0, 2, 2]])

    def test_table2(self):
        self.assertEqual(self.rps.table, CayleyTable([[0, 1, 0], [1, 1, 2], [0, 2, 2]]))

    def test_rps_is_not_associative(self):
        rp = self.rps.op('r', 'p')
        ps = self.rps.op('p', 's')
        rp_s = self.rps.op(rp, 's')
        r_ps = self.rps.op('r', ps)
        self.assertNotEqual(rp_s, r_ps)
        # op associates from left to right for multiple arguments
        _rps = self.rps.op('r', 'p', 's')
        self.assertTrue(_rps == rp_s)
        self.assertFalse(_rps == r_ps)

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
        self.ex141_sg = Semigroup('ex141', 'foobar',
                                  ['a', 'b', 'c', 'd', 'e', 'f'], self.ex141_tbl)

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
            Semigroup('rps', 'foobar', ['r', 'p', 's'],
                      [[0, 1, 0], [1, 1, 2], [0, 2, 2]])

    def test_equality_of_semigroups(self):
        sg2 = Semigroup(
            'ex141',
            'foobar',
            ['a', 'b', 'c', 'd', 'e', 'f'],
            [[0, 3, 0, 3, 0, 3], [1, 4, 1, 4, 1, 4], [2, 5, 2, 5, 2, 5], [3, 0, 3, 0, 3, 0], [4, 1, 4, 1, 4, 1],
             [5, 2, 5, 2, 5, 2]]
        )
        self.assertEqual(self.ex141_sg, sg2)


class TestGroup(TestCase):

    def setUp(self) -> None:
        self.z2 = generate_cyclic_group(2, name="Z2", description="Cyclic group of order 2")
        self.z4 = generate_cyclic_group(4, name="Z4", description="Cyclic group of order 4")
        self.s3 = generate_symmetric_group(3, name="S3", description="Symmetric group")
        self.ps3 = generate_powerset_group(3, "PS3", "Powerset group")
        self.r6 = generate_algebra_mod_n(6)
        self.v4 = make_finite_algebra('V4', 'Klein-4 group', ['e', 'h', 'v', 'r'],
                                      [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])
        self.v4x = make_finite_algebra('V4', 'Klein-4 group', ['e', 'h', 'v', 'r'],
                                       [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])

    def test_element_orders(self):
        self.assertEqual(self.v4.element_order('e'), 1)
        self.assertEqual(self.v4.element_order('h'), 2)
        self.assertEqual(self.ps3.element_order('{}'), 1)
        self.assertEqual(self.ps3.element_order('{0}'), 2)
        self.assertEqual(self.r6.element_order('0'), 1)
        self.assertEqual(self.r6.element_order('1'), 6)
        self.assertEqual(self.r6.element_order('2'), 3)
        self.assertEqual(self.r6.element_order('3'), 2)

    def test_group_equality(self):
        self.assertTrue(self.v4 == self.v4x)

    def test_elements_accessor_ps3(self):
        self.assertEqual(self.ps3.elements, ('{}', '{0}', '{1}', '{2}', '{0, 1}',
                                             '{0, 2}', '{1, 2}', '{0, 1, 2}'))

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
        self.assertEqual(self.z4.elements, ('0', '1', '2', '3'))

    def test_table_accessor_z4_1(self):
        self.assertEqual(self.z4.table,
                         CayleyTable([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]))

    def test_table_accessor_z4_2(self):
        self.assertEqual(self.z4.table.tolist(),
                         [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]])

    def test_is_associative_z4(self):
        self.assertEqual(self.z4.is_associative(), True)

    def test_is_commutative_z4(self):
        self.assertEqual(self.z4.is_commutative(), True)

    def test_identity_accessor_z4(self):
        self.assertEqual(self.z4.identity, '0')

    def test_elements_accessor_s3(self):
        # self.assertEqual(self.s3.elements, ['(1, 2, 3)', '(1, 3, 2)', '(2, 1, 3)',
        #                                     '(2, 3, 1)', '(3, 1, 2)', '(3, 2, 1)'])
        self.assertEqual(self.s3.elements, ('(0, 1, 2)', '(0, 2, 1)', '(1, 0, 2)',
                                            '(1, 2, 0)', '(2, 0, 1)', '(2, 1, 0)'))

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
        # self.assertEqual(self.s3.identity, '(1, 2, 3)')
        self.assertEqual(self.s3.identity, '(0, 1, 2)')

    def test_direct_product_and_isomorphic(self):
        z2_sqr = self.z2 * self.z2
        self.assertEqual(self.v4.isomorphic(z2_sqr),
                         {'e': '0:0', 'h': '0:1', 'r': '1:1', 'v': '1:0'})

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
        self.rng2 = generate_powerset_group(2)

    # def test_ring_equality(self):
    #     self.assertTrue(self.rng == self.rng2)

    def test_ring_elements(self):
        self.assertEqual(self.rng.elements, ('{}', '{0}', '{1}', '{0, 1}'))

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


class TestField(TestCase):

    def setUp(self) -> None:

        self.f4_elems = ['0', '1', 'a', '1+a']

        self.f4_add_table = [['0', '1', 'a', '1+a'],
                             ['1', '0', '1+a', 'a'],
                             ['a', '1+a', '0', '1'],
                             ['1+a', 'a', '1', '0']]

        self.f4_mult_table = [['0', '0', '0', '0'],
                              ['0', '1', 'a', '1+a'],
                              ['0', 'a', '1+a', '1'],
                              ['0', '1+a', '1', 'a']]

        self.f4 = make_finite_algebra('F4',
                                      'Field with 4 elements',
                                      self.f4_elems,
                                      self.f4_add_table,
                                      self.f4_mult_table
                                      )

        self.f4x = make_finite_algebra('F4X',
                                       'Field with 4 elements EXTRA COPY',
                                       self.f4_elems,
                                       self.f4_add_table,
                                       self.f4_mult_table
                                       )

    def test_field_equality(self):
        self.assertTrue(self.f4 == self.f4x)

    def test_mult_inv(self):
        self.assertEqual(self.f4.mult_inv('a'), '1+a')

    def test_div(self):
        self.assertEqual(self.f4.div('1', '1+a'), 'a')

    def test_mult_abelian_subgroup(self):
        self.subgrp = self.f4.mult_abelian_subgroup()
        self.assertEqual(self.subgrp.elements, ('1', 'a', '1+a'))
        self.assertEqual(self.subgrp.table.tolist(), [[0, 1, 2], [1, 2, 0], [2, 0, 1]])

