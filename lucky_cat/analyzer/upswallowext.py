from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides


class UpSwallowExt(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3, penetrate_depth: float = 2 / 3):
        super().__init__(trend_days, outlier_ratio)
        self.penetrate_depth = penetrate_depth

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        today = history.iloc[-1]
        yesterday = history.iloc[-2]
        # trend detected, then try to detect up swallow
        yesterday_open = yesterday['Open']
        yesterday_close = yesterday['Close']
        yesterday_low = yesterday['Low']

        # make sure pre_open > pre_close, meaning still downward
        if yesterday_open < yesterday_close:
            return False

        today_open = today['Open']
        today_close = today['Close']
        # make sure cur_open < cur_close, meaning price reverse
        if today_open > today_close:
            return False

        # make sure up swallow occur
        # need to think about whether use pre_low or pre_close
        if today_open < yesterday_close \
                and (today_close - yesterday_open) * (today_close - yesterday_close) < 0 and (
                today_close - yesterday_close) / (yesterday_open - yesterday_close) > self.penetrate_depth:
            return True
        return False

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected and self.decTrend(history[:-1]) and self.isVolumeAmplifed(history, 1.2)
