from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides


class UpHugLine(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3):
        super().__init__(trend_days, outlier_ratio, 'UpHugLine')

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        today = history.iloc[-1]
        yesterday = history.iloc[-2]

        # meet shape condition
        if yesterday['Close'] >= yesterday['Open']:
            return False
        if today['Open'] >= today['Close']:
            return False
        if not (yesterday['Low'] > today['Open'] and yesterday['High'] < today['Close']):
            return False
        return True

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected(history) and self.decTrend(
            history[:-1].tail(self.trend_days)) and self.isVolumeAmplifed(history, 1.0)
