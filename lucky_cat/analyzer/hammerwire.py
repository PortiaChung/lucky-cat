from pandas import DataFrame
from yfinance import Ticker

import plotly.graph_objects as go

from lucky_cat.common.utils.helper import isMonotonic, isMonotonicApproximate


class HammerWire:
    def __init__(self, value_ratio: float = 1 / 5, bot_ratio: float = 3, top_ratio: float = 1 / 3):
        # condition 1: abs(open - close) / (high - low) < value_ratio
        self.value_ratio = value_ratio
        # condition 2: (min(open, close) - low) / (open - close) > pos_ratio
        self.bot_ratio = bot_ratio
        # condition 3: (high - min(open, close)) / (high - low) < top_ratio
        self.top_ratio = top_ratio
        # condition 4: must be monotonically increasing / decreasing

    def is_hammer_wire(self, history: DataFrame) -> bool:
        # history = ticker.history(period='30d')
        latest = history.tail(1)
        # print(latest)
        open = latest['Open'].values[0]
        close = latest['Close'].values[0]
        high = latest['High'].values[0]
        low = latest['Low'].values[0]

        # hammer_wire definition
        day_range = max(abs(high - low), 0.01)
        oc_range = max(abs(open - close), 0.01)

        # meet condition 1
        if oc_range / day_range > self.value_ratio:
            return False
        # meet condition 2
        pos = min(open, close)
        if abs(pos - low) / oc_range < self.bot_ratio:
            return False
        # meet condition 3
        if (high - pos) / day_range > self.top_ratio:
            return False

        # meet condition 4
        # TODO(tianru): revisit algorithm
        # currently, only use close market price within 4 days (maybe open market price is better since we can trade???)
        close_market_prices = []
        monotonic_df = history.tail(4)
        for index, row in monotonic_df.iterrows():
            close_market_prices.append(row['Close'])

        monotonic_df_2 = history.tail(5)
        close_market_prices_2 = []
        for index, row in monotonic_df_2.iterrows():
            close_market_prices_2.append(row['Close'])

        if not isMonotonic(close_market_prices):
            if not isMonotonicApproximate(close_market_prices_2):
                return False

        # fig = go.Figure(
        #     data=[
        #         go.Candlestick(
        #             x=history.index,
        #             open=history['Open'],
        #             high=history['High'],
        #             low=history['Low'],
        #             close=history['Close']
        #         )
        #     ]
        # )
        # fig.show()

        return True