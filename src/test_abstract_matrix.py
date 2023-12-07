from unittest import TestCase
import finite_algebras as alg
import abstract_matrix as mat
import numpy as np

class TestAbstractMatrix(TestCase):

    def setUp(self) -> None:

        # The following duplication is for equality testing
        self.psr3 = alg.generate_powerset_ring(3)
        self.psr3x = alg.generate_powerset_ring(3)
        self.arr1 = [['{0, 1, 2}', '{2}', '{2}'],
                     ['{0, 1, 2}', '{2}', '{1, 2}'],
                     ['{0}', '{0, 1, 2}', '{0, 1, 2}']]
        self.arr1x = [['{0, 1, 2}', '{2}', '{2}'],
                      ['{0, 1, 2}', '{2}', '{1, 2}'],
                      ['{0}', '{0, 1, 2}', '{0, 1, 2}']]
        self.mat1 = mat.AbstractMatrix(self.arr1, self.psr3)
        self.mat1x = mat.AbstractMatrix(self.arr1x, self.psr3x)

    def test_equality_of_matrices(self):
        self.assertTrue(self.mat1 == self.mat1x)

    def test_zeros(self):
        self.assertEqual(mat.AbstractMatrix.zeros((3, 4), self.psr3).array.tolist(),
                         [['{}', '{}', '{}', '{}'],
                          ['{}', '{}', '{}', '{}'],
                          ['{}', '{}', '{}', '{}']])

    def test_identity(self):
        self.assertEqual(mat.AbstractMatrix.identity(3, self.psr3).array.tolist(),
                         [['{0, 1, 2}', '{}', '{}'],
                          ['{}', '{0, 1, 2}', '{}'],
                          ['{}', '{}', '{0, 1, 2}']])

    def test_random(self):
        np.random.seed(1)
        self.rand = (mat.AbstractMatrix.random((3, 4), self.psr3).array.tolist(),
                     [['{0, 2}', '{2}', '{0, 1}', '{}'],
                      ['{0, 1, 2}', '{0}', '{2}', '{0, 2}'],
                      ['{0, 1, 2}', '{}', '{}', '{0}']])

    # def test_array(self):
    #     self.fail()

    # def test_shape(self):
    #     self.fail()

    # def test_nrows(self):
    #     self.fail()

    # def test_ncols(self):
    #     self.fail()

    # def test_algebra(self):
    #     self.fail()

    # def test_ring(self):
    #     self.fail()

    # def test_copy(self):
    #     self.fail()

    # def test_transpose(self):
    #     self.fail()

    # def test_scalar_mult(self):
    #     self.fail()

    # def test_minor(self):
    #     self.fail()

    # def test_determinant(self):
    #     self.fail()

    # def test_cofactor_matrix(self):
    #     self.fail()

    # def test_inverse(self):
    #     self.fail()
