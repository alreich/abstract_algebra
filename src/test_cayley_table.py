"""
@author: Alfred J. Reich

"""

from unittest import TestCase
from cayley_table import CayleyTable


class TestCayleyTable(TestCase):

    def setUp(self) -> None:
        # not assoc; is comm; no identity -- the RPS magma table, above
        self.tbl1 = [[0, 1, 0],
                     [1, 1, 2],
                     [0, 2, 2]]
        self.tbl1_copy = [[0, 1, 0],
                          [1, 1, 2],
                          [0, 2, 2]]

        # is assoc; not comm; has identity (0) --- the S3 group table
        self.tbl2 = [[0, 1, 2, 3, 4, 5],
                     [1, 2, 0, 5, 3, 4],
                     [2, 0, 1, 4, 5, 3],
                     [3, 4, 5, 0, 1, 2],
                     [4, 5, 3, 2, 0, 1],
                     [5, 3, 4, 1, 2, 0]]

        # is assoc; is comm; has identity (0) --- the Z4 group table
        self.tbl3 = [[0, 1, 2, 3],
                     [1, 2, 3, 0],
                     [2, 3, 0, 1],
                     [3, 0, 1, 2]]

        # powerset(3) group table
        self.tbl4 = [[0, 1, 2, 3, 4, 5, 6, 7],
                     [1, 0, 4, 5, 2, 3, 7, 6],
                     [2, 4, 0, 6, 1, 7, 3, 5],
                     [3, 5, 6, 0, 7, 1, 2, 4],
                     [4, 2, 1, 7, 0, 6, 5, 3],
                     [5, 3, 7, 1, 6, 0, 4, 2],
                     [6, 7, 3, 2, 5, 4, 0, 1],
                     [7, 6, 5, 4, 3, 2, 1, 0]]

        self.tbl5 = [[0, 3, 0, 3, 0, 3],
                     [1, 4, 1, 4, 1, 4],
                     [2, 5, 2, 5, 2, 5],
                     [3, 0, 3, 0, 3, 0],
                     [4, 1, 4, 1, 4, 1],
                     [5, 2, 5, 2, 5, 2]]

        test_arrays = [self.tbl1, self.tbl2, self.tbl3, self.tbl4, self.tbl5]

        self.test_tables = [CayleyTable(tbl) for tbl in test_arrays]

    # ABOUT TEST_TABLES:
    #
    #    Table  Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?
    # -------------------------------------------------------------------------------------
    #      1      3       False         True         None      None       None      False
    #      2      6        True        False            0         0          0       True
    #      3      4        True         True            0         0          0       True
    #      4      8        True         True            0         0          0       True
    #      5      6        True        False         None         0       None      False

    def test_inverse_lookup_dict_1(self):
        tb1 = self.test_tables[1]
        id1 = 0
        self.assertEqual(tb1.inverse_lookup_dict(id1), {0: 0, 1: 2, 2: 1, 3: 3, 4: 4, 5: 5})

    def test_inverse_lookup_dict_2(self):
        tb2 = self.test_tables[2]
        id2 = 0
        self.assertEqual(tb2.inverse_lookup_dict(id2), {0: 0, 1: 3, 2: 2, 3: 1})

    def test_table_order(self):
        result = [tbl.order for tbl in self.test_tables]
        self.assertEqual(result, [3, 6, 4, 8, 6])

    def test_table_associative(self):
        result = [tbl.is_associative() for tbl in self.test_tables]
        self.assertEqual(result, [False, True, True, True, True])

    def test_table_left_id(self):
        result = [tbl.left_identity() for tbl in self.test_tables]
        self.assertEqual(result, [None, 0, 0, 0, None])

    def test_table_right_id(self):
        result = [tbl.right_identity() for tbl in self.test_tables]
        self.assertEqual(result, [None, 0, 0, 0, 0])

    def test_table_identity(self):
        result = [tbl.identity() for tbl in self.test_tables]
        self.assertEqual(result, [None, 0, 0, 0, None])

    def test_table_has_inverses(self):
        result = [tbl.has_inverses() for tbl in self.test_tables]
        self.assertEqual(result, [False, True, True, True, False])

    def test_cayley_table_to_str(self):
        ct = CayleyTable(self.tbl3)
        result = 'CayleyTable([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]])'
        self.assertEqual(str(ct), result)

    def test_equal(self):
        self.assertEqual(CayleyTable(self.tbl1), CayleyTable(self.tbl1_copy))

    # def test_about_tables(self):
    #     about_tables(self.test_tables)
