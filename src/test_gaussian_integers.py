from unittest import TestCase
from gaussian_integers import Gint


class TestGint(TestCase):

    def setUp(self) -> None:
        self.c1 = Gint(4, 5)
        self.c1_conj = Gint(4, -5)
        self.c2 = Gint(1, -2)
        self.c1_x_c2 = Gint(14, -3)  # c1 * c2
        self.c4 = Gint(4, 12)

    def test_constructor(self):
        self.assertEqual(Gint(), Gint(0, 0))
        self.assertEqual(Gint(1), Gint(1, 0))
        self.assertEqual(Gint.eye(), Gint(0, 1))
        self.assertEqual(Gint(2.3,  3.8), Gint(2, 4))
        self.assertEqual(Gint(-2.3,  3.8), Gint(-2, 4))
        self.assertEqual(Gint(2.3, -3.8), Gint(2, -4))
        self.assertEqual(Gint(-2.3, -3.8), Gint(-2, -4))
        self.assertEqual(Gint(2.3, 4), Gint(2, 4))
        self.assertEqual(Gint(-2.3, 4), Gint(-2, 4))
        self.assertEqual(Gint(2, 3.8), Gint(2, 4))
        self.assertEqual(Gint(2, -3.8), Gint(2, -4))

        self.assertEqual(Gint(2.3), Gint(2, 0))
        self.assertEqual(Gint(2), Gint(2, 0))

        self.assertEqual(Gint((2.3-3.7j)), Gint(2, -4))
        self.assertEqual(Gint(-3.3j), Gint(0, -3))

    def test_add(self):  # __add__ & __radd__
        self.assertEqual(Gint(4, 5) + Gint(1, -2), Gint(5, 3))
        self.assertEqual(Gint(4, 5) + 2, Gint(6, 5))
        self.assertEqual(2 + Gint(4, 5), Gint(6, 5))

    def test_sub(self):  # __sub__ & __rsub__
        self.assertEqual(Gint(4, 5) - Gint(1, -2), Gint(3, 7))
        self.assertEqual(Gint(4, 5) - 2, Gint(2, 5))
        self.assertEqual(2 - Gint(4, 5), Gint(-2, -5))

    def test_mul(self):  # __mul__ & __rmul__
        self.assertEqual(Gint(4, 5) * Gint(1, -2), Gint(14, -3))
        self.assertEqual(Gint(4, 5) * Gint(2, 0), Gint(8, 10))  # 2nd Gint is "2"
        self.assertEqual(Gint(4, 5) * 2, Gint(8, 10))  # Gint on left (__mul__)
        self.assertEqual(2 * Gint(4, 5), Gint(8, 10))  # Gint on right (__rmul__)

    def test_div(self):  # __truediv__
        self.assertEqual(self.c1_x_c2 // self.c1, self.c2)
        self.assertEqual(self.c1_x_c2 // self.c2, self.c1)
        self.assertEqual(Gint(4, 12) // 4, Gint(1, 3))

    def test_neg(self):  # __neg__
        self.assertEqual(-Gint(1, -2), Gint(-1, 2))

    def test_pow(self):  # __pow__
        self.assertEqual(self.c1**3, Gint(-236, 115))

    def test_complex(self):  # __complex__
        self.assertEqual(complex(self.c1), (4+5j))

    def test_str(self):  # __str__
        self.assertEqual(str(self.c1), "(4+5j)")

    def test_repr(self):  # __repr__
        self.assertEqual(repr(self.c1), "Gint(4, 5)")

    def test_equal(self):  # __eq__
        self.assertTrue(self.c1 == Gint(4, 5))
        self.assertFalse(self.c1 == self.c2)

    def test_not_equal(self):  # __ne__
        self.assertTrue(self.c1 != self.c2)

    def test_eye(self):
        self.assertEqual(Gint.eye(), Gint(0, 1))

    def test_units(self):
        self.assertEqual(Gint.units(), [Gint(1, 0), Gint(-1, 0), Gint(0, 1), Gint(0, -1)])

    def test_conj(self):
        self.assertEqual(self.c1.conj, self.c1_conj)

    def test_norm(self):
        self.assertEqual(self.c1.norm, 41)

    def test_associates(self):
        self.assertEqual(self.c1.associates(), [Gint(-4, -5), Gint(-5, 4), Gint(5, -4)])

    def test_is_associate(self):
        self.assertTrue(self.c1.is_associate(Gint(-4, -5)))
        self.assertFalse(self.c1.is_associate(self.c2))

    def test_divmod(self):
        a = Gint(4, 5)
        b = Gint(1, -2)
        q, r = a.divmod(b)
        test = f"{b * q + r} = {b} * {q} + {r}"
        answer = "(4+5j) = (1-2j) * (-1+3j) + (-1+0j)"
        self.assertEqual(test, answer)

    def test_mod(self):
        a = Gint(4, 5)
        b = Gint(1, -2)
        test = f"{a} % {b} = {a % b}"
        answer = "(4+5j) % (1-2j) = (-1+0j)"
        self.assertEqual(test, answer)

    def test_gcd_1(self):
        alpha = Gint(32, 9)
        beta = Gint(4, 11)
        self.assertEqual(alpha.gcd(beta), Gint(0, -1))

    def test_gcd_2(self):
        alpha = Gint(11, 3)
        beta = Gint(1, 8)
        self.assertEqual(alpha.gcd(beta), Gint(1, -2))
