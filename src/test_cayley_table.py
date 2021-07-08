from unittest import TestCase
from cayley_table import CayleyTable, about_tables


class Test(TestCase):

    def setUp(self) -> None:

        # not assoc; is comm; no identity -- the RPS magma table, above
        tbl1 = [[0, 1, 0], [1, 1, 2], [0, 2, 2]]

        # is assoc; not comm; has identity (0) --- the S3 group table
        tbl2 = [[0, 1, 2, 3, 4, 5], [1, 2, 0, 5, 3, 4], [2, 0, 1, 4, 5, 3],
                [3, 4, 5, 0, 1, 2], [4, 5, 3, 2, 0, 1], [5, 3, 4, 1, 2, 0]]

        # is assoc; is comm; has identity (0) --- the Z4 group table
        tbl3 = [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]

        # powerset(3) group table
        tbl4 = [[0, 1, 2, 3, 4, 5, 6, 7], [1, 0, 4, 5, 2, 3, 7, 6], [2, 4, 0, 6, 1, 7, 3, 5],
                [3, 5, 6, 0, 7, 1, 2, 4], [4, 2, 1, 7, 0, 6, 5, 3], [5, 3, 7, 1, 6, 0, 4, 2],
                [6, 7, 3, 2, 5, 4, 0, 1], [7, 6, 5, 4, 3, 2, 1, 0]]

        tbl5 = [[0, 3, 0, 3, 0, 3], [1, 4, 1, 4, 1, 4], [2, 5, 2, 5, 2, 5],
                [3, 0, 3, 0, 3, 0], [4, 1, 4, 1, 4, 1], [5, 2, 5, 2, 5, 2]]

        test_arrays = [tbl1, tbl2, tbl3, tbl4, tbl5]

        self.test_tables = [CayleyTable(tbl) for tbl in test_arrays]

    def test_about_tables(self):
        for tbl in self.test_tables:
            print(tbl)
            print()

    def test_inverse_lookup_dict(self):
        tbl = self.test_tables[2]
        id = 0
        print(tbl.inverse_lookup_dict(id))

    def test_cayley_table(self):
        about_tables(self.test_tables)
