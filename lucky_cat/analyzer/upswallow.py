from pandas import DataFrame
from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides


class UpSwallow(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3):
        super().__init__(trend_days, outlier_ratio, 'UpSwallow')

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        today = history.iloc[-1]
        yesterday = history.iloc[-2]
        # trend detected, then try to detect up swallow
        yesterday_open = yesterday['Open']
        yesterday_close = yesterday['Close']

        # make sure pre_open > pre_close, meaning still downward
        if yesterday_open < yesterday_close:
            return False

        today_open = today['Open']
        today_close = today['Close']
        # make sure cur_open < cur_close, meaning price reverse
        if today_open > today_close:
            return False

        # make sure up swallow occur
        if today_open < yesterday_close and today_close > yesterday_open:
            return True
        return False

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected(history) and self.decTrend(
            history[:-1].tail(self.trend_days)) and self.isVolumeAmplifed(history, 1.5)
