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
        self.arr1t = [['{0, 1, 2}', '{0, 1, 2}', '{0}'],
                      ['{2}', '{2}', '{0, 1, 2}'],
                      ['{2}', '{1, 2}', '{0, 1, 2}']]
        self.arr2 = [['{0, 2}', '{2}', '{2}'],
                     ['{0, 2}', '{2}', '{2}'],
                     ['{0}', '{0, 2}', '{0, 2}']]
        self.arr3 = [['{0, 1, 2}', '{2}'],
                     ['{0}', '{0, 1, 2}']]
        self.arr4 = [['{1}', '{0, 1, 2}', '{0, 1, 2}'],
                     ['{}', '{0, 1, 2}', '{0, 1, 2}'],
                     ['{}', '{1}', '{}']]
        self.arr5 = [['{0, 1, 2}', '{0, 1, 2}', '{0}'],
                     ['{0, 1, 2}', '{0, 2}', '{0, 1}'],
                     ['{0}', '{0, 1}', '{0}']]
        self.arr6 = [['{}', '{0, 1}', '{0, 2}'],
                     ['{0, 1}', '{}', '{0}'],
                     ['{0, 2}', '{0}', '{}']]
        self.arr7 = [['{}', '{0, 1}', '{0, 2}'],
                     ['{0, 1}', '{}', '{0}'],
                     ['{0, 2}', '{0}', '{}']]
        self.mat1 = mat.AbstractMatrix(self.arr1, self.psr3)
        self.mat1x = mat.AbstractMatrix(self.arr1x, self.psr3x)
        self.mat1t = mat.AbstractMatrix(self.arr1t, self.psr3)
        self.mat2 = mat.AbstractMatrix(self.arr2, self.psr3)
        self.mat1minor = mat.AbstractMatrix(self.arr3, self.psr3)
        self.mat1cof = mat.AbstractMatrix(self.arr4, self.psr3)
        self.mat1xmat1t = mat.AbstractMatrix(self.arr5, self.psr3)
        self.mat1pmat1t = mat.AbstractMatrix(self.arr6, self.psr3)
        self.mat1mmat1t = mat.AbstractMatrix(self.arr7, self.psr3)

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

    def test_array(self):
        self.assertEqual(self.mat1.array.tolist(), self.arr1)

    def test_shape(self):
        self.assertEqual(self.mat1.shape, (3, 3))

    def test_nrows(self):
        self.assertEqual(self.mat1.nrows, 3)

    def test_ncols(self):
        self.assertEqual(self.mat1.ncols, 3)

    def test_algebra(self):
        self.assertTrue(self.mat1.algebra == self.psr3x)

    def test_ring(self):
        self.assertTrue(self.mat1.algebra == self.psr3x)

    def test_copy(self):
        self.assertTrue(self.mat1 == self.mat1.copy())

    def test_transpose(self):
        self.assertTrue(self.mat1.transpose() == self.mat1t)

    def test_scalar_mult(self):
        self.assertTrue(self.mat1.scalar_mult('{0, 2}'), self.mat2)

    def test_minor(self):
        self.assertTrue(self.mat1.minor(1, 1), self.mat1minor)

    def test_determinant(self):
        self.assertEqual(self.mat1.determinant(), '{1}')

    def test_cofactor_matrix(self):
        self.assertTrue(self.mat1.cofactor_matrix() == self.mat1cof)

    def test_multiplication(self):
        self.assertTrue(self.mat1 * self.mat1.transpose() == self.mat1xmat1t)

    def test_addition(self):
        self.assertTrue(self.mat1 + self.mat1.transpose() == self.mat1pmat1t)

    def test_subtraction(self):
        self.assertTrue(self.mat1 - self.mat1.transpose() == self.mat1mmat1t)

    def test_getitem(self):
        self.assertEqual(self.mat1[1, 2], '{1, 2}')

    def test_setitem(self):
        self.mat1[1, 2] = '{}'
        self.assertEqual(self.mat1[1, 2], '{}')
        self.mat1[1, 2] = '{1, 2}'  # Put original value back

    # def test_inverse(self):
    #     self.fail()
