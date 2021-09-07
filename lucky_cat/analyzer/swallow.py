from pandas import DataFrame

from lucky_cat.common.utils.helper import isMonotonicInc, isMonotonicIncApproximate, isMonotonicDec, \
    isMonotonicDecApproximate


class Swallow:
    def __init__(self, trend_days: int = 4):
        # days used to define an increasing / decreasing trend
        self.trend_days = trend_days

    def is_up_swallow(self, history: DataFrame) -> bool:
        cur = history.iloc[-1]
        pre = history.iloc[-2]

        # first detect whether we can find a trend from history data, length is defined by trend_days
        trend_df = history.iloc[-2 - self.trend_days + 1:-2]
        ltrend_df = history.iloc[-2 - self.trend_days:-2]

        close_market_prices = []
        for index, row in trend_df.iterrows():
            close_market_prices.append(row['Close'])
        lclose_market_prices = []
        for index, row in ltrend_df.iterrows():
            lclose_market_prices.append(row['Close'])

        if not isMonotonicDec(close_market_prices):
            if not isMonotonicDecApproximate(lclose_market_prices):
                return False

        # trend detected, then try to detect up swallow
        pre_open = pre['Open']
        pre_close = pre['Close']

        # make sure pre_open > pre_close, meaning still downward
        if pre_open < pre_close:
            return False

        cur_open = cur['Open']
        cur_close = cur['Close']
        # make sure cur_open < cur_close, meaning price reverse
        if cur_open > cur_close:
            return False

        # make sure up swallow occur
        if cur_open < pre_close and cur_close > pre_open:
            return True

        return False

    def is_down_swallow(self, history: DataFrame) -> bool:
        cur = history.iloc[-1]
        pre = history.iloc[-2]

        # first detect whether we can find a trend from history data, length is defined by trend_days
        trend_df = history.iloc[-2 - self.trend_days + 1:-2]
        ltrend_df = history.iloc[-2 - self.trend_days:-2]

        close_market_prices = []
        for index, row in trend_df.iterrows():
            close_market_prices.append(row['Close'])
        lclose_market_prices = []
        for index, row in ltrend_df.iterrows():
            lclose_market_prices.append(row['Close'])

        if not isMonotonicInc(close_market_prices):
            if not isMonotonicIncApproximate(lclose_market_prices):
                return False

        # trend detected, then try to detect up swallow
        pre_open = pre['Open']
        pre_close = pre['Close']

        # make sure pre_open < pre_close, meaning still upward
        if pre_open > pre_close:
            return False

        cur_open = cur['Open']
        cur_close = cur['Close']
        # make sure cur_open > cur_close, meaning price reverse
        if cur_open < cur_close:
            return False

        # make sure down swallow occur
        if cur_open > pre_close and cur_close < pre_open:
            return True

        return False