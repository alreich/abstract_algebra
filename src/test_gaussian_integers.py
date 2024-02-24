from unittest import TestCase
from gaussian_integers import Zi, mod_divmod, gcd, xgcd, is_gaussian_prime


class TestZi(TestCase):

    def setUp(self) -> None:
        self.c1 = Zi(4, 5)
        self.c1_conj = Zi(4, -5)
        self.c2 = Zi(1, -2)
        self.c1_x_c2 = Zi(14, -3)  # c1 * c2
        self.c4 = Zi(4, 12)

    def test_constructor(self):
        self.assertEqual(Zi(), Zi(0, 0))
        self.assertEqual(Zi(1), Zi(1, 0))
        self.assertEqual(Zi.eye(), Zi(0, 1))
        self.assertEqual(Zi(2.3, 3.8), Zi(2, 4))
        self.assertEqual(Zi(-2.3, 3.8), Zi(-2, 4))
        self.assertEqual(Zi(2.3, -3.8), Zi(2, -4))
        self.assertEqual(Zi(-2.3, -3.8), Zi(-2, -4))
        self.assertEqual(Zi(2.3, 4), Zi(2, 4))
        self.assertEqual(Zi(-2.3, 4), Zi(-2, 4))
        self.assertEqual(Zi(2, 3.8), Zi(2, 4))
        self.assertEqual(Zi(2, -3.8), Zi(2, -4))

        self.assertEqual(Zi(2.3), Zi(2, 0))
        self.assertEqual(Zi(2), Zi(2, 0))

        self.assertEqual(Zi((2.3 - 3.7j)), Zi(2, -4))
        self.assertEqual(Zi(-3.3j), Zi(0, -3))

    def test_add(self):  # __add__ & __radd__
        self.assertEqual(Zi(4, 5) + Zi(1, -2), Zi(5, 3))
        self.assertEqual(Zi(4, 5) + 2, Zi(6, 5))
        self.assertEqual(2 + Zi(4, 5), Zi(6, 5))

    def test_sub(self):  # __sub__ & __rsub__
        self.assertEqual(Zi(4, 5) - Zi(1, -2), Zi(3, 7))
        self.assertEqual(Zi(4, 5) - 2, Zi(2, 5))
        self.assertEqual(2 - Zi(4, 5), Zi(-2, -5))

    def test_mul(self):  # __mul__ & __rmul__
        self.assertEqual(Zi(4, 5) * Zi(1, -2), Zi(14, -3))
        self.assertEqual(Zi(4, 5) * Zi(2, 0), Zi(8, 10))  # 2nd Zi is "2"
        self.assertEqual(Zi(4, 5) * 2, Zi(8, 10))  # Zi on left (__mul__)
        self.assertEqual(2 * Zi(4, 5), Zi(8, 10))  # Zi on right (__rmul__)

    def test_div(self):  # __truediv__
        self.assertEqual(self.c1_x_c2 // self.c1, self.c2)
        self.assertEqual(self.c1_x_c2 // self.c2, self.c1)
        self.assertEqual(Zi(4, 12) // 4, Zi(1, 3))

    def test_neg(self):  # __neg__
        self.assertEqual(-Zi(1, -2), Zi(-1, 2))

    def test_pow(self):  # __pow__
        self.assertEqual(self.c1 ** 3, Zi(-236, 115))

    def test_complex(self):  # __complex__
        self.assertEqual(complex(self.c1), (4+5j))

    def test_str(self):  # __str__
        self.assertEqual(str(self.c1), "(4+5j)")

    def test_repr(self):  # __repr__
        self.assertEqual(repr(self.c1), "Zi(4, 5)")

    def test_equal(self):  # __eq__
        self.assertTrue(self.c1 == Zi(4, 5))
        self.assertFalse(self.c1 == self.c2)

    def test_not_equal(self):  # __ne__
        self.assertTrue(self.c1 != self.c2)

    def test_eye(self):
        self.assertEqual(Zi.eye(), Zi(0, 1))

    def test_units(self):
        self.assertEqual(Zi.units(), [Zi(1, 0), Zi(-1, 0), Zi(0, 1), Zi(0, -1)])

    def test_conj(self):
        self.assertEqual(self.c1.conj, self.c1_conj)

    def test_norm(self):
        self.assertEqual(self.c1.norm, 41)

    def test_associates(self):
        self.assertEqual(self.c1.associates(), [Zi(-4, -5), Zi(-5, 4), Zi(5, -4)])

    def test_is_associate(self):
        self.assertTrue(self.c1.is_associate(Zi(-4, -5)))
        self.assertFalse(self.c1.is_associate(self.c2))

    def test_divmod(self):
        a = Zi(4, 5)
        b = Zi(1, -2)
        q, r = mod_divmod(a, b)
        test = f"{b * q + r} = {b} * {q} + {r}"
        answer = "(4+5j) = (1-2j) * (-1+3j) + (-1+0j)"
        self.assertEqual(test, answer)

    def test_mod(self):
        a = Zi(4, 5)
        b = Zi(1, -2)
        test = f"{a} % {b} = {a % b}"
        answer = "(4+5j) % (1-2j) = (-1+0j)"
        self.assertEqual(test, answer)

    def test_gcd_1(self):
        alpha = Zi(32, 9)
        beta = Zi(4, 11)
        self.assertEqual(gcd(alpha, beta), Zi(0, -1))

    def test_gcd_2(self):
        alpha = Zi(11, 3)
        beta = Zi(1, 8)
        self.assertEqual(gcd(alpha, beta), Zi(1, -2))
