from unittest import TestCase
from gaussian_integers import Gint


class TestGint(TestCase):

    def setUp(self) -> None:
        self.c1 = Gint(4, 5)
        self.c1_conj = Gint(4, -5)
        self.c2 = Gint(1, -2)
        self.c1_x_c2 = Gint(14, -3)  # c1 * c2
        self.c4 = Gint(4, 12)

    def test_add(self):
        self.assertEqual(Gint(4, 5) + Gint(1, -2), Gint(5, 3))

    def test_sub(self):
        self.assertEqual(Gint(4, 5) - Gint(1, -2), Gint(3, 7))

    def test_mul(self):
        self.assertEqual(Gint(4, 5) * Gint(1, -2), Gint(14, -3))
        self.assertEqual(Gint(4, 5) * Gint(2, 0), Gint(8, 10))  # 2nd Gint is "2"

    def test_mul_by_int(self):
        self.assertEqual(Gint(4, 5) * 2, Gint(8, 10))  # Gint on left (__mul__)
        self.assertEqual(2 * Gint(4, 5), Gint(8, 10))  # Gint on right (__rmul__)

    def test_div(self):
        self.assertEqual(Gint(4, 12) / 4, Gint(1, 3))

    def test_neg(self):
        self.assertEqual(-Gint(1, -2), Gint(-1, 2))

    def test_eye(self):
        self.assertEqual(Gint.eye(), Gint(0, 1))

    def test_units(self):
        self.assertEqual(Gint.units(), [Gint(1, 0), Gint(-1, 0), Gint(0, 1), Gint(0, -1)])

    def test_conj(self):
        self.assertEqual(self.c1.conj, self.c1_conj)

    def test_norm(self):
        self.assertEqual(self.c1.norm, 41)

    def test_divides(self):
        self.assertTrue(self.c1.divides(self.c1_x_c2))

    def test_divided_by(self):
        self.assertTrue(self.c1_x_c2.divided_by(self.c1))
        self.assertTrue(self.c4.divided_by(4))

    def test_associates(self):
        self.assertEqual(self.c1.associates(), [Gint(-4, -5), Gint(-5, 4), Gint(5, -4)])

    def test_is_associate(self):
        self.assertTrue(self.c1.is_associate(Gint(-4, -5)))
        self.assertFalse(self.c1.is_associate(self.c2))
