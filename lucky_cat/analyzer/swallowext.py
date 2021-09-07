from pandas import DataFrame

from lucky_cat.common.utils.helper import isMonotonicInc, isMonotonicIncApproximate, isMonotonicDec, \
    isMonotonicDecApproximate


class SwallowExt:
    def __init__(self, trend_days: int = 4, penerate_depth: float = 2 / 3):
        # days used to define an increasing / decreasing trend
        self.trend_days = trend_days
        self.penerate_depth = penerate_depth

    def is_up_swallowext(self, history: DataFrame) -> bool:
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
        pre_low = pre['Low']

        # make sure pre_open > pre_close, meaning still downward
        if pre_open < pre_close:
            return False

        cur_open = cur['Open']
        cur_close = cur['Close']
        # make sure cur_open < cur_close, meaning price reverse
        if cur_open > cur_close:
            return False

        # make sure up swallow occur
        # need to think about whether use pre_low or pre_close
        if cur_open < pre_close \
                and (cur_close - pre_open) * (cur_close - pre_close) < 0 and (cur_close - pre_close) / (pre_open - pre_close) > self.penerate_depth:
            return True

        return False

    def is_down_swallowext(self, history: DataFrame) -> bool:
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
        pre_high = pre['High']

        # make sure pre_open < pre_close, meaning still upward
        if pre_open > pre_close:
            return False

        cur_open = cur['Open']
        cur_close = cur['Close']
        # make sure cur_open > cur_close, meaning price reverse
        if cur_open < cur_close:
            return False

        # make sure down swallow occur
        # need to think whether to use pre_high or pre_close
        if cur_open > pre_close \
                and (cur_close - pre_open) * (cur_close - pre_close) < 0 and (pre_close - cur_close) / (pre_close - pre_open) > self.penerate_depth:
            return True

        return False