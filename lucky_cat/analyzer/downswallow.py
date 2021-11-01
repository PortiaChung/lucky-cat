from pandas import DataFrame
from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides


class DownSwallow(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3):
        super().__init__(trend_days, outlier_ratio, 'DownSwallow', False)

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        cur = history.iloc[-1]
        pre = history.iloc[-2]
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

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected(history) and self.incTrend(
            history[:-1].tail(self.trend_days)) and self.isVolumeAmplifed(history, 1.2)
