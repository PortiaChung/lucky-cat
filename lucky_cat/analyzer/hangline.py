from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from overrides import overrides

# 1. warning level < meteor line
# 2. volume requirement: must be much larger then recent average, the higher, the better
class HangLine(BasicAnalyzer):
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3, hair_to_tail: float = 1 / 2,
                 head_to_tail: float = 1 / 2):
        # condition 1: (high - max(open, close)) / (min(open, close) - low) < hair_to_tail
        self.hair_to_tail = hair_to_tail
        # condition 2: abs(open - close) / (min(open, close) - low) < head_to_tail
        self.head_to_tail = head_to_tail

        # params used to define inc / dec trend
        super().__init__(trend_days, outlier_ratio)

    @overrides
    def isShapeDetected(self, history: DataFrame) -> bool:
        latest = history.iloc[-1]
        open = latest['Open']
        close = latest['Close']
        high = latest['High']
        low = latest['Low']

        # meet condition 1
        if (high - max(open, close)) / max(min(open, close) - low, 0.01) > self.hair_to_tail:
            return False
        # meet condition 2
        if abs(open - close) / max(min(open, close) - low, 0.01) > self.head_to_tail:
            return False
        return True

    @overrides
    def analyze(self, history: DataFrame) -> bool:
        return self.isShapeDetected(history) and self.incTrend(history) and self.isVolumeAmplifed(history, 1.2)
