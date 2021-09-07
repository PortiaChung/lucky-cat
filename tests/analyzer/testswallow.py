import unittest

import pandas as pd
from lucky_cat.analyzer.swallow import Swallow


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_upswallow(self):
        swallow = Swallow(4)
        data = [[9, 9.1], [8, 8.1], [7, 7.1], [6, 6.1], [5.1, 5], [4, 6.1]]
        df = pd.DataFrame(data, columns=['Open', 'Close'])
        self.assertEqual(swallow.is_up_swallow(df), True)

    def test_downswallow(self):
        swallow = Swallow(4)
        data = [[4, 4.1], [5, 5.1], [6, 6.1], [7, 7.1], [8, 8.1], [8.2, 7.9]]
        df = pd.DataFrame(data, columns=['Open', 'Close'])
        self.assertEqual(swallow.is_down_swallow(df), True)

        # NKE 08/13/2021
        swallow = Swallow(4)
        data = [[171.41, 173.85], [174.36, 172.80], [172.5, 171.77], [171.56, 172.27], [172, 171.27], [170.89, 170.64], [170.45, 171.69]]
        df = pd.DataFrame(data, columns=['Open', 'Close'])
        self.assertEqual(swallow.is_up_swallow(df), True)



if __name__ == '__main__':
    unittest.main()
