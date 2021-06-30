from unittest import TestCase
from algebras import Group, generate_powerset_group
import os


class TestGroup(TestCase):

    def setUp(self) -> None:
        aa_path = os.path.join(os.getenv("PYPROJ"), "abstract_algebra")
        alg_dir = os.path.join(aa_path, "Algebras")
        v4_json = os.path.join(alg_dir, "v4_klein_4_group.json")
        self.v4 = Group(v4_json)
        self.v4_subs = self.v4.proper_subgroups()
        self.v4_sub0 = self.v4_subs[0]
        self.ps3 = generate_powerset_group(3)
        self.ps3.element_names = ['e', 'a', 'b', 'c', 'd', 'f', 'g', 'h']

    def test_order(self):
        self.assertEqual(self.v4.order, 4)
        self.assertEqual(self.ps3.order, 8)

    def test_element_order(self):
        self.assertEqual(self.v4.element_order('v'), 2)

    def test_identity(self):
        self.assertEqual(self.v4.identity, 'e')

    # def test_deepcopy(self):
    #     self.fail()

    def test_direct_product_delimiter(self):
        self.assertEqual(self.v4.direct_product_delimiter(), ':')

    def test_to_dict(self):
        self.assertEqual(self.v4.to_dict(), {'type': 'Group',
                                             'name': 'V4',
                                             'description': 'Klein-4 group',
                                             'element_names': ['e', 'h', 'v', 'r'],
                                             'mult_table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]})

    def test_dumps(self):
        self.assertEqual(self.v4.dumps(), '{"type": "Group", "name": "V4",'
                                          ' "description": "Klein-4 group",'
                                          ' "element_names": ["e", "h", "v", "r"],'
                                          ' "mult_table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}')

    # def test_dump(self):
    #     self.fail()

    def test_inv(self):
        self.assertEqual(self.v4.inv('h'), 'h')

    def test_conj(self):
        self.assertEqual(self.v4.conj('h', 'v'), 'h')

    def test_mult_table_with_names(self):
        self.assertEqual(self.v4.mult_table_with_names(), [['e', 'h', 'v', 'r'], ['h', 'e', 'r', 'v'], ['v', 'r', 'e', 'h'], ['r', 'v', 'h', 'e']])

    def test_mult(self):
        self.assertEqual(self.v4.mult(), 'e')
        self.assertEqual(self.v4.mult('h'), 'h')
        self.assertEqual(self.v4.mult('h', 'v'), 'r')
        self.assertEqual(self.v4.mult('h', 'r', 'v'), 'e')

    # def test_pprint(self):
    #     self.fail()

    def test_is_associative(self):
        self.assertEqual(self.v4.is_associative(), True)

    # def test_about(self):
    #     self.fail()

    # def test_about_proper_subgroups(self):
    #     self.fail()

    def test_is_abelian(self):
        self.assertEqual(self.v4.is_abelian(), True)

    def test_commutative(self):
        self.assertEqual(self.v4.is_commutative(), True)

    # def test_subgroups(self):
    #     self.assertEqual(self.v4_subs, [Group('V4_subgroup_0',
    #                                           'Subgroup of: Klein-4 group',
    #                                           ['e', 'v'],
    #                                           [[0, 1], [1, 0]]),
    #                                     Group('V4_subgroup_1',
    #                                           'Subgroup of: Klein-4 group',
    #                                           ['e', 'h'],
    #                                           [[0, 1], [1, 0]]),
    #                                     Group('V4_subgroup_2',
    #                                           'Subgroup of: Klein-4 group',
    #                                           ['e', 'r'],
    #                                           [[0, 1], [1, 0]])])

    # def test_unique_proper_subgroups(self):
    #     self.assertEqual(self.v4.unique_proper_subgroups(), [Group('V4_subgroup_0',
    #                                                                'Subgroup of: Klein-4 group',
    #                                                                ['e', 'v'],
    #                                                                [[0, 1], [1, 0]]) ])

    def test_is_normal(self):
        self.assertEqual(self.v4.is_normal(self.v4_sub0), True)

    def test_closure(self):
        pass
        # self.fail()

    def test_closed_proper_subsets_of_elements(self):
        pass
        # self.fail()

    def test_subgroup_from_elements(self):
        pass
        # self.fail()

    def test_proper_subgroups(self):
        pass
        # self.fail()

    def test_trivial_subgroups(self):
        pass
        # self.fail()

    def test_reorder_elements(self):
        pass
        # self.fail()

    def test_element_mappings(self):
        pass
        # self.fail()

    def test_isomorphic_mapping(self):
        pass
        # self.fail()

    def test_isomorphic(self):
        pass
        # self.fail()
