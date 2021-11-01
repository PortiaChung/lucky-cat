from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides


# warning level < hammer line
# volume requirement: must be much larger then recent average, the higher, the better
class ReverseHammerLine(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3, head_to_hair: float = 1 / 4,
                 tail_to_hair: float = 1 / 2):
        # condition 1: abs(open - close) / (high - max(open, close)) < head_to_hair
        self.head_to_hair = head_to_hair
        # condition 2: min(open, close) - low / (high - max(open,close)) < tail_to_hair
        self.tail_to_hair = tail_to_hair

        # params used to define inc / dec trend
        super().__init__(trend_days, outlier_ratio, 'ReverseHammerLine')

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        latest = history.iloc[-1]
        open = latest['Open']
        close = latest['Close']
        high = latest['High']
        low = latest['Low']

        # meet condition 1
        if abs(open - close) / max(high - max(open, close), 0.01) > self.head_to_hair:
            return False
        # meet condition 2
        if (min(open, close) - low) / max(high - max(open, close), 0.01) > self.tail_to_hair:
            return False
        return True

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected(history) and self.decTrend(history.tail(self.trend_days)) and self.isVolumeAmplifed(
            history, 1.2)
