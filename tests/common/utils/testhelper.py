import unittest

from lucky_cat.common.utils.helper import isMonotonicIncApproximate, isMonotonicDecApproximate


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


if __name__ == '__main__':
    unittest.main()
