from enum import Enum
import pandas as pd
from pandas import DataFrame


class CurrencyType(Enum):
    BTC = 1
    ETH = 2

class TimeRange(Enum):
    min = 1
    hour = 2
    day = 3

# This data loader can only be used to load at most 2000 data points
class DataLoader:
    def __init__(self):
        self.source_map = {
            CurrencyType.BTC: 'https://min-api.cryptocompare.com/data/v2/histo{}?fsym=BTC&tsym=USD&limit={}',
            CurrencyType.ETH: 'https://min-api.cryptocompare.com/data/v2/histo{}?fsym=ETH&tsym=USD&limit={}'
        }

    def load(self, type: CurrencyType, time_range: TimeRange, limit: int) -> DataFrame:
        currency_url = self.source_map[type].format(time_range.name, limit)
        data = pd.read_json(currency_url)
        history = DataFrame()
        trading_data = data.Data.Data
        history = DataFrame()
        open_prices = []
        close_prices = []
        high_prices = []
        low_prices = []
        volumes = []
        dates = []
        for row in trading_data:
            open_prices.append(row['open'])
            close_prices.append(row['close'])
            high_prices.append(row['high'])
            low_prices.append(row['low'])
            volumes.append(row['volumefrom'])
            dates.append(row['time'])
        history['Open'] = open_prices
        history['Close'] = close_prices
        history['Low'] = low_prices
        history['High'] = high_prices
        history['Volume'] = volumes
        history['Date'] = dates
        return history


def main():
    print("Crypto currency testing start")
    loader = DataLoader()
    eth_history = loader.load(CurrencyType.ETH, TimeRange.hour, 1000)
    btc_history = loader.load(CurrencyType.BTC, TimeRange.hour, 1000)
    print(eth_history, btc_history)


if __name__ == "__main__":
    main()