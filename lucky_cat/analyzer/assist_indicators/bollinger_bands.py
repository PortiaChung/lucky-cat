import datetime
from pandas import DataFrame


class BollingerBands:
    def __init__(self, history: DataFrame):
        self.history = history

    def calculate(self, len: int) -> DataFrame:
        num_of_rows = self.history.shape[0]
        assert num_of_rows > len
        assert len > 0
        close_prices = self.history['Close'].values.tolist()
        # print(close_prices)
        dates = self.history['Date'].values.tolist()[len - 1:]
        readable_dates = []
        for date in dates:
            # print(date)
            readable_dates.append(datetime.datetime.fromtimestamp(date / 1e9, datetime.timezone.utc))
        prices = []
        down_prices = []
        up_prices = []
        for i in range(len - 1, num_of_rows):
            range_sum = 0
            for j in range(i - len + 1, i + 1):
                range_sum += close_prices[j]
            avg_price = range_sum * 1.0 / len
            variance = 0
            for j in range(i - len + 1, i + 1):
                variance += pow(close_prices[j] - avg_price, 2)
            down_prices.append(avg_price - 2 * variance ** (1/2))
            up_prices.append(avg_price + 2 * variance ** (1/2))
            prices.append(avg_price)
        result = DataFrame()
        result['Date'] = readable_dates
        result['Price'] = prices
        result['UpPrice'] = up_prices
        result['DownPrice'] = down_prices
        return result