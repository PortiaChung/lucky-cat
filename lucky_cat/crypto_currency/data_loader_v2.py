import string

import bitfinex
import datetime
import time
import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class DataLoaderV2:
    def __init__(self):
        self.api_v2 = bitfinex.bitfinex_v2.api_v2()

    def load(self, symbol: string, timeframe: string, start_time: datetime.datetime, end_time: datetime.datetime,
             limit: int) -> DataFrame:
        pair = symbol
        TIMEFRAME = timeframe
        t_start = time.mktime(start_time.timetuple()) * 1000
        t_stop = time.mktime(end_time.timetuple()) * 1000

        # print("https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist?limit={}&start={}&end={}&sort=-1".format(TIMEFRAME, pair.upper(), limit, t_start, t_stop))

        result = self.api_v2.candles(symbol=pair, interval=TIMEFRAME, limit=limit, start=t_start, end=t_stop)
        names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
        df = pd.DataFrame(result, columns=names)
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        return df


def main():
    dataLoaderV2 = DataLoaderV2()
    result = dataLoaderV2.load('ETHUSD', '1h', datetime.datetime(2012, 9, 1, 0, 0),
                               datetime.datetime(2021, 11, 7, 0, 0), 10000)
    # fig = make_subplots(rows=1, cols=1, shared_xaxes=True,
    #                     vertical_spacing=0.03, subplot_titles=['ETH', 'Volume', 'RSI', 'MA'])
    # fig.add_trace(go.Candlestick(x=result['Date'], open=result['Open'], close=result['Close'], high=result['High'],
    #                              low=result['High'], name='ETH', opacity=1), row=1, col=1)
    # fig.show()



if __name__ == "__main__":
    main()
