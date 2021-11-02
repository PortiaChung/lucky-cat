import datetime

from pandas import DataFrame
import pandas as pd

class RSI:
    def __init__(self, history: DataFrame):
        self.history = history

    def calculate(self, len: int = 14):
        # Wells Wider's implementation
        # num_of_rows = self.history.shape[0]
        # assert num_of_rows > len
        # assert len > 0
        # close_prices = self.history['Close'].values.tolist()
        #
        # dates = self.history['Date'].values.tolist()[len:]
        # readable_dates = []
        # for date in dates:
        #     # print(date)
        #     readable_dates.append(datetime.datetime.fromtimestamp(date / 1e9, datetime.timezone.utc))
        # indices = []
        # for i in range(len, num_of_rows):
        #     up_sum = 0
        #     down_sum = 0
        #     for j in range(i - len + 1, i + 1):
        #         if close_prices[j] >= close_prices[j - 1]:
        #             up_sum += close_prices[j] - close_prices[j - 1]
        #         else:
        #             down_sum += close_prices[j - 1] - close_prices[j]
        #     indices.append(up_sum / (up_sum + down_sum) * 100)
        # result = DataFrame()
        # result['Date'] = readable_dates
        # result['Indices'] = indices
        # return result

        # TradingView's implementation
        dates = self.history['Date'].values.tolist()
        readable_dates = []
        for date in dates:
            readable_dates.append(datetime.datetime.fromtimestamp(date / 1e9, datetime.timezone.utc))
        delta = self.history["Close"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(len - 1), min_periods=len).mean()
        _loss = down.abs().ewm(com=(len - 1), min_periods=len).mean()

        RS = _gain / _loss
        series = pd.Series(100 - (100 / (1 + RS)), name="RSI")
        result = DataFrame()
        result['Indices'] = series
        result['Date'] = readable_dates
        return result.iloc[len:]