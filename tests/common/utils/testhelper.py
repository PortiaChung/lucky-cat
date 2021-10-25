import unittest

from lucky_cat.common.utils.helper import isMonotonicIncApproximate, isMonotonicDecApproximate, isIncTrend, isDecTrend


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_isMonotonicIncApproximate(self):
        A = [1.1, 1.2, 1.3, 1.4, 1.5]
        self.assertEqual(isMonotonicIncApproximate(A), True)

        A = [1.1, 1.2, 1.15, 1.3, 1.4]
        self.assertEqual(isMonotonicIncApproximate(A), True)

        A = [1.1, 1.2, 1.15, 1.3, 1.25]
        self.assertEqual(isMonotonicIncApproximate(A), False)

        A = [1.1, 1.2, 1.3, 1.4, 1.35]
        self.assertEqual(isMonotonicIncApproximate(A), False)

    def test_isMonotonicDecApproximate(self):
        A = [1.5, 1.4, 1.3, 1.2, 1.1]
        self.assertEqual(isMonotonicDecApproximate(A), True)

        A = [1.5, 1.4, 1.45, 1.2, 1.1]
        self.assertEqual(isMonotonicDecApproximate(A), True)

        A = [1.5, 1.55, 1.45, 1.46, 1.1]
        self.assertEqual(isMonotonicDecApproximate(A), False)

        A = [1.5, 1.4, 1.3, 1.2, 1.25]
        self.assertEqual(isMonotonicDecApproximate(A), False)

    def test_isIncTrend(self):
        A = [1.5, 1.6, 1.8, 2, 2.3, 2.25, 2.4, 2.6, 2.5, 2.7, 2.9]
        self.assertEqual(isIncTrend(A, 0.2), True)
        self.assertEqual(isIncTrend(A, 0.1), False)

    def test_isDecTrend(self):
        A = [20, 19, 18, 17, 17.2, 16, 15, 15.5, 16, 14.5, 14, 13]
        self.assertEqual(isDecTrend(A, 0.2), False)
        self.assertEqual(isDecTrend(A, 0.3), True)


if __name__ == '__main__':
    unittest.main()
